package com.orbit.assistant.domain.model

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
