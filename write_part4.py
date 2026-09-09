import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote:", path)

write_file("app/src/main/java/com/orbit/assistant/ui/navigation/Screen.kt", """package com.orbit.assistant.ui.navigation

sealed class Screen(val route: String) {
    object Onboarding : Screen("onboarding")
    object Home : Screen("home")
    object Chat : Screen("chat")
    object Activity : Screen("activity")
    object Settings : Screen("settings")
    object Permissions : Screen("permissions")
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/components/OrbitBottomNavigation.kt", """package com.orbit.assistant.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.filled.GraphicEq
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.orbit.assistant.ui.navigation.Screen
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.Typography

data class NavItem(
    val route: String,
    val label: String,
    val icon: ImageVector
)

val navItems = listOf(
    NavItem(Screen.Home.route, "Core", Icons.Default.GraphicEq),
    NavItem(Screen.Chat.route, "Chat", Icons.AutoMirrored.Filled.Chat),
    NavItem(Screen.Activity.route, "Activity", Icons.Default.List),
    NavItem(Screen.Permissions.route, "Shield", Icons.Default.Security),
    NavItem(Screen.Settings.route, "Config", Icons.Default.Settings)
)

@Composable
fun OrbitBottomNavigation(
    currentRoute: String,
    onNavigate: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp)
            .clip(RoundedCornerShape(24.dp))
            .background(OrbitCardSurface)
            .border(1.dp, OrbitGlassBorder, RoundedCornerShape(24.dp))
            .padding(vertical = 8.dp, horizontal = 4.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceAround,
            verticalAlignment = Alignment.CenterVertically
        ) {
            navItems.forEach { item ->
                val selected = currentRoute == item.route
                val tint = if (selected) OrbitCyanAccent else OrbitTextMuted

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(4.dp),
                    modifier = Modifier
                        .clip(RoundedCornerShape(12.dp))
                        .clickable(
                            interactionSource = remember { MutableInteractionSource() },
                            indication = null
                        ) { onNavigate(item.route) }
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    Icon(
                        imageVector = item.icon,
                        contentDescription = item.label,
                        tint = tint,
                        modifier = Modifier.size(20.dp)
                    )
                    Text(
                        text = item.label,
                        style = Typography.labelSmall.copy(color = tint)
                    )
                }
            }
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/onboarding/OnboardingScreen.kt", """package com.orbit.assistant.ui.screens.onboarding

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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Memory
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.ui.components.GlassCard
import com.orbit.assistant.ui.components.OrbitCore
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextPrimary
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun OnboardingScreen(
    onComplete: () -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(OrbitDeepVoid)
            .padding(24.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.padding(top = 16.dp)
            ) {
                Text(
                    text = "ORBIT",
                    style = Typography.titleLarge.copy(color = OrbitCyanAccent),
                    modifier = Modifier.padding(bottom = 4.dp)
                )
                Text(
                    text = "AUTONOMOUS ON-DEVICE ASSISTANT",
                    style = Typography.labelSmall.copy(color = OrbitTextMuted)
                )
            }

            OrbitCore(
                state = OrbitState.CONNECTING,
                size = 200.dp
            )

            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                FeatureRow(
                    icon = Icons.Default.Memory,
                    title = "Local OmniRoute Intelligence",
                    description = "Connects natively to your on-device local gateway without cloud leakage."
                )
                FeatureRow(
                    icon = Icons.Default.Lock,
                    title = "Hardware Keystore Vault",
                    description = "API keys secured using Android Keystore AES-256 GCM encryption."
                )
                FeatureRow(
                    icon = Icons.Default.Mic,
                    title = "Autonomous Device Tools",
                    description = "Safely launch apps, query device time, search web, and dispatch speech."
                )
            }

            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(OrbitCyanAccent)
                    .clickable { onComplete() }
                    .padding(vertical = 16.dp)
            ) {
                Text(
                    text = "INITIALIZE CORE SYSTEM",
                    style = Typography.titleMedium.copy(color = OrbitDeepVoid)
                )
            }
        }
    }
}

