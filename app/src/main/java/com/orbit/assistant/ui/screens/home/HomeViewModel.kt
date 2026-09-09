package com.orbit.assistant.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.domain.repository.SettingsRepository
import com.orbit.assistant.service.voice.OrbitSpeechRecognizer
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class HomeViewModel(
    private val orbitEngine: OrbitEngine,
    private val settingsRepository: SettingsRepository,
    private val speechRecognizer: OrbitSpeechRecognizer
) : ViewModel() {

    val orbitState: StateFlow<OrbitState> = orbitEngine.currentState
    val isOnline: StateFlow<Boolean> = orbitEngine.isOnline
    val selectedModel: StateFlow<String> = settingsRepository.settingsState
        .map { it.selectedModel }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "Auto")

    val animationIntensity = settingsRepository.settingsState
        .map { it.animationIntensity }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), com.orbit.assistant.domain.model.AnimationIntensity.MEDIUM)

    private val _inputQuery = MutableStateFlow("")
    val inputQuery: StateFlow<String> = _inputQuery.asStateFlow()

    fun updateInputQuery(text: String) {
        _inputQuery.value = text
    }

    fun submitTextCommand() {
        val query = _inputQuery.value.trim()
        if (query.isNotBlank()) {
            _inputQuery.value = ""
            viewModelScope.launch {
                orbitEngine.processCommand(query)
            }
        }
    }

    fun toggleVoiceInput() {
        val currentState = orbitEngine.currentState.value
        if (currentState == OrbitState.LISTENING) {
            speechRecognizer.stopListening()
            orbitEngine.stop()
        } else {
            speechRecognizer.startListening { spokenText ->
                viewModelScope.launch {
                    orbitEngine.processCommand(spokenText)
                }
            }
        }
    }
}
