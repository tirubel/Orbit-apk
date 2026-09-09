package com.orbit.assistant.data.engine

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

            val systemInstruction = """
                You are Orbit, an autonomous on-device personal AI assistant for Android.
                You can execute tasks on the user's Android device using predefined tools:
                - open_app(package_name): Launch installed applications (e.g. com.google.android.youtube)
                - open_url(url): Open websites in browser
                - get_current_time(): Get real local time
                - search_web(query): Search the web
                
                Never execute arbitrary shell commands or code.
                If asked to open an app like YouTube, call open_app with package_name "com.google.android.youtube".
                Keep responses direct, natural, and helpful.
            """.trimIndent()

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
