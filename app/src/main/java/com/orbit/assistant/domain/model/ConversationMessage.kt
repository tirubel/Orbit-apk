package com.orbit.assistant.domain.model

enum class MessageSender {
    USER,
    ORBIT
}

data class ActionCardData(
    val title: String,
    val detail: String,
    val statusText: String,
    val isSuccess: Boolean
)

data class ConversationMessage(
    val id: String,
    val sender: MessageSender,
    val text: String,
    val timestamp: Long = System.currentTimeMillis(),
    val actionCard: ActionCardData? = null
)
