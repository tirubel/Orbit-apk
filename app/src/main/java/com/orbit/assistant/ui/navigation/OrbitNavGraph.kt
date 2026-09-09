package com.orbit.assistant.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.orbit.assistant.ui.screens.activity.ActivityScreen
import com.orbit.assistant.ui.screens.activity.ActivityViewModel
import com.orbit.assistant.ui.screens.chat.ChatScreen
import com.orbit.assistant.ui.screens.chat.ChatViewModel
import com.orbit.assistant.ui.screens.home.HomeScreen
import com.orbit.assistant.ui.screens.home.HomeViewModel
import com.orbit.assistant.ui.screens.onboarding.OnboardingScreen
import com.orbit.assistant.ui.screens.permissions.PermissionCenterScreen
import com.orbit.assistant.ui.screens.permissions.PermissionViewModel
import com.orbit.assistant.ui.screens.settings.SettingsScreen
import com.orbit.assistant.ui.screens.settings.SettingsViewModel

@Composable
fun OrbitNavGraph(
    navController: NavHostController,
    homeViewModel: HomeViewModel,
    chatViewModel: ChatViewModel,
    activityViewModel: ActivityViewModel,
    settingsViewModel: SettingsViewModel,
    permissionViewModel: PermissionViewModel,
    onRequestPermission: (String) -> Unit,
    startDestination: String = Screen.Home.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(Screen.Onboarding.route) {
            OnboardingScreen(
                onComplete = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Onboarding.route) { inclusive = true }
                    }
                }
            )
        }
        composable(Screen.Home.route) {
            HomeScreen(
                viewModel = homeViewModel,
                onNavigate = { route ->
                    if (route != Screen.Home.route) {
                        navController.navigate(route)
                    }
                }
            )
        }
        composable(Screen.Chat.route) {
            ChatScreen(
                viewModel = chatViewModel,
                onNavigate = { route ->
                    navController.navigate(route) {
                        popUpTo(Screen.Home.route)
                    }
                }
            )
        }
        composable(Screen.Activity.route) {
            ActivityScreen(
                viewModel = activityViewModel,
                onNavigate = { route ->
                    navController.navigate(route) {
                        popUpTo(Screen.Home.route)
                    }
                }
            )
        }
        composable(Screen.Settings.route) {
            SettingsScreen(
                viewModel = settingsViewModel,
                onNavigate = { route ->
                    navController.navigate(route) {
                        popUpTo(Screen.Home.route)
                    }
                }
            )
        }
        composable(Screen.Permissions.route) {
            PermissionCenterScreen(
                viewModel = permissionViewModel,
                onRequestPermission = onRequestPermission,
                onNavigate = { route ->
                    navController.navigate(route) {
                        popUpTo(Screen.Home.route)
                    }
                }
            )
        }
    }
}
