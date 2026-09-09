package com.orbit.assistant.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.AnimationIntensity
import com.orbit.assistant.domain.model.OrbitState
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitCyanGlow
import com.orbit.assistant.ui.theme.OrbitErrorRed
import com.orbit.assistant.ui.theme.OrbitIndigoAccent
import com.orbit.assistant.ui.theme.OrbitOfflineGrey
import com.orbit.assistant.ui.theme.OrbitOnlineGreen
import com.orbit.assistant.ui.theme.OrbitSpeakingPurple
import com.orbit.assistant.ui.theme.OrbitThinkingAmber
import com.orbit.assistant.ui.theme.OrbitVioletSecondary
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

data class StateColorPalette(
    val primary: Color,
    val glow: Color,
    val secondary: Color
)

fun getStatePalette(state: OrbitState): StateColorPalette {
    return when (state) {
        OrbitState.IDLE -> StateColorPalette(OrbitCyanAccent, OrbitCyanGlow, OrbitIndigoAccent)
        OrbitState.LISTENING -> StateColorPalette(OrbitOnlineGreen, Color(0x6600F5A0), OrbitCyanAccent)
        OrbitState.THINKING -> StateColorPalette(OrbitThinkingAmber, Color(0x66FFB703), OrbitIndigoAccent)
        OrbitState.EXECUTING -> StateColorPalette(OrbitIndigoAccent, Color(0x666C5CE7), OrbitCyanAccent)
        OrbitState.SPEAKING -> StateColorPalette(OrbitSpeakingPurple, Color(0x66B5179E), OrbitVioletSecondary)
        OrbitState.ERROR -> StateColorPalette(OrbitErrorRed, Color(0x66FF4D6D), Color(0xFFE63946))
        OrbitState.CONNECTING -> StateColorPalette(OrbitCyanAccent, Color(0x4400E5FF), OrbitOnlineGreen)
        OrbitState.OFFLINE -> StateColorPalette(OrbitOfflineGrey, Color(0x3364748B), Color(0xFF334155))
    }
}

