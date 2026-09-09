package com.orbit.assistant.ui.screens.activity

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.model.ActionItem
import com.orbit.assistant.domain.repository.ActivityRepository
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ActivityViewModel(
    private val activityRepository: ActivityRepository
) : ViewModel() {

    val actions: StateFlow<List<ActionItem>> = activityRepository.actions

    fun clearAuditLog() {
        viewModelScope.launch {
            activityRepository.clearHistory()
        }
    }
}
