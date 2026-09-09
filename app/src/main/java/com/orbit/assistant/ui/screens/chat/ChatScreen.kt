package com.orbit.assistant.ui.screens.chat

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
