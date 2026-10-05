def generate_response(message):

    message = message.lower().strip()


    # =========================================
    # GREETING
    # =========================================

    if any(word in message for word in [
        "hi",
        "hello",
        "hey"
    ]):

        return (
            "Hi! I'm your Digital Twin wellbeing assistant. "
            "How are you feeling today?"
        )


    # =========================================
    # SAD / LOW
    # =========================================

    if any(word in message for word in [
        "sad",
        "low",
        "depressed",
        "unhappy",
        "crying"
    ]):

        return (
            "I'm sorry you're feeling low. "
            "You don't have to handle everything alone. "
            "Would you like to talk about what's bothering you?"
        )


    # =========================================
    # STRESS
    # =========================================

    if any(word in message for word in [
        "stress",
        "stressed",
        "pressure"
    ]):

        return (
            "It sounds like you may be under some pressure. "
            "Try taking a short break, breathing slowly, "
            "and stepping away from the screen for a few minutes."
        )


    # =========================================
    # ANXIETY
    # =========================================

    if any(word in message for word in [
        "anxiety",
        "anxious",
        "panic",
        "worried"
    ]):

        return (
            "I'm here with you. "
            "Try slowing your breathing and focusing on what is happening "
            "around you right now. If these feelings are severe or persistent, "
            "consider talking to a mental-health professional."
        )


    # =========================================
    # SLEEP
    # =========================================

    if any(word in message for word in [
        "sleep",
        "insomnia",
        "can't sleep"
    ]):

        return (
            "Sleep can strongly affect mood and daily wellbeing. "
            "Try keeping a consistent sleep schedule and reducing screen "
            "use before bedtime."
        )


    # =========================================
    # TIRED
    # =========================================

    if any(word in message for word in [
        "tired",
        "exhausted",
        "fatigue"
    ]):

        return (
            "You sound tired. Consider taking some rest, drinking water, "
            "and checking whether you've had enough sleep and food today."
        )


    # =========================================
    # DEFAULT
    # =========================================

    return (
        "I'm listening. Tell me a little more about how you're feeling "
        "or what's happening today."
    )