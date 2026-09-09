package com.orbit.assistant.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.orbit.assistant.ui.components.OrbitBottomNavigation
import com.orbit.assistant.ui.components.OrbitCore
import com.orbit.assistant.ui.components.OrbitMicrophoneButton
import com.orbit.assistant.ui.components.OrbitStatusIndicator
import com.orbit.assistant.ui.components.OrbitTextInput
import com.orbit.assistant.ui.components.getStatePalette
import com.orbit.assistant.ui.navigation.Screen
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun HomeScreen(
    viewModel: HomeViewModel,
    onNavigate: (String) -> Unit
) {
    val state by viewModel.orbitState.collectAsState()
    val isOnline by viewModel.isOnline.collectAsState()
    val modelName by viewModel.selectedModel.collectAsState()
    val intensity by viewModel.animationIntensity.collectAsState()
    val inputQuery by viewModel.inputQuery.collectAsState()

    val quickPrompts = listOf(
        "What time is it?",
        "Open YouTube",
        "What is 25 times 4?",
        "Search Android Jetpack Compose docs"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(OrbitDeepVoid)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 76.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Top Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "ORBIT",
                        style = Typography.titleLarge.copy(color = OrbitCyanAccent)
                    )
                    Text(
                        text = "NATIVE SYSTEM ONLINE",
                        style = Typography.labelSmall.copy(color = OrbitTextMuted)
                    )
                }
                OrbitStatusIndicator(
                    isOnline = isOnline,
                    modelName = modelName
                )
            }

            // Central Core Zone
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
                modifier = Modifier.padding(vertical = 12.dp)
            ) {
                OrbitCore(
                    state = state,
                    intensity = intensity,
                    size = 250.dp,
                    onClick = { viewModel.toggleVoiceInput() }
                )
                Spacer(modifier = Modifier.height(20.dp))
                val palette = getStatePalette(state)
                Text(
                    text = state.label.uppercase(),
                    style = Typography.titleMedium.copy(color = palette.primary)
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = state.subtitle,
                    style = Typography.bodyMedium.copy(color = OrbitTextSecondary)
                )
            }

            // Controls & Quick Action Chips
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(quickPrompts) { prompt ->
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp))
                                .background(OrbitCardSurface)
                                .border(1.dp, OrbitGlassBorder, RoundedCornerShape(20.dp))
                                .clickable {
                                    viewModel.updateInputQuery(prompt)
                                    viewModel.submitTextCommand()
                                }
                                .padding(horizontal = 14.dp, vertical = 8.dp)
                        ) {
                            Text(
                                text = prompt,
                                style = Typography.bodyMedium.copy(color = OrbitTextSecondary)
                            )
                        }
                    }
                }

                OrbitTextInput(
                    value = inputQuery,
                    onValueChange = { viewModel.updateInputQuery(it) },
                    onSend = { viewModel.submitTextCommand() }
                )

                OrbitMicrophoneButton(
                    state = state,
                    onClick = { viewModel.toggleVoiceInput() }
                )
            }
        }

        OrbitBottomNavigation(
            currentRoute = Screen.Home.route,
            onNavigate = onNavigate,
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}
