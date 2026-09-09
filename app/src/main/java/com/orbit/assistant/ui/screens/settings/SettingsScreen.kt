package com.orbit.assistant.ui.screens.settings

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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.NetworkCheck
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.AnimationIntensity
import com.orbit.assistant.ui.components.GlassCard
import com.orbit.assistant.ui.components.OrbitBottomNavigation
import com.orbit.assistant.ui.navigation.Screen
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitErrorRed
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitIndigoAccent
import com.orbit.assistant.ui.theme.OrbitOnlineGreen
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextPrimary
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun SettingsScreen(
    viewModel: SettingsViewModel,
    onNavigate: (String) -> Unit
) {
    val state by viewModel.settingsState.collectAsState()
    val urlInput by viewModel.urlInput.collectAsState()
    val apiKeyInput by viewModel.apiKeyInput.collectAsState()
    val isTesting by viewModel.isTestingConnection.collectAsState()
    val testResult by viewModel.testResult.collectAsState()
    val isSuccess by viewModel.isSuccess.collectAsState()

    var modelDropdownExpanded by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(OrbitDeepVoid)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 76.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "CORE CONFIGURATION",
                        style = Typography.titleMedium.copy(color = OrbitCyanAccent)
                    )
                    Text(
                        text = "OMNIROUTE & HARDWARE KEYSTORE VAULT",
                        style = Typography.labelSmall.copy(color = OrbitTextMuted)
                    )
                }
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Section 1: OmniRoute Gateway
                GlassCard(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "OMNIROUTE GATEWAY",
                            style = Typography.labelSmall.copy(color = OrbitCyanAccent)
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Text("Gateway Endpoint URL", style = Typography.labelSmall, color = OrbitTextSecondary)
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(OrbitCardSurface)
                                .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                                .padding(12.dp)
                        ) {
                            BasicTextField(
                                value = urlInput,
                                onValueChange = { viewModel.updateUrl(it) },
                                singleLine = true,
                                textStyle = Typography.bodyLarge.copy(color = OrbitTextPrimary),
                                cursorBrush = SolidColor(OrbitCyanAccent),
                                modifier = Modifier.fillMaxWidth()
                            )
                        }

                        Spacer(modifier = Modifier.height(12.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("OmniRoute API Key", style = Typography.labelSmall, color = OrbitTextSecondary)
                            Spacer(modifier = Modifier.width(6.dp))
                            Icon(Icons.Default.Lock, contentDescription = "Keystore secured", tint = OrbitCyanAccent, modifier = Modifier.size(12.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Android Keystore Encrypted", style = Typography.labelSmall, color = OrbitOnlineGreen)
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(OrbitCardSurface)
                                .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                                .padding(12.dp)
                        ) {
                            if (apiKeyInput.isEmpty()) {
                                Text(
                                    text = if (state.hasApiKey) "•••••••• (Encrypted in Keystore)" else "Enter secret API key...",
                                    style = Typography.bodyLarge,
                                    color = if (state.hasApiKey) OrbitTextSecondary else OrbitTextMuted
                                )
                            }
                            BasicTextField(
                                value = apiKeyInput,
                                onValueChange = { viewModel.updateApiKey(it) },
                                singleLine = true,
                                visualTransformation = PasswordVisualTransformation(),
                                textStyle = Typography.bodyLarge.copy(color = OrbitTextPrimary),
                                cursorBrush = SolidColor(OrbitCyanAccent),
                                modifier = Modifier.fillMaxWidth()
                            )
                        }

                        Spacer(modifier = Modifier.height(12.dp))
                        Text("Active Model Architecture", style = Typography.labelSmall, color = OrbitTextSecondary)
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(OrbitCardSurface)
                                .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                                .clickable { modelDropdownExpanded = true }
                                .padding(12.dp)
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(state.selectedModel, style = Typography.bodyLarge, color = OrbitTextPrimary)
                                Icon(Icons.Default.ArrowDropDown, contentDescription = null, tint = OrbitCyanAccent)
                            }

                            DropdownMenu(
                                expanded = modelDropdownExpanded,
                                onDismissRequest = { modelDropdownExpanded = false }
                            ) {
                                state.availableModels.forEach { modelItem ->
                                    DropdownMenuItem(
                                        text = { Text(modelItem) },
                                        onClick = {
                                            viewModel.selectModel(modelItem)
                                            modelDropdownExpanded = false
                                        }
                                    )
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(16.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            Box(
                                contentAlignment = Alignment.Center,
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(OrbitIndigoAccent)
                                    .clickable { viewModel.saveSettings() }
                                    .padding(vertical = 12.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                                ) {
                                    Icon(Icons.Default.Save, contentDescription = null, tint = OrbitTextPrimary, modifier = Modifier.size(16.dp))
                                    Text("SAVE", style = Typography.titleMedium.copy(color = OrbitTextPrimary))
                                }
                            }

                            Box(
                                contentAlignment = Alignment.Center,
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(OrbitCyanAccent)
                                    .clickable(enabled = !isTesting) { viewModel.testConnection() }
                                    .padding(vertical = 12.dp)
                            ) {
                                if (isTesting) {
                                    CircularProgressIndicator(modifier = Modifier.size(18.dp), color = OrbitDeepVoid, strokeWidth = 2.dp)
                                } else {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                                    ) {
                                        Icon(Icons.Default.NetworkCheck, contentDescription = null, tint = OrbitDeepVoid, modifier = Modifier.size(16.dp))
                                        Text("TEST LINK", style = Typography.titleMedium.copy(color = OrbitDeepVoid))
                                    }
                                }
                            }
                        }

                        testResult?.let { resText ->
                            Spacer(modifier = Modifier.height(12.dp))
                            val bannerColor = if (isSuccess) OrbitOnlineGreen else OrbitErrorRed
                            val bgBanner = if (isSuccess) OrbitOnlineGreen.copy(alpha = 0.1f) else OrbitErrorRed.copy(alpha = 0.1f)
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(bgBanner)
                                    .border(1.dp, bannerColor.copy(alpha = 0.4f), RoundedCornerShape(8.dp))
                                    .padding(10.dp)
                            ) {
                                Text(
                                    text = resText,
                                    style = Typography.bodyMedium.copy(color = bannerColor)
                                )
                            }
                        }
                    }
                }

                // Section 2: Voice & Audio
                GlassCard(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "VOICE & AUDIO SYSTEM",
                            style = Typography.labelSmall.copy(color = OrbitCyanAccent)
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text("Speech Recognition (STT)", style = Typography.bodyLarge, color = OrbitTextPrimary)
                                Text("Android SpeechRecognizer service", style = Typography.labelSmall, color = OrbitTextMuted)
                            }
                            Switch(
                                checked = state.voiceEnabled,
                                onCheckedChange = { viewModel.toggleVoice(it) },
                                colors = SwitchDefaults.colors(checkedThumbColor = OrbitCyanAccent)
                            )
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text("Text-to-Speech (TTS)", style = Typography.bodyLarge, color = OrbitTextPrimary)
                                Text("Android TextToSpeech vocalization", style = Typography.labelSmall, color = OrbitTextMuted)
                            }
                            Switch(
                                checked = state.textToSpeech,
                                onCheckedChange = { viewModel.toggleTts(it) },
                                colors = SwitchDefaults.colors(checkedThumbColor = OrbitCyanAccent)
                            )
                        }
                    }
                }

                // Section 3: Visual & Kinetics
                GlassCard(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "KINETIC CANVAS ENGINE",
                            style = Typography.labelSmall.copy(color = OrbitCyanAccent)
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Text("Orbit Core Animation Intensity", style = Typography.labelSmall, color = OrbitTextSecondary)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            AnimationIntensity.values().forEach { intensity ->
                                val isSelected = state.animationIntensity == intensity
                                val bg = if (isSelected) OrbitCyanAccent else OrbitCardSurface
                                val fg = if (isSelected) OrbitDeepVoid else OrbitTextSecondary
                                Box(
                                    contentAlignment = Alignment.Center,
                                    modifier = Modifier
                                        .weight(1f)
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(bg)
                                        .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                                        .clickable { viewModel.setAnimationIntensity(intensity) }
                                        .padding(vertical = 10.dp)
                                ) {
                                    Text(intensity.name, style = Typography.labelSmall.copy(color = fg))
                                }
                            }
                        }
                    }
                }

                // Section 4: Safety Guardrails
                GlassCard(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "SAFETY & CONFIRMATION",
                            style = Typography.labelSmall.copy(color = OrbitCyanAccent)
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Action Confirmation Mode", style = Typography.bodyLarge, color = OrbitTextPrimary)
                                Text("Prompt user before high-impact device actions", style = Typography.labelSmall, color = OrbitTextMuted)
                            }
                            Switch(
                                checked = state.confirmationMode,
                                onCheckedChange = { viewModel.toggleConfirmation(it) },
                                colors = SwitchDefaults.colors(checkedThumbColor = OrbitCyanAccent)
                            )
                        }
                    }
                }
            }
        }

        OrbitBottomNavigation(
            currentRoute = Screen.Settings.route,
            onNavigate = onNavigate,
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}
