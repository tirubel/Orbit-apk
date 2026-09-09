package com.orbit.assistant.ui.screens.onboarding

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
