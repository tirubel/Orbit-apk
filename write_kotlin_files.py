import os

files = {}

# 1. Models
files["app/src/main/java/com/orbit/assistant/domain/model/OrbitState.kt"] = """package com.orbit.assistant.domain.model

enum class OrbitState(val label: String, val subtitle: String) {
    IDLE("Ready", "How can I help?"),
    CONNECTING("Connecting...", "Establishing OmniRoute link"),
    LISTENING("Listening...", "Say something to Orbit"),
    THINKING("Thinking...", "Analyzing context & intent"),
    EXECUTING("Working...", "Executing requested action"),
    SPEAKING("Speaking...", "Orbit voice output active"),
    ERROR("Alert", "Something went wrong"),
    OFFLINE("Orbit is Offline", "OmniRoute service unreachable")
}

data class OrbitUiState(
    val state: OrbitState = OrbitState.IDLE,
    val isOnline: Boolean = true,
    val currentTaskDescription: String? = null,
    val activeQuery: String = "",
    val errorMessage: String? = null
)
"""

files["app/src/main/java/com/orbit/assistant/domain/model/ActionItem.kt"] = """package com.orbit.assistant.domain.model

enum class ActionStatus {
    COMPLETED,
    FAILED,
    IN_PROGRESS
}

data class ActionItem(
    val id: String,
    val title: String,
    val detail: String,
    val timestamp: String,
    val section: String = "Today",
    val status: ActionStatus = ActionStatus.COMPLETED
)
"""

files["app/src/main/java/com/orbit/assistant/domain/model/ConversationMessage.kt"] = """package com.orbit.assistant.domain.model

enum class MessageSender {
    USER,
    ORBIT
}

data class ActionCardData(
    val title: String,
    val detail: String,
    val statusText: String,
    val isSuccess: Boolean
)

data class ConversationMessage(
    val id: String,
    val sender: MessageSender,
    val text: String,
    val timestamp: Long = System.currentTimeMillis(),
    val actionCard: ActionCardData? = null
)
"""

files["app/src/main/java/com/orbit/assistant/domain/model/PermissionItem.kt"] = """package com.orbit.assistant.domain.model

data class PermissionItem(
    val id: String,
    val title: String,
    val description: String,
    val isGranted: Boolean,
    val isRequired: Boolean = true
)
"""

files["app/src/main/java/com/orbit/assistant/domain/model/SettingsState.kt"] = """package com.orbit.assistant.domain.model

enum class AnimationIntensity {
    LOW,
    MEDIUM,
    HIGH
}

enum class ResponseStyle {
    CONCISE,
    DETAILED,
    CREATIVE
}

data class SettingsState(
    val assistantName: String = "Orbit",
    val wakeWord: String = "Orbit",
    val voice: String = "Default (Aura Cyan)",
    val responseStyle: ResponseStyle = ResponseStyle.CONCISE,
    val animationIntensity: AnimationIntensity = AnimationIntensity.MEDIUM,
    // OmniRoute Local Gateway
    val omniRouteUrl: String = "http://127.0.0.1:20128/v1",
    val apiKeyMasked: String = "",
    val hasApiKey: Boolean = false,
    val selectedModel: String = "Auto",
    val availableModels: List<String> = listOf("Auto"),
    val connectionStatus: String = "Not connected",
    // Voice & Audio
    val voiceEnabled: Boolean = true,
    val textToSpeech: Boolean = true,
    // Safety & Automation
    val confirmationMode: Boolean = true,
    val memoryEnabled: Boolean = true,
    val maxAgentSteps: Int = 10,
    val debugLogging: Boolean = false
)
"""

files["app/src/main/java/com/orbit/assistant/domain/model/ToolModels.kt"] = """package com.orbit.assistant.domain.model

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
            is Failure -> \"\"\"{"success": false, "error": "$error"${details?.let { """, "details": "$it"""" } ?: ""}}\"\"\"
        }
    }
}
"""

files["app/src/main/java/com/orbit/assistant/domain/model/OmniRouteModels.kt"] = """package com.orbit.assistant.domain.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonObject

@Serializable
data class OmniRouteModelItem(
    val id: String,
    val `object`: String = "model",
    val created: Long = 0,
    @SerialName("owned_by")
    val ownedBy: String = "local"
)

@Serializable
data class OmniRouteModelsResponse(
    val `object`: String = "list",
    val data: List<OmniRouteModelItem> = emptyList()
)

@Serializable
data class ChatFunctionCall(
    val name: String,
    val arguments: String // JSON string
)

@Serializable
data class ChatToolCall(
    val id: String = "call_1",
    val type: String = "function",
    val function: ChatFunctionCall
)

@Serializable
data class ChatCompletionMessage(
    val role: String,
    val content: String? = null,
    val name: String? = null,
    @SerialName("tool_calls")
    val toolCalls: List<ChatToolCall>? = null,
    @SerialName("tool_call_id")
    val toolCallId: String? = null
)

@Serializable
data class ChatCompletionToolFunction(
    val name: String,
    val description: String,
    val parameters: JsonObject
)

@Serializable
data class ChatCompletionTool(
    val type: String = "function",
    val function: ChatCompletionToolFunction
)

@Serializable
data class ChatCompletionRequest(
    val model: String,
    val messages: List<ChatCompletionMessage>,
    val tools: List<ChatCompletionTool>? = null,
    @SerialName("tool_choice")
    val toolChoice: String? = "auto",
    val temperature: Float = 0.7f,
    val max_tokens: Int? = 1024
)

@Serializable
data class ChatCompletionChoice(
    val index: Int = 0,
    val message: ChatCompletionMessage,
    @SerialName("finish_reason")
    val finishReason: String? = null
)

@Serializable
data class ChatCompletionResponse(
    val id: String,
    val `object`: String = "chat.completion",
    val created: Long = 0,
    val model: String,
    val choices: List<ChatCompletionChoice> = emptyList()
)
"""

for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
print("Batch 1 written.")
