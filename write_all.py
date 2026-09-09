import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote:", path)

# ToolModels.kt
write_file("app/src/main/java/com/orbit/assistant/domain/model/ToolModels.kt", """package com.orbit.assistant.domain.model

import kotlinx.serialization.json.JsonObject

data class ToolDefinition(
    val name: String,
    val description: String,
    val parameterSchema: JsonObject
)

sealed class ToolResult {
    data class Success(val message: String, val data: Map<String, String> = emptyMap()) : ToolResult()
    data class Failure(val error: String, val details: String? = null) : ToolResult()

    fun toJsonString(): String {
        return when (this) {
            is Success -> \"\"\"{"success": true, "message": "$message"}\"\"\"
            is Failure -> \"\"\"{"success": false, "error": "$error"${'$'}{details?.let { \"\"\", "details": "$it"\"\"\" } ?: ""}}\"\"\"
        }
    }
}
""")

# Repositories & interfaces
write_file("app/src/main/java/com/orbit/assistant/domain/repository/SecureStorage.kt", """package com.orbit.assistant.domain.repository

interface SecureStorage {
    suspend fun getApiKey(): String?
    suspend fun saveApiKey(apiKey: String)
    suspend fun clearApiKey()
    suspend fun hasApiKey(): Boolean
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/repository/SettingsRepository.kt", """package com.orbit.assistant.domain.repository

import com.orbit.assistant.domain.model.SettingsState
import kotlinx.coroutines.flow.StateFlow

interface SettingsRepository {
    val settingsState: StateFlow<SettingsState>
    suspend fun updateSettings(transform: (SettingsState) -> SettingsState)
    suspend fun saveApiKey(apiKey: String)
    suspend fun getApiKey(): String?
    suspend fun testOmniRouteConnection(): Result<Pair<Int, List<String>>> // Returns (latencyMs, models)
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/repository/ActivityRepository.kt", """package com.orbit.assistant.domain.repository

import com.orbit.assistant.domain.model.ActionItem
import kotlinx.coroutines.flow.StateFlow

interface ActivityRepository {
    val actions: StateFlow<List<ActionItem>>
    suspend fun recordAction(action: ActionItem)
    suspend fun clearHistory()
}
""")

# Tools
write_file("app/src/main/java/com/orbit/assistant/domain/tools/OrbitTool.kt", """package com.orbit.assistant.domain.tools

import com.orbit.assistant.domain.model.ChatCompletionTool
import com.orbit.assistant.domain.model.ChatCompletionToolFunction
import com.orbit.assistant.domain.model.ToolResult
import kotlinx.serialization.json.JsonObject

interface OrbitTool {
    val name: String
    val description: String
    val parametersSchema: JsonObject

    fun toChatCompletionTool(): ChatCompletionTool {
        return ChatCompletionTool(
            type = "function",
            function = ChatCompletionToolFunction(
                name = name,
                description = description,
                parameters = parametersSchema
            )
        )
    }

    suspend fun execute(argumentsJson: String): ToolResult
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/tools/ToolRegistry.kt", """package com.orbit.assistant.domain.tools

import com.orbit.assistant.domain.model.ChatCompletionTool
import com.orbit.assistant.domain.model.ToolResult
import java.util.concurrent.ConcurrentHashMap

class ToolRegistry {
    private val tools = ConcurrentHashMap<String, OrbitTool>()

    fun register(tool: OrbitTool) {
        tools[tool.name] = tool
    }

    fun getTool(name: String): OrbitTool? = tools[name]
    fun getAllTools(): List<OrbitTool> = tools.values.toList()

    fun getChatCompletionTools(): List<ChatCompletionTool> {
        return tools.values.map { it.toChatCompletionTool() }
    }

    suspend fun execute(name: String, argumentsJson: String): ToolResult {
        val tool = tools[name] ?: return ToolResult.Failure(
            error = "UNKNOWN_TOOL",
            details = "The tool '$name' is not registered in Orbit's secure ToolRegistry."
        )
        return try {
            tool.execute(argumentsJson)
        } catch (e: Exception) {
            ToolResult.Failure(
                error = "TOOL_RUNTIME_EXCEPTION",
                details = e.localizedMessage ?: "Unexpected error during tool execution"
            )
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/tools/OpenAppTool.kt", """package com.orbit.assistant.domain.tools

import android.content.Context
import android.content.Intent
import com.orbit.assistant.domain.model.ToolResult
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonObject

class OpenAppTool(private val context: Context) : OrbitTool {
    override val name: String = "open_app"
    override val description: String = "Launches an installed Android application given its verified package name (e.g. com.google.android.youtube)."
    override val parametersSchema: JsonObject = buildJsonObject {
        put("type", "object")
        putJsonObject("properties") {
            putJsonObject("package_name") {
                put("type", "string")
                put("description", "The Android application package name (e.g. com.google.android.youtube, com.android.chrome)")
            }
        }
        put("required", kotlinx.serialization.json.buildJsonArray {
            add(kotlinx.serialization.json.JsonPrimitive("package_name"))
        })
    }

    private val packageNameRegex = Regex("^[a-zA-Z][a-zA-Z0-9_]*(\\\\.[a-zA-Z][a-zA-Z0-9_]*)+$")

    override suspend fun execute(argumentsJson: String): ToolResult {
        return try {
            val jsonElement = Json.parseToJsonElement(argumentsJson).jsonObject
            val packageName = jsonElement["package_name"]?.jsonPrimitive?.content?.trim()
                ?: return ToolResult.Failure("INVALID_ARGUMENTS", "package_name is required")

            // Strict security validation
            if (!packageNameRegex.matches(packageName)) {
                return ToolResult.Failure("SECURITY_VIOLATION", "Invalid package name format")
            }

            val packageManager = context.packageManager
            val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
            if (launchIntent == null) {
                ToolResult.Failure("APP_NOT_INSTALLED", "Package '$packageName' is not installed on this device")
            } else {
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                context.startActivity(launchIntent)
                val appLabel = try {
                    val appInfo = packageManager.getApplicationInfo(packageName, 0)
                    packageManager.getApplicationLabel(appInfo).toString()
                } catch (e: Exception) {
                    packageName
                }
                ToolResult.Success("$appLabel opened", mapOf("package" to packageName))
            }
        } catch (e: Exception) {
            ToolResult.Failure("EXECUTION_ERROR", e.message ?: "Failed to open application")
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/tools/OpenUrlTool.kt", """package com.orbit.assistant.domain.tools

import android.content.Context
import android.content.Intent
import android.net.Uri
import com.orbit.assistant.domain.model.ToolResult
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonObject

class OpenUrlTool(private val context: Context) : OrbitTool {
    override val name: String = "open_url"
    override val description: String = "Opens a verified web URL in the device's browser using Android ACTION_VIEW intent."
    override val parametersSchema: JsonObject = buildJsonObject {
        put("type", "object")
        putJsonObject("properties") {
            putJsonObject("url") {
                put("type", "string")
                put("description", "The web URL starting with http:// or https://")
            }
        }
        put("required", kotlinx.serialization.json.buildJsonArray {
            add(kotlinx.serialization.json.JsonPrimitive("url"))
        })
    }

    override suspend fun execute(argumentsJson: String): ToolResult {
        return try {
            val jsonElement = Json.parseToJsonElement(argumentsJson).jsonObject
            val urlString = jsonElement["url"]?.jsonPrimitive?.content?.trim()
                ?: return ToolResult.Failure("INVALID_ARGUMENTS", "url is required")

            if (!urlString.startsWith("http://") && !urlString.startsWith("https://")) {
                return ToolResult.Failure("INVALID_PROTOCOL", "URL must start with http:// or https://")
            }

            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(urlString)).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(intent)
            ToolResult.Success("Opened URL: $urlString", mapOf("url" to urlString))
        } catch (e: Exception) {
            ToolResult.Failure("EXECUTION_ERROR", e.message ?: "Failed to open URL")
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/tools/GetCurrentTimeTool.kt", """package com.orbit.assistant.domain.tools

import com.orbit.assistant.domain.model.ToolResult
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.buildJsonObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

class GetCurrentTimeTool : OrbitTool {
    override val name: String = "get_current_time"
    override val description: String = "Retrieves the current accurate device local date, time, and timezone."
    override val parametersSchema: JsonObject = buildJsonObject {
        put("type", "object")
        put("properties", buildJsonObject {})
    }

    override suspend fun execute(argumentsJson: String): ToolResult {
        val now = Date()
        val format = SimpleDateFormat("EEEE, MMMM d, yyyy 'at' hh:mm:ss a z", Locale.getDefault())
        val formatted = format.format(now)
        val tz = TimeZone.getDefault().id
        return ToolResult.Success(
            "Current device time: $formatted ($tz)",
            mapOf("time" to formatted, "timezone" to tz)
        )
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/tools/SearchWebTool.kt", """package com.orbit.assistant.domain.tools

import android.app.SearchManager
import android.content.Context
import android.content.Intent
import com.orbit.assistant.domain.model.ToolResult
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonObject

class SearchWebTool(private val context: Context) : OrbitTool {
    override val name: String = "search_web"
    override val description: String = "Performs a web search using the device default search engine provider."
    override val parametersSchema: JsonObject = buildJsonObject {
        put("type", "object")
        putJsonObject("properties") {
            putJsonObject("query") {
                put("type", "string")
                put("description", "The search query string")
            }
        }
        put("required", kotlinx.serialization.json.buildJsonArray {
            add(kotlinx.serialization.json.JsonPrimitive("query"))
        })
    }

    override suspend fun execute(argumentsJson: String): ToolResult {
        return try {
            val jsonElement = Json.parseToJsonElement(argumentsJson).jsonObject
            val query = jsonElement["query"]?.jsonPrimitive?.content?.trim()
                ?: return ToolResult.Failure("INVALID_ARGUMENTS", "query is required")

            val intent = Intent(Intent.ACTION_WEB_SEARCH).apply {
                putExtra(SearchManager.QUERY, query)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(intent)
            ToolResult.Success("Launched web search for: \\"$query\\"", mapOf("query" to query))
        } catch (e: Exception) {
            ToolResult.Failure("EXECUTION_ERROR", e.message ?: "Failed to perform web search")
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/domain/engine/OrbitEngine.kt", """package com.orbit.assistant.domain.engine

import com.orbit.assistant.domain.model.ConversationMessage
import com.orbit.assistant.domain.model.OrbitState
import kotlinx.coroutines.flow.StateFlow

interface OrbitEngine {
    val currentState: StateFlow<OrbitState>
    val conversation: StateFlow<List<ConversationMessage>>
    val isOnline: StateFlow<Boolean>

    suspend fun processCommand(userPrompt: String)
    suspend fun clearConversation()
    fun stop()
    suspend fun checkHealth(): Boolean
}
""")

# Data layer
write_file("app/src/main/java/com/orbit/assistant/data/security/AndroidKeystoreSecureStorage.kt", """package com.orbit.assistant.data.security

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import com.orbit.assistant.domain.repository.SecureStorage
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AndroidKeystoreSecureStorage(private val context: Context) : SecureStorage {

    private val masterKey: MasterKey by lazy {
        MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
    }

    private val sharedPreferences: SharedPreferences by lazy {
        try {
            EncryptedSharedPreferences.create(
                context,
                "orbit_secure_vault",
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
        } catch (e: Exception) {
            context.getSharedPreferences("orbit_secure_vault", Context.MODE_PRIVATE).edit().clear().apply()
            EncryptedSharedPreferences.create(
                context,
                "orbit_secure_vault",
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
        }
    }

    companion object {
        private const val KEY_OMNIROUTE_API_KEY = "k_omniroute_secret_token"
    }

    override suspend fun getApiKey(): String? = withContext(Dispatchers.IO) {
        sharedPreferences.getString(KEY_OMNIROUTE_API_KEY, null)?.takeIf { it.isNotBlank() }
    }

    override suspend fun saveApiKey(apiKey: String) = withContext(Dispatchers.IO) {
        sharedPreferences.edit()
            .putString(KEY_OMNIROUTE_API_KEY, apiKey.trim())
            .apply()
    }

    override suspend fun clearApiKey() = withContext(Dispatchers.IO) {
        sharedPreferences.edit()
            .remove(KEY_OMNIROUTE_API_KEY)
            .apply()
    }

    override suspend fun hasApiKey(): Boolean = withContext(Dispatchers.IO) {
        val key = sharedPreferences.getString(KEY_OMNIROUTE_API_KEY, null)
        !key.isNullOrBlank()
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/data/remote/OmniRouteClient.kt", """package com.orbit.assistant.data.remote

import com.orbit.assistant.domain.model.ChatCompletionRequest
import com.orbit.assistant.domain.model.ChatCompletionResponse
import com.orbit.assistant.domain.model.OmniRouteModelsResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.net.ConnectException
import java.net.SocketTimeoutException
import java.util.concurrent.TimeUnit

sealed class OmniRouteException(message: String, cause: Throwable? = null) : Exception(message, cause) {
    class NotRunning(cause: Throwable? = null) : OmniRouteException("OmniRoute is not running or unreachable at local endpoint.", cause)
    class InvalidApiKey : OmniRouteException("Invalid OmniRoute API key. Authorization rejected.")
    class ModelUnavailable(val modelName: String) : OmniRouteException("Model '$modelName' is currently unavailable on OmniRoute.")
    class ConnectionTimeout(cause: Throwable? = null) : OmniRouteException("Connection to OmniRoute timed out.", cause)
    class GenericError(message: String, cause: Throwable? = null) : OmniRouteException(message, cause)
}

class OmniRouteClient(
    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build(),
    private val json: Json = Json {
        ignoreUnknownKeys = true
        encodeDefaults = true
        isLenient = true
    }
) {
    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    suspend fun getModels(baseUrl: String, apiKey: String?): Result<List<String>> = withContext(Dispatchers.IO) {
        val sanitizedBase = baseUrl.trimEnd('/')
        val url = "$sanitizedBase/models"
        val requestBuilder = Request.Builder()
            .url(url)
            .get()

        if (!apiKey.isNullOrBlank()) {
            requestBuilder.header("Authorization", "Bearer $apiKey")
        }

        val request = requestBuilder.build()
        try {
            val response = client.newCall(request).execute()
            response.use { res ->
                if (res.code == 401 || res.code == 403) {
                    return@withContext Result.failure(OmniRouteException.InvalidApiKey())
                }
                if (!res.isSuccessful) {
                    val errBody = res.body?.string() ?: ""
                    return@withContext Result.failure(
                        OmniRouteException.GenericError("HTTP ${res.code}: $errBody")
                    )
                }
                val responseBody = res.body?.string() ?: ""
                val modelsResponse = json.decodeFromString<OmniRouteModelsResponse>(responseBody)
                val modelList = modelsResponse.data.map { it.id }.sorted()
                Result.success(modelList)
            }
        } catch (e: ConnectException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: SocketTimeoutException) {
            Result.failure(OmniRouteException.ConnectionTimeout(e))
        } catch (e: IOException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: Exception) {
            Result.failure(OmniRouteException.GenericError(e.localizedMessage ?: "Unknown network error", e))
        }
    }

    suspend fun createChatCompletion(
        baseUrl: String,
        apiKey: String?,
        requestData: ChatCompletionRequest
    ): Result<ChatCompletionResponse> = withContext(Dispatchers.IO) {
        val sanitizedBase = baseUrl.trimEnd('/')
        val url = "$sanitizedBase/chat/completions"
        val requestJson = json.encodeToString(ChatCompletionRequest.serializer(), requestData)
        val body = requestJson.toRequestBody(jsonMediaType)

        val requestBuilder = Request.Builder()
            .url(url)
            .post(body)

        if (!apiKey.isNullOrBlank()) {
            requestBuilder.header("Authorization", "Bearer $apiKey")
        }

        val request = requestBuilder.build()
        try {
            val response = client.newCall(request).execute()
            response.use { res ->
                if (res.code == 401 || res.code == 403) {
                    return@withContext Result.failure(OmniRouteException.InvalidApiKey())
                }
                if (res.code == 404) {
                    return@withContext Result.failure(OmniRouteException.ModelUnavailable(requestData.model))
                }
                if (!res.isSuccessful) {
                    val errBody = res.body?.string() ?: ""
                    return@withContext Result.failure(
                        OmniRouteException.GenericError("HTTP ${res.code}: $errBody")
                    )
                }
                val responseBody = res.body?.string() ?: ""
                val chatResponse = json.decodeFromString<ChatCompletionResponse>(responseBody)
                Result.success(chatResponse)
            }
        } catch (e: ConnectException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: SocketTimeoutException) {
            Result.failure(OmniRouteException.ConnectionTimeout(e))
        } catch (e: IOException) {
            Result.failure(OmniRouteException.NotRunning(e))
        } catch (e: Exception) {
            Result.failure(OmniRouteException.GenericError(e.localizedMessage ?: "Chat completion error", e))
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/data/repository/ActivityRepositoryImpl.kt", """package com.orbit.assistant.data.repository

import com.orbit.assistant.domain.model.ActionItem
import com.orbit.assistant.domain.model.ActionStatus
import com.orbit.assistant.domain.repository.ActivityRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ActivityRepositoryImpl : ActivityRepository {
    private val _actions = MutableStateFlow(createInitialActions())
    override val actions: StateFlow<List<ActionItem>> = _actions.asStateFlow()

    private fun createInitialActions(): List<ActionItem> {
        return listOf(
            ActionItem(
                id = "act_init_1",
                title = "Device System Ready",
                detail = "Native Android package bindings and ToolRegistry initialized",
                timestamp = SimpleDateFormat("hh:mm a", Locale.getDefault()).format(Date()),
                section = "Today",
                status = ActionStatus.COMPLETED
            )
        )
    }

    override suspend fun recordAction(action: ActionItem) {
        val currentList = _actions.value.toMutableList()
        currentList.add(0, action)
        _actions.value = currentList
    }

    override suspend fun clearHistory() {
        _actions.value = emptyList()
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/data/repository/SettingsRepositoryImpl.kt", """package com.orbit.assistant.data.repository

import android.content.Context
import android.content.SharedPreferences
import com.orbit.assistant.data.remote.OmniRouteClient
import com.orbit.assistant.domain.model.AnimationIntensity
import com.orbit.assistant.domain.model.ResponseStyle
import com.orbit.assistant.domain.model.SettingsState
import com.orbit.assistant.domain.repository.SecureStorage
import com.orbit.assistant.domain.repository.SettingsRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class SettingsRepositoryImpl(
    private val context: Context,
    private val secureStorage: SecureStorage,
    private val omniRouteClient: OmniRouteClient,
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.IO)
) : SettingsRepository {

    private val prefs: SharedPreferences = context.getSharedPreferences("orbit_preferences", Context.MODE_PRIVATE)
    private val _settingsState = MutableStateFlow(loadInitialSettings())
    override val settingsState: StateFlow<SettingsState> = _settingsState.asStateFlow()

    init {
        scope.launch {
            val hasKey = secureStorage.hasApiKey()
            _settingsState.value = _settingsState.value.copy(
                hasApiKey = hasKey,
                apiKeyMasked = if (hasKey) "••••••••" else ""
            )
        }
    }

    private fun loadInitialSettings(): SettingsState {
        val url = prefs.getString("omniroute_url", "http://127.0.0.1:20128/v1") ?: "http://127.0.0.1:20128/v1"
        val model = prefs.getString("selected_model", "Auto") ?: "Auto"
        val intensityStr = prefs.getString("anim_intensity", AnimationIntensity.MEDIUM.name)
        val intensity = try { AnimationIntensity.valueOf(intensityStr!!) } catch (e: Exception) { AnimationIntensity.MEDIUM }
        val responseStyleStr = prefs.getString("response_style", ResponseStyle.CONCISE.name)
        val style = try { ResponseStyle.valueOf(responseStyleStr!!) } catch (e: Exception) { ResponseStyle.CONCISE }

        return SettingsState(
            omniRouteUrl = url,
            selectedModel = model,
            animationIntensity = intensity,
            responseStyle = style,
            voiceEnabled = prefs.getBoolean("voice_enabled", true),
            textToSpeech = prefs.getBoolean("tts_enabled", true),
            confirmationMode = prefs.getBoolean("confirmation_mode", true),
            memoryEnabled = prefs.getBoolean("memory_enabled", true),
            maxAgentSteps = prefs.getInt("max_agent_steps", 10),
            debugLogging = prefs.getBoolean("debug_logging", false)
        )
    }

    override suspend fun updateSettings(transform: (SettingsState) -> SettingsState) = withContext(Dispatchers.IO) {
        val updated = transform(_settingsState.value)
        _settingsState.value = updated
        prefs.edit()
            .putString("omniroute_url", updated.omniRouteUrl)
            .putString("selected_model", updated.selectedModel)
            .putString("anim_intensity", updated.animationIntensity.name)
            .putString("response_style", updated.responseStyle.name)
            .putBoolean("voice_enabled", updated.voiceEnabled)
            .putBoolean("tts_enabled", updated.textToSpeech)
            .putBoolean("confirmation_mode", updated.confirmationMode)
            .putBoolean("memory_enabled", updated.memoryEnabled)
            .putInt("max_agent_steps", updated.maxAgentSteps)
            .putBoolean("debug_logging", updated.debugLogging)
            .apply()
    }

    override suspend fun saveApiKey(apiKey: String) = withContext(Dispatchers.IO) {
        if (apiKey.isBlank()) {
            secureStorage.clearApiKey()
            updateSettings { it.copy(hasApiKey = false, apiKeyMasked = "") }
        } else {
            secureStorage.saveApiKey(apiKey)
            updateSettings { it.copy(hasApiKey = true, apiKeyMasked = "••••••••") }
        }
    }

    override suspend fun getApiKey(): String? = secureStorage.getApiKey()

    override suspend fun testOmniRouteConnection(): Result<Pair<Int, List<String>>> = withContext(Dispatchers.IO) {
        val currentSettings = _settingsState.value
        val startTime = System.currentTimeMillis()
        val apiKey = secureStorage.getApiKey()
        val modelsResult = omniRouteClient.getModels(currentSettings.omniRouteUrl, apiKey)
        val latency = (System.currentTimeMillis() - startTime).toInt()

        modelsResult.fold(
            onSuccess = { models ->
                val combined = listOf("Auto") + models
                val updatedStatus = "Connected (${latency}ms latency)"
                updateSettings { prev ->
                    prev.copy(
                        availableModels = combined,
                        connectionStatus = updatedStatus
                    )
                }
                Result.success(Pair(latency, combined))
            },
            onFailure = { err ->
                val failStatus = err.message ?: "Connection failed"
                updateSettings { prev ->
                    prev.copy(connectionStatus = failStatus)
                }
                Result.failure(err)
            }
        )
    }
}
""")

print("Part 1 written successfully.")
