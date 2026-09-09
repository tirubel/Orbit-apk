package com.orbit.assistant.ui.screens.permissions

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModel
import com.orbit.assistant.domain.model.PermissionItem
import com.orbit.assistant.service.OrbitAccessibilityService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class PermissionViewModel(
    private val context: Context
) : ViewModel() {

    private val _permissions = MutableStateFlow(checkRealPermissions())
    val permissions: StateFlow<List<PermissionItem>> = _permissions.asStateFlow()

    fun refreshPermissions() {
        _permissions.value = checkRealPermissions()
    }

    private fun checkRealPermissions(): List<PermissionItem> {
        val hasMic = ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED

        val hasNotifications = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            true
        }

        val hasAccessibility = OrbitAccessibilityService.isServiceRunning

        return listOf(
            PermissionItem(
                id = "perm_mic",
                title = "Microphone Access (RECORD_AUDIO)",
                description = "Required for Android SpeechRecognizer audio streaming and voice commands.",
                isGranted = hasMic,
                isRequired = true
            ),
            PermissionItem(
                id = "perm_accessibility",
                title = "Accessibility Synergy Service",
                description = "Enables Orbit to coordinate device workflows and launch applications safely.",
                isGranted = hasAccessibility,
                isRequired = true
            ),
            PermissionItem(
                id = "perm_notifications",
                title = "Notifications (POST_NOTIFICATIONS)",
                description = "Provides asynchronous telemetry when multi-step agent actions complete.",
                isGranted = hasNotifications,
                isRequired = false
            )
        )
    }

    fun openAccessibilitySettings() {
        val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
    }

    fun openAppSettings() {
        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.fromParts("package", context.packageName, null)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
    }
}
