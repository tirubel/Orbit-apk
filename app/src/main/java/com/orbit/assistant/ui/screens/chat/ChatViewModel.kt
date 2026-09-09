package com.orbit.assistant.ui.screens.chat

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.model.ConversationMessage
import com.orbit.assistant.domain.model.OrbitState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ChatViewModel(
    private val orbitEngine: OrbitEngine
) : ViewModel() {

    val conversation: StateFlow<List<ConversationMessage>> = orbitEngine.conversation
    val currentState: StateFlow<OrbitState> = orbitEngine.currentState

    private val _inputText = MutableStateFlow("")
    val inputText: StateFlow<String> = _inputText.asStateFlow()

    fun updateInputText(text: String) {
        _inputText.value = text
    }

    fun sendMessage() {
        val query = _inputText.value.trim()
        if (query.isNotBlank()) {
            _inputText.value = ""
            viewModelScope.launch {
                orbitEngine.processCommand(query)
            }
        }
    }

    fun clearChat() {
        viewModelScope.launch {
            orbitEngine.clearConversation()
        }
    }
}
