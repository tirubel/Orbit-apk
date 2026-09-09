package com.orbit.assistant.ui.screens.activity

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
