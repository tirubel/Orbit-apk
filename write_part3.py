import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Wrote:", path)

# Theme
write_file("app/src/main/java/com/orbit/assistant/ui/theme/Color.kt", """package com.orbit.assistant.ui.theme

import androidx.compose.ui.graphics.Color

val OrbitDeepVoid = Color(0xFF07090E)
val OrbitSpaceSurface = Color(0xFF0E131D)
val OrbitCardSurface = Color(0xB2141B28)
val OrbitGlassBorder = Color(0x4D2A3952)
val OrbitGlassBorderHighlight = Color(0x7300E5FF)

val OrbitCyanAccent = Color(0xFF00E5FF)
val OrbitCyanGlow = Color(0x6600E5FF)
val OrbitIndigoAccent = Color(0xFF6C5CE7)
val OrbitVioletSecondary = Color(0xFF9D4EDD)

val OrbitOnlineGreen = Color(0xFF00F5A0)
val OrbitThinkingAmber = Color(0xFFFFB703)
val OrbitSpeakingPurple = Color(0xFFB5179E)
val OrbitErrorRed = Color(0xFFFF4D6D)
val OrbitOfflineGrey = Color(0xFF64748B)

val OrbitTextPrimary = Color(0xFFF1F5F9)
val OrbitTextSecondary = Color(0xFF94A3B8)
val OrbitTextMuted = Color(0xFF475569)
""")

write_file("app/src/main/java/com/orbit/assistant/ui/theme/Type.kt", """package com.orbit.assistant.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    titleLarge = TextStyle(
        fontFamily = FontFamily.Monospace,
        fontWeight = FontWeight.Bold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        color = OrbitTextPrimary
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.Monospace,
        fontWeight = FontWeight.SemiBold,
        fontSize = 16.sp,
        lineHeight = 22.sp,
        color = OrbitTextPrimary
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 15.sp,
        lineHeight = 22.sp,
        color = OrbitTextPrimary
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 13.sp,
        lineHeight = 18.sp,
        color = OrbitTextSecondary
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Monospace,
        fontWeight = FontWeight.Medium,
        fontSize = 10.sp,
        lineHeight = 14.sp,
        color = OrbitTextMuted
    )
)
""")

write_file("app/src/main/java/com/orbit/assistant/ui/theme/Theme.kt", """package com.orbit.assistant.ui.theme

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
""")

# Components
write_file("app/src/main/java/com/orbit/assistant/ui/components/GlassCard.kt", """package com.orbit.assistant.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitGlassBorder

@Composable
fun GlassCard(
    modifier: Modifier = Modifier,
    shape: Shape = RoundedCornerShape(16.dp),
    backgroundColor: Color = OrbitCardSurface,
    borderColor: Color = OrbitGlassBorder,
    borderWidth: Dp = 1.dp,
    content: @Composable BoxScope.() -> Unit
) {
    Surface(
        modifier = modifier,
        shape = shape,
        color = backgroundColor,
        border = BorderStroke(borderWidth, borderColor)
    ) {
        Box(content = content)
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/components/OrbitCore.kt", """package com.orbit.assistant.ui.components

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
""")

write_file("app/src/main/java/com/orbit/assistant/ui/components/OrbitMicrophoneButton.kt", """package com.orbit.assistant.ui.components

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
""")

write_file("app/src/main/java/com/orbit/assistant/ui/components/OrbitTextInput.kt", """package com.orbit.assistant.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.unit.dp
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitDeepVoid
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitTextMuted
import com.orbit.assistant.ui.theme.OrbitTextPrimary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun OrbitTextInput(
    value: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    placeholder: String = "Ask Orbit or command device...",
    enabled: Boolean = true,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(OrbitCardSurface)
            .border(1.dp, OrbitGlassBorder, RoundedCornerShape(24.dp))
            .padding(horizontal = 16.dp, vertical = 10.dp)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth()
        ) {
            Box(modifier = Modifier.weight(1f)) {
                if (value.isEmpty()) {
                    Text(
                        text = placeholder,
                        style = Typography.bodyLarge,
                        color = OrbitTextMuted
                    )
                }
                BasicTextField(
                    value = value,
                    onValueChange = onValueChange,
                    enabled = enabled,
                    singleLine = true,
                    textStyle = Typography.bodyLarge.copy(color = OrbitTextPrimary),
                    cursorBrush = SolidColor(OrbitCyanAccent),
                    modifier = Modifier.fillMaxWidth()
                )
            }
            if (value.isNotBlank()) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .padding(start = 8.dp)
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(OrbitCyanAccent)
                        .clickable { onSend() }
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.Send,
                        contentDescription = "Send",
                        tint = OrbitDeepVoid,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/components/OrbitActionCard.kt", """package com.orbit.assistant.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.orbit.assistant.domain.model.ActionCardData
import com.orbit.assistant.ui.theme.OrbitCyanAccent
import com.orbit.assistant.ui.theme.OrbitErrorRed
import com.orbit.assistant.ui.theme.OrbitOnlineGreen
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun OrbitActionCard(
    action: ActionCardData,
    modifier: Modifier = Modifier
) {
    val statusColor = if (action.isSuccess) OrbitOnlineGreen else OrbitErrorRed
    val borderColor = if (action.isSuccess) Color(0x3300F5A0) else Color(0x33FF4D6D)

    GlassCard(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        borderColor = borderColor
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = action.title,
                    style = Typography.titleMedium.copy(color = OrbitCyanAccent)
                )
                Text(
                    text = action.statusText,
                    style = Typography.labelSmall.copy(color = statusColor)
                )
            }
            Text(
                text = action.detail,
                style = Typography.bodyMedium.copy(color = OrbitTextSecondary)
            )
        }
    }
}
""")

write_file("app/src/main/java/com/orbit/assistant/ui/components/OrbitStatusIndicator.kt", """package com.orbit.assistant.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.orbit.assistant.ui.theme.OrbitCardSurface
import com.orbit.assistant.ui.theme.OrbitGlassBorder
import com.orbit.assistant.ui.theme.OrbitOfflineGrey
import com.orbit.assistant.ui.theme.OrbitOnlineGreen
import com.orbit.assistant.ui.theme.OrbitTextSecondary
import com.orbit.assistant.ui.theme.Typography

@Composable
fun OrbitStatusIndicator(
    isOnline: Boolean,
    modelName: String,
    modifier: Modifier = Modifier
) {
    val dotColor = if (isOnline) OrbitOnlineGreen else OrbitOfflineGrey
    val text = if (isOnline) "OMNIROUTE ONLINE • $modelName" else "OMNIROUTE OFFLINE"

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(OrbitCardSurface)
            .border(1.dp, OrbitGlassBorder, RoundedCornerShape(16.dp))
            .padding(horizontal = 10.dp, vertical = 5.dp)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(6.dp)
                    .clip(CircleShape)
                    .background(dotColor)
            )
            Text(
                text = text,
                style = Typography.labelSmall.copy(color = OrbitTextSecondary)
            )
        }
    }
}
""")

print("Part 3 written successfully.")
