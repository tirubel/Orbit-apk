package com.orbit.assistant.ui.components

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitIndigoAccent

@Composable
fun OrbitMicrophoneButton(
    state: OrbitState,
    size: Dp = 68.dp,
    onClick: () -> Unit
) {
    val isListening = state == OrbitState.LISTENING
    val isProcessing = state == OrbitState.THINKING || state == OrbitState.EXECUTING || state == OrbitState.SPEAKING
    val palette = getStatePalette(state)

    val infiniteTransition = rememberInfiniteTransition(label = "MicHalo")
    val haloScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.35f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "haloScale"
    )

    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier.size(size * 1.5f)
    ) {
        if (isListening || isProcessing) {
            Box(
                modifier = Modifier
                    .size(size)
                    .scale(haloScale)
                    .clip(CircleShape)
                    .background(palette.glow)
            )
        }

        Box(
            contentAlignment = Alignment.Center,
            modifier = Modifier
                .size(size)
                .clip(CircleShape)
                .background(
                    Brush.linearGradient(
                        colors = listOf(palette.primary, OrbitIndigoAccent)
                    )
                )
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) { onClick() }
        ) {
            Icon(
                imageVector = if (isListening || isProcessing) Icons.Default.Stop else Icons.Default.Mic,
                contentDescription = if (isListening) "Stop voice input" else "Start voice input",
                tint = OrbitDeepVoid,
                modifier = Modifier.size(size * 0.44f)
            )
        }
    }
}
