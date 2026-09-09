package com.orbit.assistant.domain.model

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
