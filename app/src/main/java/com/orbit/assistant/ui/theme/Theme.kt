package com.orbit.assistant.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val DarkColorScheme = darkColorScheme(
    primary = OrbitCyanAccent,
    secondary = OrbitIndigoAccent,
    tertiary = OrbitOnlineGreen,
    background = OrbitDeepVoid,
    surface = OrbitSpaceSurface,
    onPrimary = OrbitDeepVoid,
    onSecondary = OrbitTextPrimary,
    onTertiary = OrbitDeepVoid,
    onBackground = OrbitTextPrimary,
    onSurface = OrbitTextPrimary,
    error = OrbitErrorRed,
    onError = OrbitDeepVoid
)

@Composable
fun OrbitTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        typography = Typography,
        content = content
    )
}
