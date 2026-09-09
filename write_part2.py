import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote:", path)

write_file("app/src/main/java/com/orbit/assistant/data/engine/RealOrbitEngine.kt", """package com.orbit.assistant.data.engine

import com.orbit.assistant.data.remote.OmniRouteClient
import com.orbit.assistant.data.remote.OmniRouteException
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.model.ActionCardData
import com.orbit.assistant.domain.model.ActionItem
import com.orbit.assistant.domain.model.ActionStatus
import com.orbit.assistant.domain.model.ChatCompletionMessage
import com.orbit.assistant.domain.model.ChatCompletionRequest
import com.orbit.assistant.domain.model.ConversationMessage
import com.orbit.assistant.domain.model.MessageSender
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.domain.model.ToolResult
import com.orbit.assistant.domain.repository.ActivityRepository
import com.orbit.assistant.domain.repository.SettingsRepository
import com.orbit.assistant.domain.tools.ToolRegistry
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

class RealOrbitEngine(
    private val omniRouteClient: OmniRouteClient,
    private val settingsRepository: SettingsRepository,
    private val activityRepository: ActivityRepository,
    private val toolRegistry: ToolRegistry,
    private val onSpeak: ((String) -> Unit)? = null,
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.Default)
) : OrbitEngine {

    private val _currentState = MutableStateFlow(OrbitState.IDLE)
    override val currentState: StateFlow<OrbitState> = _currentState.asStateFlow()

    private val _conversation = MutableStateFlow<List<ConversationMessage>>(listOf(
        ConversationMessage(
            id = "orbit_init",
            sender = MessageSender.ORBIT,
            text = "Orbit native core online. Connected to local device environment."
        )
    ))
    override val conversation: StateFlow<List<ConversationMessage>> = _conversation.asStateFlow()

    private val _isOnline = MutableStateFlow(true)
    override val isOnline: StateFlow<Boolean> = _isOnline.asStateFlow()

    private var currentJob: Job? = null

    override fun stop() {
        currentJob?.cancel()
        _currentState.value = OrbitState.IDLE
    }

    override suspend fun clearConversation() {
        _conversation.value = emptyList()
    }

    override suspend fun checkHealth(): Boolean {
        val settings = settingsRepository.settingsState.value
        val apiKey = settingsRepository.getApiKey()
        val res = omniRouteClient.getModels(settings.omniRouteUrl, apiKey)
        val healthy = res.isSuccess
        _isOnline.value = healthy
        if (!healthy && _currentState.value == OrbitState.IDLE) {
            _currentState.value = OrbitState.OFFLINE
        } else if (healthy && _currentState.value == OrbitState.OFFLINE) {
            _currentState.value = OrbitState.IDLE
        }
        return healthy
    }

    override suspend fun processCommand(userPrompt: String) {
        if (userPrompt.isBlank()) return
        stop()

        currentJob = scope.launch {
            val userMsg = ConversationMessage(
                id = UUID.randomUUID().toString(),
                sender = MessageSender.USER,
                text = userPrompt
            )
            _conversation.value = _conversation.value + userMsg
            _currentState.value = OrbitState.THINKING

            val settings = settingsRepository.settingsState.value
            val apiKey = settingsRepository.getApiKey()
            val modelToUse = if (settings.selectedModel == "Auto") {
                settings.availableModels.firstOrNull { it != "Auto" } ?: "local-default"
            } else {
                settings.selectedModel
            }
            val maxSteps = settings.maxAgentSteps.coerceIn(1, 10)
            var currentStep = 0
            var isFinished = false

            val systemInstruction = \"\"\"
                You are Orbit, an autonomous on-device personal AI assistant for Android.
                You can execute tasks on the user's Android device using predefined tools:
                - open_app(package_name): Launch installed applications (e.g. com.google.android.youtube)
                - open_url(url): Open websites in browser
                - get_current_time(): Get real local time
                - search_web(query): Search the web
                
                Never execute arbitrary shell commands or code.
                If asked to open an app like YouTube, call open_app with package_name "com.google.android.youtube".
                Keep responses direct, natural, and helpful.
            \"\"\".trimIndent()

            val chatHistory = mutableListOf<ChatCompletionMessage>(
                ChatCompletionMessage(role = "system", content = systemInstruction)
            )

            val recentMessages = _conversation.value.takeLast(10)
            for (msg in recentMessages) {
                chatHistory.add(
                    ChatCompletionMessage(
                        role = if (msg.sender == MessageSender.USER) "user" else "assistant",
                        content = msg.text
                    )
                )
            }

            val availableTools = toolRegistry.getChatCompletionTools()

            try {
                while (!isFinished && currentStep < maxSteps) {
                    currentStep++
                    val request = ChatCompletionRequest(
                        model = modelToUse,
                        messages = chatHistory,
                        tools = if (availableTools.isNotEmpty()) availableTools else null,
                        toolChoice = "auto",
                        temperature = 0.7f
                    )

                    val responseResult = omniRouteClient.createChatCompletion(
                        baseUrl = settings.omniRouteUrl,
                        apiKey = apiKey,
                        requestData = request
                    )

                    responseResult.fold(
                        onSuccess = { response ->
                            _isOnline.value = true
                            val choice = response.choices.firstOrNull()
                            if (choice == null) {
                                postOrbitError("No response choices returned by OmniRoute model.")
                                isFinished = true
                                return@fold
                            }

                            val responseMessage = choice.message
                            chatHistory.add(responseMessage)

                            val toolCalls = responseMessage.toolCalls
                            if (!toolCalls.isNullOrEmpty()) {
                                _currentState.value = OrbitState.EXECUTING
                                for (toolCall in toolCalls) {
                                    val funcName = toolCall.function.name
                                    val funcArgs = toolCall.function.arguments
                                    val toolResult = toolRegistry.execute(funcName, funcArgs)
                                    val isSuccess = toolResult is ToolResult.Success
                                    val resultText = toolResult.toJsonString()

                                    val timeStr = SimpleDateFormat("hh:mm a", Locale.getDefault()).format(Date())
                                    val actionItem = ActionItem(
                                        id = UUID.randomUUID().toString(),
                                        title = "Tool: $funcName",
                                        detail = if (isSuccess) (toolResult as ToolResult.Success).message else (toolResult as ToolResult.Failure).error,
                                        timestamp = timeStr,
                                        status = if (isSuccess) ActionStatus.COMPLETED else ActionStatus.FAILED
                                    )
                                    activityRepository.recordAction(actionItem)

                                    val actionCard = ActionCardData(
                                        title = funcName.uppercase(),
                                        detail = if (isSuccess) (toolResult as ToolResult.Success).message else (toolResult as ToolResult.Failure).error,
                                        statusText = if (isSuccess) "✓ Completed" else "✕ Failed",
                                        isSuccess = isSuccess
                                    )

                                    chatHistory.add(
                                        ChatCompletionMessage(
                                            role = "tool",
                                            toolCallId = toolCall.id,
                                            name = funcName,
                                            content = resultText
                                        )
                                    )

                                    _conversation.value = _conversation.value + ConversationMessage(
                                        id = UUID.randomUUID().toString(),
                                        sender = MessageSender.ORBIT,
                                        text = if (isSuccess) "Executed $funcName successfully." else "Tool $funcName failed: ${(toolResult as ToolResult.Failure).error}",
                                        actionCard = actionCard
                                    )
                                }
                                _currentState.value = OrbitState.THINKING
                            } else {
                                isFinished = true
                                val replyText = responseMessage.content ?: "Command acknowledged."
                                _currentState.value = OrbitState.SPEAKING
                                val finalMessage = ConversationMessage(
                                    id = UUID.randomUUID().toString(),
                                    sender = MessageSender.ORBIT,
                                    text = replyText
                                )
                                _conversation.value = _conversation.value + finalMessage
                                if (settings.textToSpeech) {
                                    onSpeak?.invoke(replyText)
                                }
                                kotlinx.coroutines.delay(1200)
                                _currentState.value = OrbitState.IDLE
                            }
                        },
                        onFailure = { err ->
                            isFinished = true
                            handleEngineError(err)
                        }
                    )
                }

                if (currentStep >= maxSteps && !isFinished) {
                    postOrbitError("Agent reached maximum step limit ($maxSteps). Operation stopped to avoid infinite loops.")
                }
            } catch (e: Exception) {
                handleEngineError(e)
            }
        }
    }

    private suspend fun handleEngineError(err: Throwable) {
        when (err) {
            is OmniRouteException.NotRunning -> {
                _isOnline.value = false
                _currentState.value = OrbitState.OFFLINE
                postOrbitMessage("OmniRoute is offline. Make sure the local server is active at ${settingsRepository.settingsState.value.omniRouteUrl}.")
            }
            is OmniRouteException.InvalidApiKey -> {
                _currentState.value = OrbitState.ERROR
                postOrbitMessage("Invalid OmniRoute API key. Please verify credentials in Settings.")
            }
            is OmniRouteException.ModelUnavailable -> {
                _currentState.value = OrbitState.ERROR
                postOrbitMessage("Requested model '${err.modelName}' is unavailable on OmniRoute.")
            }
            is OmniRouteException.ConnectionTimeout -> {
                _currentState.value = OrbitState.ERROR
                postOrbitMessage("OmniRoute connection timed out. Check local port connectivity.")
            }
            else -> {
                _currentState.value = OrbitState.ERROR
                postOrbitMessage("Error: ${err.localizedMessage ?: "Failed to contact OmniRoute"}")
            }
        }
    }

    private fun postOrbitMessage(text: String) {
        _conversation.value = _conversation.value + ConversationMessage(
            id = UUID.randomUUID().toString(),
            sender = MessageSender.ORBIT,
            text = text
        )
    }

    private fun postOrbitError(errorText: String) {
        _currentState.value = OrbitState.ERROR
        _conversation.value = _conversation.value + ConversationMessage(
            id = UUID.randomUUID().toString(),
            sender = MessageSender.ORBIT,
            text = errorText,
            actionCard = ActionCardData(
                title = "ORBIT ERROR",
                detail = errorText,
                statusText = "✕ Halted",
                isSuccess = false
            )
        )
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/service/OrbitAccessibilityService.kt", """package com.orbit.assistant.service

import android.accessibilityservice.AccessibilityService
import android.content.Intent
import android.view.accessibility.AccessibilityEvent
import android.util.Log

class OrbitAccessibilityService : AccessibilityService() {

    companion object {
        private const val TAG = "OrbitAccessibility"
        var instance: OrbitAccessibilityService? = null
            private set

        val isServiceRunning: Boolean
            get() = instance != null
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
        Log.d(TAG, "Orbit Accessibility Service Connected.")
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // Passive observation of window state changes
    }

    override fun onInterrupt() {
        Log.w(TAG, "Orbit Accessibility Service Interrupted.")
    }

    override fun onDestroy() {
        super.onDestroy()
        instance = null
    }

    fun launchApplicationSafe(packageName: String): Boolean {
        return try {
            val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
            if (launchIntent != null) {
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(launchIntent)
                true
            } else {
                false
            }
        } catch (e: Exception) {
            Log.e(TAG, "Failed to launch package $packageName", e)
            false
        }
    }

    fun tapCoordinates(x: Float, y: Float): Boolean {
        throw UnsupportedOperationException("Direct screen touch dispatch is reserved for Phase 2 Device Synergy.")
    }

    fun swipeGesture(startX: Float, startY: Float, endX: Float, endY: Float): Boolean {
        throw UnsupportedOperationException("Direct gesture swipe is reserved for Phase 2 Device Synergy.")
    }

    fun typeTextIntoFocusedNode(text: String): Boolean {
        throw UnsupportedOperationException("Direct IME node text injection is reserved for Phase 2 Device Synergy.")
    }

    fun readScreenNodeTree(): String {
        throw UnsupportedOperationException("Direct screen node scraping is reserved for Phase 2 Device Synergy.")
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/service/voice/OrbitTextToSpeech.kt", """package com.orbit.assistant.service.voice

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import java.util.Locale

class OrbitTextToSpeech(context: Context) : TextToSpeech.OnInitListener {

    private var tts: TextToSpeech? = TextToSpeech(context.applicationContext, this)
    private var isInitialized = false

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = tts?.setLanguage(Locale.US)
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.w("OrbitTTS", "Language is not supported on device TTS engine.")
            } else {
                isInitialized = true
                tts?.setPitch(1.05f)
                tts?.setSpeechRate(1.0f)
            }
        } else {
            Log.e("OrbitTTS", "Failed to initialize Android TextToSpeech engine.")
        }
    }

    fun speak(text: String) {
        if (!isInitialized) return
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "orbit_utterance_${System.currentTimeMillis()}")
    }

    fun stop() {
        tts?.stop()
    }

    fun shutdown() {
        tts?.stop()
        tts?.shutdown()
        tts = null
        isInitialized = false
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/service/voice/OrbitSpeechRecognizer.kt", """package com.orbit.assistant.service.voice

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.Locale

class OrbitSpeechRecognizer(private val context: Context) {

    private var speechRecognizer: SpeechRecognizer? = null

    private val _isListening = MutableStateFlow(false)
    val isListening: StateFlow<Boolean> = _isListening.asStateFlow()

    private val _spokenText = MutableStateFlow<String?>(null)
    val spokenText: StateFlow<String?> = _spokenText.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    fun isAvailable(): Boolean = SpeechRecognizer.isRecognitionAvailable(context)

    fun startListening(onResult: (String) -> Unit) {
        if (!isAvailable()) {
            _error.value = "Speech recognition service is not available on this device."
            return
        }

        stopListening()

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(context).apply {
            setRecognitionListener(object : RecognitionListener {
                override fun onReadyForSpeech(params: Bundle?) {
                    _isListening.value = true
                    _error.value = null
                }
                override fun onBeginningOfSpeech() {}
                override fun onRmsChanged(rmsdB: Float) {}
                override fun onBufferReceived(buffer: ByteArray?) {}
                override fun onEndOfSpeech() {
                    _isListening.value = false
                }
                override fun onError(errorCode: Int) {
                    _isListening.value = false
                    val msg = when (errorCode) {
                        SpeechRecognizer.ERROR_NO_MATCH -> "No speech recognized. Please try again."
                        SpeechRecognizer.ERROR_NETWORK -> "Network issue during speech recognition."
                        SpeechRecognizer.ERROR_AUDIO -> "Audio recording error."
                        SpeechRecognizer.ERROR_CLIENT -> "Speech recognition client error."
                        else -> "Speech recognition error code: $errorCode"
                    }
                    _error.value = msg
                }
                override fun onResults(results: Bundle?) {
                    _isListening.value = false
                    val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    val text = matches?.firstOrNull()?.trim()
                    if (!text.isNullOrBlank()) {
                        _spokenText.value = text
                        onResult(text)
                    }
                }
                override fun onPartialResults(partialResults: Bundle?) {}
                override fun onEvent(eventType: Int, params: Bundle?) {}
            })
        }

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
        }

        speechRecognizer?.startListening(intent)
    }

    fun stopListening() {
        _isListening.value = false
        speechRecognizer?.stopListening()
        speechRecognizer?.destroy()
        speechRecognizer = null
    }
}
""")

print("Part 2 written successfully.")
