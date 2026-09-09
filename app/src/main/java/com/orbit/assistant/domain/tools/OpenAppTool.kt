package com.orbit.assistant.domain.tools

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

    private val packageNameRegex = Regex("^[a-zA-Z][a-zA-Z0-9_]*(\\.[a-zA-Z][a-zA-Z0-9_]*)+$")

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
