package com.orbit.assistant.domain.engine

import com.orbit.assistant.domain.model.ConversationMessage
import com.orbit.assistant.domain.model.OrbitState
import kotlinx.coroutines.flow.StateFlow

interface OrbitEngine {
    val currentState: StateFlow<OrbitState>
    val conversation: StateFlow<List<ConversationMessage>>
    val isOnline: StateFlow<Boolean>

    suspend fun processCommand(userPrompt: String)
    suspend fun clearConversation()
    fun stop()
    suspend fun checkHealth(): Boolean
}
