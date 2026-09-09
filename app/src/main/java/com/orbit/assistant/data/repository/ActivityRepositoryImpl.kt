package com.orbit.assistant.data.repository

import com.orbit.assistant.domain.model.ActionItem
import com.orbit.assistant.domain.model.ActionStatus
import com.orbit.assistant.domain.repository.ActivityRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ActivityRepositoryImpl : ActivityRepository {
    private val _actions = MutableStateFlow(createInitialActions())
    override val actions: StateFlow<List<ActionItem>> = _actions.asStateFlow()

    private fun createInitialActions(): List<ActionItem> {
        return listOf(
            ActionItem(
                id = "act_init_1",
                title = "Device System Ready",
                detail = "Native Android package bindings and ToolRegistry initialized",
                timestamp = SimpleDateFormat("hh:mm a", Locale.getDefault()).format(Date()),
                section = "Today",
                status = ActionStatus.COMPLETED
            )
        )
    }

    override suspend fun recordAction(action: ActionItem) {
        val currentList = _actions.value.toMutableList()
        currentList.add(0, action)
        _actions.value = currentList
    }

    override suspend fun clearHistory() {
        _actions.value = emptyList()
    }
}
