package com.example.mindweaver

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun MainDashboardScreen() {
    val metrics = remember { MockRepository.getHealthMetrics() }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "MindWeaver Dashboard",
            style = MaterialTheme.typography.headlineMedium
        )
        Spacer(modifier = Modifier.height(16.dp))

        Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(text = "Heart Rate: ${metrics.heartRate}")
                Text(text = "SpO2: ${metrics.spO2}")
                Text(text = "Daily Steps: ${metrics.steps}")
                Text(text = "Sleep: ${metrics.sleep}")
                Text(text = "Air CO2 Level: ${metrics.co2}")
            }
        }
    }
}