@Composable
private fun FeatureRow(
    icon: ImageVector,
    title: String,
    description: String
) {
    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(40.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = OrbitCyanAccent,
                    modifier = Modifier.size(20.dp)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = Typography.titleMedium.copy(color = OrbitTextPrimary)
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = description,
                    style = Typography.bodyMedium.copy(color = OrbitTextSecondary)
                )
            }
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/home/HomeViewModel.kt", """package com.orbit.assistant.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.domain.repository.SettingsRepository
import com.orbit.assistant.service.voice.OrbitSpeechRecognizer
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class HomeViewModel(
    private val orbitEngine: OrbitEngine,
    private val settingsRepository: SettingsRepository,
    private val speechRecognizer: OrbitSpeechRecognizer
) : ViewModel() {

    val orbitState: StateFlow<OrbitState> = orbitEngine.currentState
    val isOnline: StateFlow<Boolean> = orbitEngine.isOnline
    val selectedModel: StateFlow<String> = settingsRepository.settingsState
        .map { it.selectedModel }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "Auto")

    val animationIntensity = settingsRepository.settingsState
        .map { it.animationIntensity }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), com.orbit.assistant.domain.model.AnimationIntensity.MEDIUM)

    private val _inputQuery = MutableStateFlow("")
    val inputQuery: StateFlow<String> = _inputQuery.asStateFlow()

    fun updateInputQuery(text: String) {
        _inputQuery.value = text
    }

    fun submitTextCommand() {
        val query = _inputQuery.value.trim()
        if (query.isNotBlank()) {
            _inputQuery.value = ""
            viewModelScope.launch {
                orbitEngine.processCommand(query)
            }
        }
    }

    fun toggleVoiceInput() {
        val currentState = orbitEngine.currentState.value
        if (currentState == OrbitState.LISTENING) {
            speechRecognizer.stopListening()
            orbitEngine.stop()
        } else {
            speechRecognizer.startListening { spokenText ->
                viewModelScope.launch {
                    orbitEngine.processCommand(spokenText)
                }
            }
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/home/HomeScreen.kt", """package com.orbit.assistant.ui.screens.home

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
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/chat/ChatViewModel.kt", """package com.orbit.assistant.ui.screens.chat

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.model.ConversationMessage
import com.orbit.assistant.domain.model.OrbitState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ChatViewModel(
    private val orbitEngine: OrbitEngine
) : ViewModel() {

    val conversation: StateFlow<List<ConversationMessage>> = orbitEngine.conversation
    val currentState: StateFlow<OrbitState> = orbitEngine.currentState

    private val _inputText = MutableStateFlow("")
    val inputText: StateFlow<String> = _inputText.asStateFlow()

    fun updateInputText(text: String) {
        _inputText.value = text
    }

    fun sendMessage() {
        val query = _inputText.value.trim()
        if (query.isNotBlank()) {
            _inputText.value = ""
            viewModelScope.launch {
                orbitEngine.processCommand(query)
            }
        }
    }

    fun clearChat() {
        viewModelScope.launch {
            orbitEngine.clearConversation()
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/chat/ChatScreen.kt", """package com.orbit.assistant.ui.screens.chat

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
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.ConversationMessage
import com.orbit.assistant.domain.model.MessageSender
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.ui.components.OrbitActionCard
import com.orbit.assistant.ui.components.OrbitBottomNavigation
import com.orbit.assistant.ui.components.OrbitTextInput
import com.orbit.assistant.ui.navigation.Screen
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitIndigoAccent
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextPrimary
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun ChatScreen(
    viewModel: ChatViewModel,
    onNavigate: (String) -> Unit
) {
    val messages by viewModel.conversation.collectAsState()
    val currentState by viewModel.currentState.collectAsState()
    val inputText by viewModel.inputText.collectAsState()
    val listState = rememberLazyListState()

    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(OrbitDeepVoid)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 76.dp)
        ) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "COMMUNICATION STREAM",
                        style = Typography.titleMedium.copy(color = OrbitCyanAccent)
                    )
                    Text(
                        text = "LIVE AUTONOMOUS DIALOGUE",
                        style = Typography.labelSmall.copy(color = OrbitTextMuted)
                    )
                }
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                        .clickable { viewModel.clearChat() }
                        .padding(8.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.DeleteSweep,
                        contentDescription = "Clear chat",
                        tint = OrbitTextSecondary
                    )
                }
            }

            // Message Stream
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(messages, key = { it.id }) { msg ->
                    ChatBubble(msg)
                }

                if (currentState == OrbitState.THINKING || currentState == OrbitState.EXECUTING) {
                    item {
                        Text(
                            text = if (currentState == OrbitState.THINKING) "Orbit is reasoning..." else "Orbit is executing tool...",
                            style = Typography.labelSmall.copy(color = OrbitCyanAccent),
                            modifier = Modifier.padding(start = 12.dp, top = 4.dp)
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))
            Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp)) {
                OrbitTextInput(
                    value = inputText,
                    onValueChange = { viewModel.updateInputText(it) },
                    onSend = { viewModel.sendMessage() },
                    placeholder = "Message Orbit..."
                )
            }
        }

        OrbitBottomNavigation(
            currentRoute = Screen.Chat.route,
            onNavigate = onNavigate,
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}

