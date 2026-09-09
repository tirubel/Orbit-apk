package com.orbit.assistant.domain.repository

import com.orbit.assistant.domain.model.ActionItem
import kotlinx.coroutines.flow.StateFlow

interface ActivityRepository {
    val actions: StateFlow<List<ActionItem>>
    suspend fun recordAction(action: ActionItem)
    suspend fun clearHistory()
}
