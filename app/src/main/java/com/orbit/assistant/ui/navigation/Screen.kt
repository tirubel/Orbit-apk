package com.orbit.assistant.ui.navigation

sealed class Screen(val route: String) {
    object Onboarding : Screen("onboarding")
    object Home : Screen("home")
    object Chat : Screen("chat")
    object Activity : Screen("activity")
    object Settings : Screen("settings")
    object Permissions : Screen("permissions")
}
