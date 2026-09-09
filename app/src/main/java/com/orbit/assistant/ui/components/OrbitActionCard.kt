package com.orbit.assistant.ui.components

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
