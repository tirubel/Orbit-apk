package com.orbit.assistant.ui.components

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
