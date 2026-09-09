package com.orbit.assistant.data.repository

import android.content.Context
import android.content.SharedPreferences
import com.orbit.assistant.data.remote.OmniRouteClient
import com.orbit.assistant.domain.model.AnimationIntensity
import com.orbit.assistant.domain.model.ResponseStyle
import com.orbit.assistant.domain.model.SettingsState
import com.orbit.assistant.domain.repository.SecureStorage
import com.orbit.assistant.domain.repository.SettingsRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class SettingsRepositoryImpl(
    private val context: Context,
    private val secureStorage: SecureStorage,
    private val omniRouteClient: OmniRouteClient,
    private val scope: CoroutineScope = CoroutineScope(Dispatchers.IO)
) : SettingsRepository {

    private val prefs: SharedPreferences = context.getSharedPreferences("orbit_preferences", Context.MODE_PRIVATE)
    private val _settingsState = MutableStateFlow(loadInitialSettings())
    override val settingsState: StateFlow<SettingsState> = _settingsState.asStateFlow()

    init {
        scope.launch {
            val hasKey = secureStorage.hasApiKey()
            _settingsState.value = _settingsState.value.copy(
                hasApiKey = hasKey,
                apiKeyMasked = if (hasKey) "••••••••" else ""
            )
        }
    }

    private fun loadInitialSettings(): SettingsState {
        val url = prefs.getString("omniroute_url", "http://127.0.0.1:20128/v1") ?: "http://127.0.0.1:20128/v1"
        val model = prefs.getString("selected_model", "Auto") ?: "Auto"
        val intensityStr = prefs.getString("anim_intensity", AnimationIntensity.MEDIUM.name)
        val intensity = try { AnimationIntensity.valueOf(intensityStr!!) } catch (e: Exception) { AnimationIntensity.MEDIUM }
        val responseStyleStr = prefs.getString("response_style", ResponseStyle.CONCISE.name)
        val style = try { ResponseStyle.valueOf(responseStyleStr!!) } catch (e: Exception) { ResponseStyle.CONCISE }

        return SettingsState(
            omniRouteUrl = url,
            selectedModel = model,
            animationIntensity = intensity,
            responseStyle = style,
            voiceEnabled = prefs.getBoolean("voice_enabled", true),
            textToSpeech = prefs.getBoolean("tts_enabled", true),
            confirmationMode = prefs.getBoolean("confirmation_mode", true),
            memoryEnabled = prefs.getBoolean("memory_enabled", true),
            maxAgentSteps = prefs.getInt("max_agent_steps", 10),
            debugLogging = prefs.getBoolean("debug_logging", false)
        )
    }

    override suspend fun updateSettings(transform: (SettingsState) -> SettingsState) = withContext(Dispatchers.IO) {
        val updated = transform(_settingsState.value)
        _settingsState.value = updated
        prefs.edit()
            .putString("omniroute_url", updated.omniRouteUrl)
            .putString("selected_model", updated.selectedModel)
            .putString("anim_intensity", updated.animationIntensity.name)
            .putString("response_style", updated.responseStyle.name)
            .putBoolean("voice_enabled", updated.voiceEnabled)
            .putBoolean("tts_enabled", updated.textToSpeech)
            .putBoolean("confirmation_mode", updated.confirmationMode)
            .putBoolean("memory_enabled", updated.memoryEnabled)
            .putInt("max_agent_steps", updated.maxAgentSteps)
            .putBoolean("debug_logging", updated.debugLogging)
            .apply()
    }

    override suspend fun saveApiKey(apiKey: String) = withContext(Dispatchers.IO) {
        if (apiKey.isBlank()) {
            secureStorage.clearApiKey()
            updateSettings { it.copy(hasApiKey = false, apiKeyMasked = "") }
        } else {
            secureStorage.saveApiKey(apiKey)
            updateSettings { it.copy(hasApiKey = true, apiKeyMasked = "••••••••") }
        }
    }

    override suspend fun getApiKey(): String? = secureStorage.getApiKey()

    override suspend fun testOmniRouteConnection(): Result<Pair<Int, List<String>>> = withContext(Dispatchers.IO) {
        val currentSettings = _settingsState.value
        val startTime = System.currentTimeMillis()
        val apiKey = secureStorage.getApiKey()
        val modelsResult = omniRouteClient.getModels(currentSettings.omniRouteUrl, apiKey)
        val latency = (System.currentTimeMillis() - startTime).toInt()

        modelsResult.fold(
            onSuccess = { models ->
                val combined = listOf("Auto") + models
                val updatedStatus = "Connected (${latency}ms latency)"
                updateSettings { prev ->
                    prev.copy(
                        availableModels = combined,
                        connectionStatus = updatedStatus
                    )
                }
                Result.success(Pair(latency, combined))
            },
            onFailure = { err ->
                val failStatus = err.message ?: "Connection failed"
                updateSettings { prev ->
                    prev.copy(connectionStatus = failStatus)
                }
                Result.failure(err)
            }
        )
    }
}
