package com.orbit.assistant.domain.model

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
