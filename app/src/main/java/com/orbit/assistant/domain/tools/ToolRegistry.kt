package com.orbit.assistant.domain.tools

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