@Composable
private fun ChatBubble(message: ConversationMessage) {
    val isUser = message.sender == MessageSender.USER
    val alignment = if (isUser) Alignment.End else Alignment.Start

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = alignment
    ) {
        val bubbleColor = if (isUser) OrbitIndigoAccent.copy(alpha = 0.35f) else OrbitCardSurface
        val borderColor = if (isUser) OrbitIndigoAccent.copy(alpha = 0.6f) else OrbitGlassBorder

        Box(
            modifier = Modifier
                .widthIn(max = 300.dp)
                .clip(
                    RoundedCornerShape(
                        topStart = 16.dp,
                        topEnd = 16.dp,
                        bottomStart = if (isUser) 16.dp else 2.dp,
                        bottomEnd = if (isUser) 2.dp else 16.dp
                    )
                )
                .background(bubbleColor)
                .border(
                    1.dp,
                    borderColor,
                    RoundedCornerShape(
                        topStart = 16.dp,
                        topEnd = 16.dp,
                        bottomStart = if (isUser) 16.dp else 2.dp,
                        bottomEnd = if (isUser) 2.dp else 16.dp
                    )
                )
                .padding(horizontal = 14.dp, vertical = 10.dp)
        ) {
            Text(
                text = message.text,
                style = Typography.bodyLarge.copy(color = OrbitTextPrimary)
            )
        }

        message.actionCard?.let { card ->
            Spacer(modifier = Modifier.height(6.dp))
            OrbitActionCard(action = card, modifier = Modifier.widthIn(max = 320.dp))
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/activity/ActivityViewModel.kt", """package com.orbit.assistant.ui.screens.activity

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
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/activity/ActivityScreen.kt", """package com.orbit.assistant.ui.screens.activity

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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.ActionItem
import com.orbit.assistant.domain.model.ActionStatus
import com.orbit.assistant.ui.components.GlassCard
import com.orbit.assistant.ui.components.OrbitBottomNavigation
import com.orbit.assistant.ui.navigation.Screen
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitErrorRed
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitOnlineGreen
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextPrimary
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.OrbitThinkingAmber
import com.orbit.assistant.ui.theme.Typography

@Composable
fun ActivityScreen(
    viewModel: ActivityViewModel,
    onNavigate: (String) -> Unit
) {
    val actions by viewModel.actions.collectAsState()

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(OrbitDeepVoid)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 76.dp)
        ) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "SYSTEM AUDIT LOG",
                        style = Typography.titleMedium.copy(color = OrbitCyanAccent)
                    )
                    Text(
                        text = "VERIFIED ACTION & TELEMETRY HISTORY",
                        style = Typography.labelSmall.copy(color = OrbitTextMuted)
                    )
                }
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                        .clickable { viewModel.clearAuditLog() }
                        .padding(8.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "Clear logs",
                        tint = OrbitTextSecondary
                    )
                }
            }

            if (actions.isEmpty()) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                ) {
                    Text(
                        text = "No recorded device actions yet.",
                        style = Typography.bodyMedium.copy(color = OrbitTextMuted)
                    )
                }
            } else {
                LazyColumn(
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    items(actions, key = { it.id }) { item ->
                        ActivityRow(item)
                    }
                }
            }
        }

        OrbitBottomNavigation(
            currentRoute = Screen.Activity.route,
            onNavigate = onNavigate,
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}