@Composable
fun OrbitCore(
    state: OrbitState,
    intensity: AnimationIntensity = AnimationIntensity.MEDIUM,
    size: Dp = 240.dp,
    modifier: Modifier = Modifier,
    onClick: () -> Unit = {}
) {
    val durationMultiplier = when (intensity) {
        AnimationIntensity.LOW -> 1.8f
        AnimationIntensity.MEDIUM -> 1.0f
        AnimationIntensity.HIGH -> 0.6f
    }

    val infiniteTransition = rememberInfiniteTransition(label = "OrbitCoreInfinite")
    val rotationOuter by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween((6000 * durationMultiplier).toInt(), easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotationOuter"
    )
    val rotationInner by infiniteTransition.animateFloat(
        initialValue = 360f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween((4500 * durationMultiplier).toInt(), easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotationInner"
    )
    val pulsePhase by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = (2 * PI).toFloat(),
        animationSpec = infiniteRepeatable(
            animation = tween((2200 * durationMultiplier).toInt(), easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "pulsePhase"
    )

    val palette = getStatePalette(state)
    val isAudioActive = state == OrbitState.LISTENING || state == OrbitState.SPEAKING

    Box(
        contentAlignment = Alignment.Center,
        modifier = modifier
            .size(size)
            .clickable(
                indication = null,
                interactionSource = remember { MutableInteractionSource() }
            ) { onClick() }
    ) {
        Canvas(modifier = Modifier.size(size)) {
            val center = Offset(this.size.width / 2f, this.size.height / 2f)
            val baseRadius = (this.size.minDimension / 2f) * 0.85f

            // 1. Ambient Breathing Glow
            val breathScale = 0.90f + sin(pulsePhase) * 0.08f
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(palette.glow, Color.Transparent),
                    center = center,
                    radius = baseRadius * breathScale * 1.3f
                ),
                radius = baseRadius * breathScale * 1.3f,
                center = center
            )

            // 2. Segmented Outer Technical Ring
            rotate(rotationOuter, pivot = center) {
                drawCircle(
                    color = palette.primary,
                    radius = baseRadius * 0.95f,
                    center = center,
                    style = Stroke(
                        width = 1.6f,
                        pathEffect = PathEffect.dashPathEffect(floatArrayOf(24f, 12f, 6f, 12f), 0f)
                    ),
                    alpha = 0.5f
                )
            }

            // 3. Counter-rotating Inner Guide Ring
            rotate(rotationInner, pivot = center) {
                drawCircle(
                    color = palette.secondary,
                    radius = baseRadius * 0.82f,
                    center = center,
                    style = Stroke(
                        width = 1.2f,
                        pathEffect = PathEffect.dashPathEffect(floatArrayOf(12f, 16f), 0f)
                    ),
                    alpha = 0.35f
                )
            }

            // 4. Equalizer Frequency Bars or Holographic Ring
            if (isAudioActive) {
                val barCount = 36
                rotate(rotationOuter * 0.5f, pivot = center) {
                    for (i in 0 until barCount) {
                        val angle = (i.toFloat() / barCount) * (2 * PI).toFloat()
                        val waveAmp = (sin(pulsePhase * 3f + i * 0.6f) * 0.5f + cos(pulsePhase * 2f + i) * 0.4f + 0.6f)
                        val barLen = (waveAmp * 18f).coerceAtLeast(3f)
                        val rInner = baseRadius * 0.66f
                        val rOuter = rInner + barLen
                        val start = Offset(center.x + cos(angle) * rInner, center.y + sin(angle) * rInner)
                        val end = Offset(center.x + cos(angle) * rOuter, center.y + sin(angle) * rOuter)
                        drawLine(
                            color = palette.primary,
                            start = start,
                            end = end,
                            strokeWidth = 2.2f,
                            cap = StrokeCap.Round,
                            alpha = 0.75f + waveAmp * 0.25f
                        )
                    }
                }
            } else {
                drawCircle(
                    color = palette.primary,
                    radius = baseRadius * 0.68f,
                    center = center,
                    style = Stroke(
                        width = 1f,
                        pathEffect = PathEffect.dashPathEffect(floatArrayOf(6f, 8f), 0f)
                    ),
                    alpha = 0.25f
                )
            }

            // 5. Intelligent Inner Energy Core
            val corePulse = 0.95f + sin(pulsePhase * 1.5f) * 0.05f
            val coreRadius = baseRadius * 0.44f * corePulse
            drawCircle(
                brush = Brush.radialGradient(
                    colorStops = arrayOf(
                        0.0f to Color.White,
                        0.35f to palette.primary,
                        0.85f to palette.secondary,
                        1.0f to Color.Transparent
                    ),
                    center = Offset(center.x - coreRadius * 0.2f, center.y - coreRadius * 0.25f),
                    radius = coreRadius
                ),
                radius = coreRadius,
                center = center
            )

            // 6. Sub-atomic Orbiting Data Particles
            val particleSpeeds = floatArrayOf(1.0f, -0.7f, 1.3f, -0.9f)
            val particleDists = floatArrayOf(0.72f, 0.86f, 0.60f, 0.78f)
            val particleRadii = floatArrayOf(2.5f, 3.0f, 2.0f, 2.8f)
            for (p in 0 until 4) {
                val pAngle = (rotationOuter * 0.02f * particleSpeeds[p]) + (p * 1.57f)
                val dist = baseRadius * particleDists[p]
                val px = center.x + cos(pAngle) * dist
                val py = center.y + sin(pAngle) * dist
                drawCircle(
                    color = Color.White,
                    radius = particleRadii[p],
                    center = Offset(px, py),
                    alpha = 0.85f
                )
            }
        }
    }
}
