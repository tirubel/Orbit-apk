package com.orbit.assistant.domain.repository

import com.orbit.assistant.domain.model.SettingsState
import kotlinx.coroutines.flow.StateFlow

interface SettingsRepository {
    val settingsState: StateFlow<SettingsState>
    suspend fun updateSettings(transform: (SettingsState) -> SettingsState)
    suspend fun saveApiKey(apiKey: String)
    suspend fun getApiKey(): String?
    suspend fun testOmniRouteConnection(): Result<Pair<Int, List<String>>> // Returns (latencyMs, models)
}