@Composable
private fun ActivityRow(item: ActionItem) {
    val statusColor = when (item.status) {
        ActionStatus.COMPLETED -> OrbitOnlineGreen
        ActionStatus.FAILED -> OrbitErrorRed
        ActionStatus.IN_PROGRESS -> OrbitThinkingAmber
    }

    GlassCard(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = item.title,
                    style = Typography.titleMedium.copy(color = OrbitTextPrimary)
                )
                Text(
                    text = item.status.name,
                    style = Typography.labelSmall.copy(color = statusColor)
                )
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = item.detail,
                style = Typography.bodyMedium.copy(color = OrbitTextSecondary)
            )
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "${item.section} • ${item.timestamp}",
                style = Typography.labelSmall.copy(color = OrbitTextMuted)
            )
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/settings/SettingsViewModel.kt", """package com.orbit.assistant.ui.screens.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.orbit.assistant.domain.model.AnimationIntensity
import com.orbit.assistant.domain.model.SettingsState
import com.orbit.assistant.domain.repository.SettingsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SettingsViewModel(
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    val settingsState: StateFlow<SettingsState> = settingsRepository.settingsState

    private val _urlInput = MutableStateFlow("http://127.0.0.1:20128/v1")
    val urlInput: StateFlow<String> = _urlInput.asStateFlow()

    private val _apiKeyInput = MutableStateFlow("")
    val apiKeyInput: StateFlow<String> = _apiKeyInput.asStateFlow()

    private val _isTestingConnection = MutableStateFlow(false)
    val isTestingConnection: StateFlow<Boolean> = _isTestingConnection.asStateFlow()

    private val _testResult = MutableStateFlow<String?>(null)
    val testResult: StateFlow<String?> = _testResult.asStateFlow()

    private val _isSuccess = MutableStateFlow(false)
    val isSuccess: StateFlow<Boolean> = _isSuccess.asStateFlow()

    init {
        viewModelScope.launch {
            settingsRepository.settingsState.collect { state ->
                _urlInput.value = state.omniRouteUrl
            }
        }
    }

    fun updateUrl(url: String) {
        _urlInput.value = url
    }

    fun updateApiKey(key: String) {
        _apiKeyInput.value = key
    }

    fun selectModel(model: String) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(selectedModel = model) }
        }
    }

    fun setAnimationIntensity(intensity: AnimationIntensity) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(animationIntensity = intensity) }
        }
    }

    fun toggleVoice(enabled: Boolean) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(voiceEnabled = enabled) }
        }
    }

    fun toggleTts(enabled: Boolean) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(textToSpeech = enabled) }
        }
    }

    fun toggleConfirmation(enabled: Boolean) {
        viewModelScope.launch {
            settingsRepository.updateSettings { it.copy(confirmationMode = enabled) }
        }
    }

    fun saveSettings() {
        viewModelScope.launch {
            settingsRepository.updateSettings {
                it.copy(omniRouteUrl = _urlInput.value.trim())
            }
            if (_apiKeyInput.value.isNotBlank()) {
                settingsRepository.saveApiKey(_apiKeyInput.value.trim())
                _apiKeyInput.value = ""
            }
            _testResult.value = "Settings saved to encrypted vault."
            _isSuccess.value = true
        }
    }

    fun testConnection() {
        viewModelScope.launch {
            _isTestingConnection.value = true
            _testResult.value = "Pinging OmniRoute at ${_urlInput.value}..."
            _isSuccess.value = false

            settingsRepository.updateSettings { it.copy(omniRouteUrl = _urlInput.value.trim()) }
            if (_apiKeyInput.value.isNotBlank()) {
                settingsRepository.saveApiKey(_apiKeyInput.value.trim())
                _apiKeyInput.value = ""
            }

            val result = settingsRepository.testOmniRouteConnection()
            _isTestingConnection.value = false
            result.fold(
                onSuccess = { (latency, models) ->
                    _isSuccess.value = true
                    _testResult.value = "OmniRoute Connected (${latency}ms latency). ${models.size - 1} models available."
                },
                onFailure = { err ->
                    _isSuccess.value = false
                    _testResult.value = "Connection Failed: ${err.message ?: "Unknown error"}"
                }
            )
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/settings/SettingsScreen.kt", """package com.orbit.assistant.ui.screens.settings

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
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/permissions/PermissionViewModel.kt", """package com.orbit.assistant.ui.screens.permissions

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
""")

write_file("app/src/main/java/com/orbit/assistant/ui/screens/permissions/PermissionCenterScreen.kt", """package com.orbit.assistant.ui.screens.permissions

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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Dangerous
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.PermissionItem
import com.orbit.assistant.ui.components.GlassCard
import com.orbit.assistant.ui.components.OrbitBottomNavigation
import com.orbit.assistant.ui.navigation.Screen
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitErrorRed
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitOnlineGreen
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextPrimary
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun PermissionCenterScreen(
    viewModel: PermissionViewModel,
    onRequestPermission: (String) -> Unit,
    onNavigate: (String) -> Unit
) {
    val permissions by viewModel.permissions.collectAsState()

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(OrbitDeepVoid)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 76.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "PERMISSION SHIELD",
                        style = Typography.titleMedium.copy(color = OrbitCyanAccent)
                    )
                    Text(
                        text = "REAL DEVICE ACCESS & PRIVACY STATE",
                        style = Typography.labelSmall.copy(color = OrbitTextMuted)
                    )
                }
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .border(1.dp, OrbitGlassBorder, RoundedCornerShape(8.dp))
                        .clickable { viewModel.refreshPermissions() }
                        .padding(8.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Refresh,
                        contentDescription = "Refresh permissions",
                        tint = OrbitTextSecondary
                    )
                }
            }

            LazyColumn(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                items(permissions, key = { it.id }) { item ->
                    PermissionCard(
                        item = item,
                        onRequest = {
                            if (item.id == "perm_accessibility") {
                                viewModel.openAccessibilitySettings()
                            } else if (item.id == "perm_mic") {
                                onRequestPermission(android.Manifest.permission.RECORD_AUDIO)
                            } else {
                                viewModel.openAppSettings()
                            }
                        }
                    )
                }

                item {
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .border(1.dp, OrbitGlassBorder, RoundedCornerShape(12.dp))
                            .clickable { viewModel.openAppSettings() }
                            .padding(14.dp)
                    ) {
                        Text(
                            text = "OPEN ANDROID SYSTEM APP SETTINGS",
                            style = Typography.labelSmall.copy(color = OrbitCyanAccent)
                        )
                    }
                }
            }
        }

        OrbitBottomNavigation(
            currentRoute = Screen.Permissions.route,
            onNavigate = onNavigate,
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}

