package com.orbit.assistant.domain.tools

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
