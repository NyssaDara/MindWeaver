def calculate_digital_twin(
    health,
    mood,
    screen_time=None,
    previous_health=None,
    previous_mood=None
):

    score = 0

    signals = []

    suggestions = []


    # =========================================
    # HEALTH DATA
    # =========================================

    if health:

        heart_rate = health.get("heart_rate")

        spo2 = health.get("spo2")

        steps = health.get("steps")

        sleep = health.get("sleep_hours")


        # -----------------------------------------
        # HEART RATE
        # -----------------------------------------

        if heart_rate is not None:

            if heart_rate > 100:

                score += 10

                signals.append(
                    "Heart rate is currently elevated."
                )

            elif heart_rate < 50:

                score += 10

                signals.append(
                    "Heart rate is currently lower than usual."
                )


        # -----------------------------------------
        # SPO2
        # -----------------------------------------

        if spo2 is not None:

            if spo2 < 94:

                score += 20

                signals.append(
                    "SpO₂ reading is lower than expected."
                )


        # -----------------------------------------
        # SLEEP
        # -----------------------------------------

        if sleep is not None:

            if sleep < 5:

                score += 15

                signals.append(
                    "Sleep duration is quite low."
                )

            elif sleep < 6:

                score += 8

                signals.append(
                    "Sleep duration is below the recommended range."
                )


        # -----------------------------------------
        # ACTIVITY
        # -----------------------------------------

        if steps is not None:

            if steps < 2000:

                score += 10

                signals.append(
                    "Physical activity is relatively low today."
                )


    # =========================================
    # MOOD DATA
    # =========================================

    if mood:

        stress = mood.get("stress_level")

        anxiety = mood.get("anxiety_level")

        mood_value = mood.get("mood")


        # -----------------------------------------
        # STRESS
        # -----------------------------------------

        if stress is not None:

            if stress >= 8:

                score += 15

                signals.append(
                    "Self-reported stress level is high."
                )

            elif stress >= 6:

                score += 8

                signals.append(
                    "Self-reported stress is elevated."
                )


        # -----------------------------------------
        # ANXIETY
        # -----------------------------------------

        if anxiety is not None:

            if anxiety >= 8:

                score += 15

                signals.append(
                    "Self-reported anxiety level is high."
                )

            elif anxiety >= 6:

                score += 8

                signals.append(
                    "Self-reported anxiety is elevated."
                )


        # -----------------------------------------
        # MOOD
        # -----------------------------------------

        if mood_value:

            negative_moods = [
                "sad",
                "low",
                "very low",
                "anxious",
                "stressed",
                "bad",
                "terrible"
            ]

            if mood_value.lower() in negative_moods:

                score += 10

                signals.append(
                    "The latest mood check-in indicates lower wellbeing."
                )


    # =========================================
    # SCREEN TIME
    # =========================================

    if screen_time is not None:

        if screen_time > 600:

            score += 10

            signals.append(
                "Screen time is unusually high."
            )

        elif screen_time > 480:

            score += 5

            signals.append(
                "Screen time is relatively high."
            )


    # =========================================
    # COMBINATION PATTERNS
    # =========================================

    if health and mood:

        sleep = health.get("sleep_hours")

        steps = health.get("steps")

        stress = mood.get("stress_level")

        anxiety = mood.get("anxiety_level")


        if (
            sleep is not None
            and sleep < 6
            and stress is not None
            and stress >= 7
        ):

            score += 10

            signals.append(
                "Reduced sleep and elevated stress are occurring together."
            )


        if (
            steps is not None
            and steps < 3000
            and anxiety is not None
            and anxiety >= 7
        ):

            score += 10

            signals.append(
                "Low activity and elevated anxiety are occurring together."
            )


    # =========================================
    # LIMIT SCORE
    # =========================================

    if score > 100:

        score = 100


    # =========================================
    # RISK LEVEL
    # =========================================

    if score < 25:

        risk_level = "Low"

        suggestions.append(
            "Your current pattern appears relatively stable."
        )

        suggestions.append(
            "Continue your regular sleep, activity and wellbeing routine."
        )


    elif score < 50:

        risk_level = "Moderate"

        suggestions.append(
            "Some changes from your usual wellbeing pattern are visible."
        )

        suggestions.append(
            "Consider taking a break, staying hydrated and maintaining regular sleep."
        )


    elif score < 75:

        risk_level = "Elevated"

        suggestions.append(
            "Several wellbeing signals appear elevated."
        )

        suggestions.append(
            "Consider reducing stress, getting adequate rest and monitoring how you feel."
        )


    else:

        risk_level = "High"

        suggestions.append(
            "Multiple signals indicate that your wellbeing pattern deserves attention."
        )

        suggestions.append(
            "If these changes persist or you feel unwell, consider speaking with a healthcare professional."
        )


    # =========================================
    # FINAL RESULT
    # =========================================

    return {

        "risk_score": score,

        "risk_level": risk_level,

        "signals": signals,

        "suggestions": suggestions

    }