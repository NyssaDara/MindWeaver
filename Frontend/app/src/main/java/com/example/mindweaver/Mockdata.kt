package com.example.mindweaver

data class HealthMetrics(
    val heartRate: String = "72 bpm",
    val spO2: String = "98%",
    val steps: String = "8,420",
    val sleep: String = "7h 15m",
    val co2: String = "410 ppm"
)

object MockRepository {
    fun getHealthMetrics(): HealthMetrics {
        return HealthMetrics()
    }
}
