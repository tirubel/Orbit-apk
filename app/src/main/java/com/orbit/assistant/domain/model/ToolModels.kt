package com.orbit.assistant.domain.model

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
            is Success -> """{"success": true, "message": "$message"}"""
            is Failure -> """{"success": false, "error": "$error"${'$'}{details?.let { """, "details": "$it"""" } ?: ""}}"""
        }
    }
}
