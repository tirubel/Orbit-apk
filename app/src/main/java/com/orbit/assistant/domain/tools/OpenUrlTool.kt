package com.orbit.assistant.domain.tools

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
