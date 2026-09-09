package com.orbit.assistant.ui.screens.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.model.AnimationIntensity
import com.orbit.assistant.domain.model.SettingsState
import com.orbit.assistant.domain.repository.SettingsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SettingsViewModel(
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    val settingsState: StateFlow<SettingsState> = settingsRepository.settingsState

    private val _urlInput = MutableStateFlow("http://127.0.0.1:20128/v1")
    val urlInput: StateFlow<String> = _urlInput.asStateFlow()

    private val _apiKeyInput = MutableStateFlow("")
    val apiKeyInput: StateFlow<String> = _apiKeyInput.asStateFlow()

    private val _isTestingConnection = MutableStateFlow(false)
    val isTestingConnection: StateFlow<Boolean> = _isTestingConnection.asStateFlow()

    private val _testResult = MutableStateFlow<String?>(null)
    val testResult: StateFlow<String?> = _testResult.asStateFlow()

    private val _isSuccess = MutableStateFlow(false)
    val isSuccess: StateFlow<Boolean> = _isSuccess.asStateFlow()

    init {
        viewModelScope.launch {
            settingsRepository.settingsState.collect { state ->
                _urlInput.value = state.omniRouteUrl
            }
        }
    }

    fun updateUrl(url: String) {
        _urlInput.value = url
    }

    fun updateApiKey(key: String) {
        _apiKeyInput.value = key
    }

    fun selectModel(model: String) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(selectedModel = model) }
        }
    }

    fun setAnimationIntensity(intensity: AnimationIntensity) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(animationIntensity = intensity) }
        }
    }

    fun toggleVoice(enabled: Boolean) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(voiceEnabled = enabled) }
        }
    }

    fun toggleTts(enabled: Boolean) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(textToSpeech = enabled) }
        }
    }

    fun toggleConfirmation(enabled: Boolean) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(confirmationMode = enabled) }
        }
    }

    fun saveSettings() {
        viewModelScope.launch {
            settingsRepository.updateSettings {
                it.copy(omniRouteUrl = _urlInput.value.trim())
            }
            if (_apiKeyInput.value.isNotBlank()) {
                settingsRepository.saveApiKey(_apiKeyInput.value.trim())
                _apiKeyInput.value = ""
            }
            _testResult.value = "Settings saved to encrypted vault."
            _isSuccess.value = true
        }
    }

    fun testConnection() {
        viewModelScope.launch {
            _isTestingConnection.value = true
            _testResult.value = "Pinging OmniRoute at ${_urlInput.value}..."
            _isSuccess.value = false

            settingsRepository.updateSettings { it.copy(omniRouteUrl = _urlInput.value.trim()) }
            if (_apiKeyInput.value.isNotBlank()) {
                settingsRepository.saveApiKey(_apiKeyInput.value.trim())
                _apiKeyInput.value = ""
            }

            val result = settingsRepository.testOmniRouteConnection()
            _isTestingConnection.value = false
            result.fold(
                onSuccess = { (latency, models) ->
                    _isSuccess.value = true
                    _testResult.value = "OmniRoute Connected (${latency}ms latency). ${models.size - 1} models available."
                },
                onFailure = { err ->
                    _isSuccess.value = false
                    _testResult.value = "Connection Failed: ${err.message ?: "Unknown error"}"
                }
            )
        }
    }
}
