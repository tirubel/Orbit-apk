package com.orbit.assistant.domain.tools

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
            ToolResult.Success("Launched web search for: \"$query\"", mapOf("query" to query))
        } catch (e: Exception) {
            ToolResult.Failure("EXECUTION_ERROR", e.message ?: "Failed to perform web search")
        }
    }
}
