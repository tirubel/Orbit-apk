package com.orbit.assistant.domain.tools

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
