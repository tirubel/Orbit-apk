package com.orbit.assistant.ui.screens.permissions

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