@Composable
private fun PermissionCard(
    item: PermissionItem,
    onRequest: () -> Unit
) {
    val statusColor = if (item.isGranted) OrbitOnlineGreen else OrbitErrorRed
    val statusText = if (item.isGranted) "GRANTED" else "NOT GRANTED"
    val icon = if (item.isGranted) Icons.Default.CheckCircle else Icons.Default.Dangerous

    GlassCard(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = item.title,
                    style = Typography.titleMedium.copy(color = OrbitTextPrimary),
                    modifier = Modifier.weight(1f)
                )
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Icon(icon, contentDescription = null, tint = statusColor, modifier = Modifier.size(16.dp))
                    Text(
                        text = statusText,
                        style = Typography.labelSmall.copy(color = statusColor)
                    )
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = item.description,
                style = Typography.bodyMedium.copy(color = OrbitTextSecondary)
            )
            if (!item.isGranted) {
                Spacer(modifier = Modifier.height(12.dp))
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(OrbitCyanAccent)
                        .clickable { onRequest() }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = "GRANT PERMISSION",
                        style = Typography.labelSmall.copy(color = OrbitDeepVoid)
                    )
                }
            }
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/navigation/OrbitNavGraph.kt", """package com.orbit.assistant.ui.navigation

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
""")

write_file("app/src/main/java/com/orbit/assistant/OrbitApplication.kt", """package com.orbit.assistant

