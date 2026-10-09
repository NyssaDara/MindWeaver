
import os
import random
from datetime import date, time, timedelta

import streamlit as st
import requests

st.set_page_config(
    page_title="MindWeaver",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = os.getenv(
    "MINDWEAVER_API_BASE",
    "http://127.0.0.1:5000"
)

# -------------------- CUSTOM DESIGN --------------------

st.markdown("""
<style>
@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;600;700;800&display=swap'
);

.stApp {
    background: linear-gradient(
        135deg, #fffaff, #f7f2ff, #fff5fa
    );
    color: #30294f;
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    color: #39316f;
    font-family: 'Manrope', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #f0e8ff, #fff5fb
    );
    border-right: 1px solid #e7dcf6;
}

[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 18px;
    border: 1px solid #eee4f8;
    box-shadow: 0 4px 16px #6d54a410;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: linear-gradient(
        100deg, #5544b5, #8065d8
    );
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
}

div.stButton > button:hover {
    color: white;
    border: none;
}

.mw-hero {
    background: linear-gradient(
        110deg, #eee6ff, #fff0f7
    );
    border: 1px solid #e9ddf7;
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 20px;
}

.mw-card {
    background: rgba(255,255,255,0.9);
    border: 1px solid #eee4f8;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 12px;
}

.muted {
    color: #77718f;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# -------------------- SESSION DATA --------------------

def initialize():
    defaults = {
        "name": "Priya Sharma",
        "age": 26,
        "blood_group": "O+",
        "mood_history": [],
        "chat_history": [
            (
                "assistant",
                "Hey 💜 I'm here for you. "
                "How are you feeling today?"
            )
        ],
        "tasks": [
            {"name": "Drink water", "time": "11:00 AM", "done": False},
            {"name": "Take a short walk", "time": "04:00 PM", "done": False},
            {"name": "Read for 20 minutes", "time": "07:00 PM", "done": False},
            {"name": "Wind down for sleep", "time": "10:30 PM", "done": False}
        ],
        "medications": [
            {"name": "Vitamin supplement", "time": "09:00 AM", "done": False}
        ],
        "appointments": [],
        "health": {
            "heart_rate": 72,
            "spo2": 98,
            "steps": 8432,
            "sleep": 7.5
        }
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize()


# -------------------- HELPER FUNCTIONS --------------------

def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="mw-hero">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def api_post(endpoint, payload):
    """Send data to Flask when the backend is running."""
    try:
        response = requests.post(
            f"{API_BASE}{endpoint}",
            json=payload,
            timeout=3
        )
        return response.ok, response.json()
    except Exception:
        return False, {}


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("# ♡ MindWeaver")
    st.caption("Your mind. Your health. Your priority.")
    st.divider()

    page = st.radio(
        "MENU",
        [
            "Home",
            "Health",
            "Mood & Wellbeing",
            "Wearables",
            "Health Trends",
            "AI Companion",
            "Comfort Voice",
            "Games",
            "Pregnancy Care",
            "Medications",
            "Appointments",
            "Daily Tasks",
            "Reports & Insights",
            "Settings"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(f"**{st.session_state.name}**")
    st.caption("Your personal wellbeing space")


# -------------------- HOME --------------------

if page == "Home":

    hero(
        f"Hello, {st.session_state.name.split()[0]} 🌷",
        "Small steps every day can lead to big changes."
    )

    h = st.session_state.health

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Heart Rate", f"{h['heart_rate']} bpm")
    c2.metric("SpO₂", f"{h['spo2']}%")
    c3.metric("Steps Today", f"{h['steps']:,}")
    c4.metric("Sleep", f"{h['sleep']} hours")

    st.markdown("### Your Health, Our Priority")

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("""
        <div class="mw-card">
            <h3>🌸 Your Daily Summary</h3>
            <p class="muted">
                Take a moment to check in with yourself.
                Your health is about more than numbers.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Today's Focus")

        a, b, c = st.columns(3)
        a.metric("Mood", "Good")
        b.metric(
            "Tasks Done",
            f"{sum(t['done'] for t in st.session_state.tasks)}"
            f"/{len(st.session_state.tasks)}"
        )
        c.metric("Check-ins", len(st.session_state.mood_history))

    with right:
        st.markdown("""
        <div class="mw-card">
            <h3>💜 A Little Reminder</h3>
            Drink some water, take a screen break,
            and remember to be kind to yourself.
        </div>
        """, unsafe_allow_html=True)

    st.info("The health values shown here are sample demo data.")


# -------------------- HEALTH --------------------

elif page == "Health":

    hero(
        "Your Health Overview 💗",
        "Keep your health information together in one place."
    )

    h = st.session_state.health

    with st.form("health_form"):

        c1, c2 = st.columns(2)

        with c1:
            heart_rate = st.number_input(
                "Heart rate (bpm)", 30, 220,
                int(h["heart_rate"])
            )
            spo2 = st.number_input(
                "SpO₂ (%)", 50, 100,
                int(h["spo2"])
            )

        with c2:
            steps = st.number_input(
                "Steps today", 0, 100000,
                int(h["steps"]), step=100
            )
            sleep = st.number_input(
                "Sleep (hours)", 0.0, 24.0,
                float(h["sleep"]), step=0.25
            )

        save = st.form_submit_button("Save Health Check-in")

    if save:
        st.session_state.health = {
            "heart_rate": heart_rate,
            "spo2": spo2,
            "steps": steps,
            "sleep": sleep
        }

        st.success("Health check-in saved for this session!")

        st.caption(
            "To save to MySQL, connect this form to your Flask API."
        )

    h = st.session_state.health

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Heart Rate", f"{h['heart_rate']} bpm")
    c2.metric("SpO₂", f"{h['spo2']}%")
    c3.metric("Steps", f"{h['steps']:,}")
    c4.metric("Sleep", f"{h['sleep']} hours")

    st.caption(
        "These are manually entered values, not live medical readings."
    )


# -------------------- MOOD --------------------

elif page == "Mood & Wellbeing":

    hero(
        "How Are You Feeling? 🌼",
        "There's no right or wrong answer. Just check in with yourself."
    )

    with st.form("mood_form"):

        mood = st.select_slider(
            "Your mood today",
            options=["Very Low", "Low", "Okay", "Good", "Great"],
            value="Good"
        )

        c1, c2 = st.columns(2)

        with c1:
            stress = st.slider("Stress level", 0, 10, 4)

        with c2:
            anxiety = st.slider("Anxiety level", 0, 10, 3)

        note = st.text_area(
            "Anything on your mind?",
            placeholder="A busy day, feeling tired, something good..."
        )

        save = st.form_submit_button("Save Check-in")

    if save:
        entry = {
            "date": str(date.today()),
            "mood": mood,
            "stress": stress,
            "anxiety": anxiety,
            "note": note
        }

        st.session_state.mood_history.append(entry)
        st.success("Thanks for checking in with yourself 💜")

    st.markdown("### Your Recent Check-ins")

    if st.session_state.mood_history:
        st.dataframe(
            st.session_state.mood_history[::-1],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Your saved mood check-ins will appear here.")

    st.caption(
        "This feature supports self-reflection; it does not diagnose "
        "mental-health conditions."
    )


# -------------------- WEARABLES --------------------

elif page == "Wearables":

    hero(
        "Your Wearables ⌚",
        "Bring supported health readings together."
    )

    st.markdown("""
    <div class="mw-card">
        <h3>⌚ Demo Wearable</h3>
        <p class="muted">
            Sample device readings are shown below.
            Live readings need a supported device integration
            and user permission.
        </p>
    </div>
    """, unsafe_allow_html=True)

    h = st.session_state.health

    a, b, c = st.columns(3)
    a.metric("Heart Rate", f"{h['heart_rate']} bpm")
    b.metric("SpO₂", f"{h['spo2']}%")
    c.metric("Steps", f"{h['steps']:,}")

    st.subheader("Add a Sample Reading")

    with st.form("wearable_form"):
        whr = st.number_input("Heart rate", 30, 220, 76)
        wspo = st.number_input("SpO₂", 50, 100, 98)
        wsteps = st.number_input("Steps", 0, 100000, 6421)
        wsleep = st.number_input("Sleep hours", 0.0, 24.0, 7.0)

        save = st.form_submit_button("Save Reading")

    if save:
        st.session_state.health = {
            "heart_rate": whr,
            "spo2": wspo,
            "steps": wsteps,
            "sleep": wsleep
        }
        st.success("Sample reading saved.")


# -------------------- HEALTH TRENDS --------------------

elif page == "Health Trends":

    hero(
        "Your Health Trends 📈",
        "Notice your patterns over time, not just one number."
    )

    import pandas as pd

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Heart Rate": [75, 73, 77, 72, 74, 71, 72],
        "Sleep Hours": [6.8, 7.1, 6.5, 7.6, 7.2, 8.0, 7.5],
        "Steps": [5200, 6100, 4900, 7800, 7200, 9100, 8432]
    })

    tab1, tab2, tab3 = st.tabs(
        ["Heart Rate", "Sleep", "Steps"]
    )

    with tab1:
        st.line_chart(df.set_index("Day")[["Heart Rate"]])

    with tab2:
        st.bar_chart(df.set_index("Day")[["Sleep Hours"]])

    with tab3:
        st.bar_chart(df.set_index("Day")[["Steps"]])

    st.caption("Illustrative demo trends, not live wearable data.")


# -------------------- AI COMPANION --------------------

elif page == "AI Companion":

    hero(
        "Your AI Companion 💜",
        "A friendly space to talk about how you're feeling."
    )

    st.caption(
        "This prototype uses simple response rules, not a trained AI model."
    )

    for role, message in st.session_state.chat_history:
        with st.chat_message(
            role,
            avatar="💜" if role == "assistant" else "🌷"
        ):
            st.write(message)

    prompt = st.chat_input("Tell me what's on your mind...")

    if prompt:

        st.session_state.chat_history.append(("user", prompt))

        text = prompt.lower()

        if any(w in text for w in ["sad", "low", "lonely", "cry"]):
            reply = (
                "I'm sorry things feel heavy right now. 💜 "
                "Would you like to talk about what's been happening?"
            )

        elif any(w in text for w in ["stress", "pressure", "overwhelmed"]):
            reply = (
                "That sounds like a lot to handle. "
                "Take a slow breath. Is there one small thing "
                "you could make easier for yourself right now?"
            )

        elif any(w in text for w in ["sleep", "tired", "exhausted"]):
            reply = (
                "Rest matters. If possible, give yourself some "
                "quiet time and a gentle wind-down routine."
            )

        elif any(w in text for w in ["anxiety", "anxious", "worried"]):
            reply = (
                "Let's take it one moment at a time. "
                "Notice five things around you and breathe slowly. "
                "If this keeps happening, consider reaching out "
                "to someone you trust or a professional."
            )

        elif any(w in text for w in ["hi", "hello", "hey"]):
            reply = "Hey 💜 How are you feeling today?"

        else:
            reply = (
                "I'm listening. Tell me a little more, "
                "if you feel comfortable. We can think through "
                "one small next step together."
            )

        st.session_state.chat_history.append(
            ("assistant", reply)
        )

        st.rerun()


# -------------------- COMFORT VOICE --------------------

elif page == "Comfort Voice":

    hero(
        "Comfort Voice 🎙️",
        "A familiar voice can make a moment feel a little warmer."
    )

    st.info(
        "Only use recordings shared with the person's permission. "
        "This prototype previews audio; it does not clone voices."
    )

    audio = st.file_uploader(
        "Upload a voice recording",
        type=["wav", "mp3", "m4a", "ogg"]
    )

    if audio:
        st.audio(audio)
        st.success("Your audio preview is ready.")


# -------------------- GAMES --------------------

elif page == "Games":

    hero(
        "Little Moments, Big Focus 🧩",
        "Try a short activity for memory, attention, or relaxation."
    )

    game = st.selectbox(
        "Choose a game",
        [
            "Memory Match",
            "Focus & Find",
            "Breathing Zone",
            "Daily Recall"
        ]
    )

    if game == "Memory Match":

        sequence = st.session_state.get(
            "memory_sequence",
            ["🌸", "🌙", "🦋"]
        )

        st.write("Remember this sequence:")

        st.markdown("## " + "   ".join(sequence))

        answer = st.text_input(
            "Type the emojis in the same order"
        )

        if st.button("Check Answer"):
            if answer.replace(" ", "") == "".join(sequence):
                st.success("You got it! Great job 💜")
            else:
                st.info("Not quite. Take your time and try again.")

        if st.button("New Sequence"):
            st.session_state.memory_sequence = random.sample(
                ["🌸", "🌙", "🦋", "🍃", "⭐", "💜"], 3
            )
            st.rerun()

    elif game == "Focus & Find":

        st.write("Find the special flower 🌼")

        options = random.sample(
            ["🌷", "🌼", "🌙", "🍃", "🌸", "⭐"], 6
        )

        cols = st.columns(6)

        for i, option in enumerate(options):
            with cols[i]:
                if st.button(option, key=f"focus_{i}"):
                    if option == "🌼":
                        st.success("You found it!")
                    else:
                        st.info("Good try! Look again.")

    elif game == "Breathing Zone":

        st.markdown("### Breathe in · Hold · Breathe out")

        st.write(
            "Try breathing in for 4 seconds, holding gently "
            "for 4, and breathing out for 6. Stop if uncomfortable."
        )

        if st.button("Start Breathing Exercise"):
            st.success(
                "Relax your shoulders. Breathe slowly and comfortably."
            )

    else:

        st.write("Recall three things from your day.")

        recall = st.text_area("Your daily recall")

        if st.button("Save Recall"):
            st.session_state.daily_recall = recall
            st.success("Your recall was saved for this session.")


# -------------------- PREGNANCY CARE --------------------

elif page == "Pregnancy Care":

    hero(
        "Pregnancy Care 🌷",
        "An optional place to keep pregnancy notes and appointments."
    )

    st.info(
        "Optional tracking support only. It does not diagnose "
        "pregnancy complications or replace medical care."
    )

    with st.form("pregnancy_form"):

        enabled = st.checkbox("Enable pregnancy tracking")

        lmp = st.date_input(
            "First day of last menstrual period",
            value=date.today()
        )

        symptoms = st.text_area("Symptoms or personal notes")

        weight = st.number_input(
            "Weight (kg, optional)",
            min_value=0.0,
            max_value=300.0,
            value=0.0
        )

        save = st.form_submit_button("Save Pregnancy Notes")

    if save:
        st.session_state.pregnancy_enabled = enabled
        st.session_state.lmp = lmp
        st.session_state.pregnancy_notes = symptoms
        st.session_state.pregnancy_weight = weight
        st.success("Pregnancy notes saved for this session.")

    if st.session_state.get("pregnancy_enabled", False):

        days = max(
            0,
            (date.today() - st.session_state.lmp).days
        )

        st.metric(
            "Estimated gestational age",
            f"{days // 7} weeks + {days % 7} days"
        )

        st.caption(
            "This is a rough date-based estimate. "
            "Confirm dates with a healthcare professional."
        )


# -------------------- MEDICATIONS --------------------

elif page == "Medications":

    hero(
        "Medications & Vitamins 💊",
        "Keep track of the reminders you choose to manage."
    )

    for i, med in enumerate(st.session_state.medications):

        c1, c2, c3 = st.columns([3, 2, 1])

        c1.write(f"**{med['name']}**")
        c2.write(med["time"])

        st.session_state.medications[i]["done"] = c3.checkbox(
            "Taken",
            value=med["done"],
            key=f"med_{i}"
        )

        st.divider()

    with st.form("add_medication"):

        name = st.text_input("Medication or vitamin")
        med_time = st.time_input(
            "Reminder time",
            value=time(9, 0)
        )

        add = st.form_submit_button("Add Reminder")

    if add and name.strip():

        st.session_state.medications.append({
            "name": name.strip(),
            "time": med_time.strftime("%I:%M %p"),
            "done": False
        })

        st.success("Reminder added.")
        st.rerun()


# -------------------- APPOINTMENTS --------------------

elif page == "Appointments":

    hero(
        "Doctor Appointments 🩺",
        "Keep upcoming visits and follow-ups in one place."
    )

    for appointment in st.session_state.appointments:

        st.markdown(
            f"""
            <div class="mw-card">
                <h3>{appointment['doctor']}</h3>
                <p>{appointment['when']}</p>
                <p class="muted">{appointment['reason']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.form("appointment_form"):

        doctor = st.text_input("Doctor's name")

        appt_date = st.date_input(
            "Appointment date",
            value=date.today() + timedelta(days=7)
        )

        appt_time = st.time_input(
            "Appointment time",
            value=time(10, 30)
        )

        reason = st.text_input("Reason for appointment")

        save = st.form_submit_button("Save Appointment")

    if save and doctor.strip():

        st.session_state.appointments.append({
            "doctor": doctor.strip(),
            "when": (
                f"{appt_date.strftime('%d %b %Y')} · "
                f"{appt_time.strftime('%I:%M %p')}"
            ),
            "reason": reason or "General appointment"
        })

        st.success("Appointment saved.")
        st.rerun()


# -------------------- DAILY TASKS --------------------

elif page == "Daily Tasks":

    hero(
        "Your Daily Tasks ☑️",
        "Small steps count. Choose what feels doable today."
    )

    completed = sum(
        task["done"] for task in st.session_state.tasks
    )

    total = len(st.session_state.tasks)

    st.progress(
        completed / max(total, 1),
        text=f"{completed} of {total} tasks completed"
    )

    for i, task in enumerate(st.session_state.tasks):

        st.session_state.tasks[i]["done"] = st.checkbox(
            f"{task['name']} · {task['time']}",
            value=task["done"],
            key=f"task_{i}"
        )

    with st.form("add_task"):

        task_name = st.text_input(
            "Add a task",
            placeholder="Take a short walk..."
        )

        task_time = st.time_input(
            "Time",
            value=time(17, 0)
        )

        add = st.form_submit_button("Add Task")

    if add and task_name.strip():

        st.session_state.tasks.append({
            "name": task_name.strip(),
            "time": task_time.strftime("%I:%M %p"),
            "done": False
        })

        st.success("Task added.")
        st.rerun()


# -------------------- REPORTS --------------------

elif page == "Reports & Insights":

    hero(
        "Reports & Insights ✨",
        "A simple snapshot of your saved check-ins and daily routine."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Mood Check-ins",
        len(st.session_state.mood_history)
    )

    c2.metric(
        "Tasks Completed",
        f"{sum(t['done'] for t in st.session_state.tasks)}"
        f"/{len(st.session_state.tasks)}"
    )

    c3.metric(
        "Appointments",
        len(st.session_state.appointments)
    )

    if st.session_state.mood_history:
        st.subheader("Mood History")

        st.dataframe(
            st.session_state.mood_history,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "A few entries cannot establish a reliable health pattern. "
        "Use this page for reflection, not diagnosis."
    )

    summary = {
        "name": st.session_state.name,
        "mood_history": st.session_state.mood_history,
        "tasks": st.session_state.tasks,
        "appointments": st.session_state.appointments
    }

    import json

    st.download_button(
        "Download My Summary",
        data=json.dumps(summary, indent=2),
        file_name="mindweaver_summary.json",
        mime="application/json"
    )


# -------------------- SETTINGS --------------------

elif page == "Settings":

    hero(
        "Your Settings ⚙️",
        "Make your MindWeaver profile feel like yours."
    )

    with st.form("profile_form"):

        name = st.text_input(
            "Full name",
            value=st.session_state.name
        )

        age = st.number_input(
            "Age",
            1, 120,
            int(st.session_state.age)
        )

        blood_group = st.selectbox(
            "Blood group",
            ["Unknown", "A+", "A-", "B+", "B-",
             "AB+", "AB-", "O+", "O-"],
            index=(
                ["Unknown", "A+", "A-", "B+", "B-",
                 "AB+", "AB-", "O+", "O-"].index(
                    st.session_state.blood_group
                )
                if st.session_state.blood_group in
                ["Unknown", "A+", "A-", "B+", "B-",
                 "AB+", "AB-", "O+", "O-"]
                else 0
            )
        )

        save = st.form_submit_button("Save Profile")

    if save:

        st.session_state.name = name.strip() or "Friend"
        st.session_state.age = age
        st.session_state.blood_group = blood_group

        st.success("Profile updated.")
        st.rerun()

    st.divider()

    st.subheader("Privacy")

    st.write(
        "Use fictional information for your hackathon demo. "
        "Do not enter real sensitive health data without "
        "appropriate consent and security."
    )


# -------------------- FOOTER --------------------

st.divider()

st.caption(
    "MindWeaver 💜 · Prototype demo · "
    "Not a medical diagnosis or replacement for professional care."
)