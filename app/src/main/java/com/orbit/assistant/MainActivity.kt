package com.orbit.assistant

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.compose.rememberNavController
import com.orbit.assistant.ui.navigation.OrbitNavGraph
import com.orbit.assistant.ui.screens.activity.ActivityViewModel
import com.orbit.assistant.ui.screens.chat.ChatViewModel
import com.orbit.assistant.ui.screens.home.HomeViewModel
import com.orbit.assistant.ui.screens.permissions.PermissionViewModel
import com.orbit.assistant.ui.screens.settings.SettingsViewModel
import com.orbit.assistant.ui.theme.OrbitTheme

class MainActivity : ComponentActivity() {

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { _ ->
        permissionViewModel.refreshPermissions()
    }

    private val app by lazy { application as OrbitApplication }

    private val homeViewModel: HomeViewModel by viewModels {
        object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return HomeViewModel(
                    orbitEngine = app.orbitEngine,
                    settingsRepository = app.settingsRepository,
                    speechRecognizer = app.speechRecognizer
                ) as T
            }
        }
    }

    private val chatViewModel: ChatViewModel by viewModels {
        object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return ChatViewModel(app.orbitEngine) as T
            }
        }
    }

    private val activityViewModel: ActivityViewModel by viewModels {
        object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return ActivityViewModel(app.activityRepository) as T
            }
        }
    }

    private val settingsViewModel: SettingsViewModel by viewModels {
        object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return SettingsViewModel(app.settingsRepository) as T
            }
        }
    }

    private val permissionViewModel: PermissionViewModel by viewModels {
        object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return PermissionViewModel(this@MainActivity) as T
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            OrbitTheme {
                val navController = rememberNavController()
                OrbitNavGraph(
                    navController = navController,
                    homeViewModel = homeViewModel,
                    chatViewModel = chatViewModel,
                    activityViewModel = activityViewModel,
                    settingsViewModel = settingsViewModel,
                    permissionViewModel = permissionViewModel,
                    onRequestPermission = { permission ->
                        permissionLauncher.launch(permission)
                    }
                )
            }
        }
    }

    override fun onResume() {
        super.onResume()
        permissionViewModel.refreshPermissions()
    }
}