import android.app.Application
import com.orbit.assistant.data.engine.RealOrbitEngine
import com.orbit.assistant.data.remote.OmniRouteClient
import com.orbit.assistant.data.repository.ActivityRepositoryImpl
import com.orbit.assistant.data.repository.SettingsRepositoryImpl
import com.orbit.assistant.data.security.AndroidKeystoreSecureStorage
import com.orbit.assistant.domain.engine.OrbitEngine
import com.orbit.assistant.domain.repository.ActivityRepository
import com.orbit.assistant.domain.repository.SecureStorage
import com.orbit.assistant.domain.repository.SettingsRepository
import com.orbit.assistant.domain.tools.GetCurrentTimeTool
import com.orbit.assistant.domain.tools.OpenAppTool
import com.orbit.assistant.domain.tools.OpenUrlTool
import com.orbit.assistant.domain.tools.SearchWebTool
import com.orbit.assistant.domain.tools.ToolRegistry
import com.orbit.assistant.service.voice.OrbitSpeechRecognizer
import com.orbit.assistant.service.voice.OrbitTextToSpeech

class OrbitApplication : Application() {

    lateinit var secureStorage: SecureStorage
        private set
    lateinit var omniRouteClient: OmniRouteClient
        private set
    lateinit var settingsRepository: SettingsRepository
        private set
    lateinit var activityRepository: ActivityRepository
        private set
    lateinit var toolRegistry: ToolRegistry
        private set
    lateinit var speechRecognizer: OrbitSpeechRecognizer
        private set
    lateinit var textToSpeech: OrbitTextToSpeech
        private set
    lateinit var orbitEngine: OrbitEngine
        private set

    override fun onCreate() {
        super.onCreate()

        // 1. Hardware Keystore backed storage
        secureStorage = AndroidKeystoreSecureStorage(this)

        // 2. OmniRoute OpenAI-compatible network client
        omniRouteClient = OmniRouteClient()

        // 3. Repositories
        settingsRepository = SettingsRepositoryImpl(
            context = this,
            secureStorage = secureStorage,
            omniRouteClient = omniRouteClient
        )
        activityRepository = ActivityRepositoryImpl()

        // 4. Secure Tool Registry (Zero arbitrary code execution)
        toolRegistry = ToolRegistry().apply {
            register(OpenAppTool(this@OrbitApplication))
            register(OpenUrlTool(this@OrbitApplication))
            register(GetCurrentTimeTool())
            register(SearchWebTool(this@OrbitApplication))
        }

        // 5. Native Voice Subsystems
        speechRecognizer = OrbitSpeechRecognizer(this)
        textToSpeech = OrbitTextToSpeech(this)

        // 6. Real Autonomous Agent Loop
        orbitEngine = RealOrbitEngine(
            omniRouteClient = omniRouteClient,
            settingsRepository = settingsRepository,
            activityRepository = activityRepository,
            toolRegistry = toolRegistry,
            onSpeak = { text -> textToSpeech.speak(text) }
        )
    }

    override fun onTerminate() {
        super.onTerminate()
        textToSpeech.shutdown()
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/MainActivity.kt", """package com.orbit.assistant

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
""")

print("Part 4 written successfully.")
