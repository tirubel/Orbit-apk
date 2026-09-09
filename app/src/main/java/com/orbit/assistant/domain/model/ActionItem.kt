package com.orbit.assistant.domain.model

enum class ActionStatus {
    COMPLETED,
    FAILED,
    IN_PROGRESS
}

data class ActionItem(
    val id: String,
    val title: String,
    val detail: String,
    val timestamp: String,
    val section: String = "Today",
    val status: ActionStatus = ActionStatus.COMPLETED
)
