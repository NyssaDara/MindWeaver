
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
        "name": "",
        "age": None,
        "blood_group": "",
        "mood_history": [],
        "chat_history": [],
        "tasks": [],
        "medications": [],
        "appointments": [],
        "health": {
            "heart_rate": None,
            "spo2": None,
            "steps": None,
            "sleep": None
        },
        "health_history": [],
        "wearable": {"name": "", "connected": False}
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.name == "Priya Sharma":
        st.session_state.name = ""
    if st.session_state.age == 26:
        st.session_state.age = None
    if st.session_state.blood_group == "O+":
        st.session_state.blood_group = ""

    if st.session_state.health in (
        {"heart_rate": 72, "spo2": 98, "steps": 8432, "sleep": 7.5},
        {"heart_rate": 76, "spo2": 98, "steps": 6421, "sleep": 7.0}
    ):
        st.session_state.health = {
            "heart_rate": None,
            "spo2": None,
            "steps": None,
            "sleep": None
        }

    default_task_schedule = {
        ("Drink water", "11:00 AM"),
        ("Take a short walk", "04:00 PM"),
        ("Read for 20 minutes", "07:00 PM"),
        ("Wind down for sleep", "10:30 PM")
    }
    if {
        (task["name"], task["time"])
        for task in st.session_state.tasks
    } == default_task_schedule:
        st.session_state.tasks = []

    if st.session_state.medications == [
        {"name": "Vitamin supplement", "time": "09:00 AM", "done": False}
    ]:
        st.session_state.medications = []

    if st.session_state.chat_history == [
        (
            "assistant",
            "Hey 💜 I'm here for you. "
            "How are you feeling today?"
        )
    ]:
        st.session_state.chat_history = []


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


def health_metric(value, suffix="", grouped=False):
    if value is None:
        return "—"
    if grouped:
        value = f"{int(value):,}"
    return f"{value}{suffix}"


def game_progress(game_name):
    progress = st.session_state.setdefault("game_progress", {})
    return progress.setdefault(game_name, {"score": 0, "level": 1})


def award_game_level(game_name, points):
    progress = game_progress(game_name)
    progress["score"] += points
    progress["level"] += 1


def valid_sudoku(board):
    required = set(range(1, 10))
    rows_valid = all(set(row) == required for row in board)
    columns_valid = all(
        {board[row][column] for row in range(9)} == required
        for column in range(9)
    )
    boxes_valid = all(
        {
            board[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        } == required
        for box_row in (0, 3, 6)
        for box_column in (0, 3, 6)
    )
    return rows_valid and columns_valid and boxes_valid


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("# ♡ MindWeaver")
    st.caption("Your mind. Your health. Your priority.")
    st.divider()

    page = st.radio(
        "MENU",
        [
            "Home",
            "Health & Wearables",
            "Mood & Wellbeing",
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
    st.markdown(f"**{st.session_state.name or 'Profile'}**")
    st.caption("Your personal wellbeing space")


# -------------------- HOME --------------------

if page == "Home":

    first_name = st.session_state.name.strip().split()
    hero(
        f"Hello, {first_name[0]} 🌷" if first_name else "Your dashboard 🌷",
        "Small steps every day can lead to big changes."
    )

    h = st.session_state.health

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Heart Rate", health_metric(h["heart_rate"], " bpm"))
    c2.metric("SpO₂", health_metric(h["spo2"], "%"))
    c3.metric("Steps Today", health_metric(h["steps"], grouped=True))
    c4.metric("Sleep", health_metric(h["sleep"], " hours"))

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
        a.metric("Mood", "—")
        b.metric(
            "Tasks Done",
            (
                f"{sum(t['done'] for t in st.session_state.tasks)}"
                f"/{len(st.session_state.tasks)}"
                if st.session_state.tasks else "—"
            )
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

 
# -------------------- HEALTH & WEARABLES --------------------

elif page == "Health & Wearables":

    hero(
        "Health & Wearables",
        "Enter health readings and wearable details in one place."
    )

    h = st.session_state.health
    wearable = st.session_state.wearable

    with st.form("health_wearable_form"):

        c1, c2 = st.columns(2)

        with c1:
            heart_rate = st.number_input(
                "Heart rate (bpm)",
                min_value=30,
                max_value=220,
                value=h["heart_rate"],
                placeholder="Not entered"
            )
            spo2 = st.number_input(
                "SpO₂ (%)",
                min_value=50,
                max_value=100,
                value=h["spo2"],
                placeholder="Not entered"
            )

        with c2:
            steps = st.number_input(
                "Steps today",
                min_value=0,
                max_value=100000,
                value=h["steps"],
                step=100,
                placeholder="Not entered"
            )
            sleep = st.number_input(
                "Sleep (hours)",
                min_value=0.0,
                max_value=24.0,
                value=h["sleep"],
                step=0.25,
                placeholder="Not entered"
            )

        st.subheader("Wearable")
        wearable_name = st.text_input(
            "Wearable name",
            value=wearable["name"],
            placeholder="e.g. Fitbit, Garmin, Apple Watch"
        )
        wearable_connected = st.checkbox(
            "This wearable is connected",
            value=wearable["connected"]
        )
        save = st.form_submit_button("Save")

    if save:
        if wearable_connected and not wearable_name.strip():
            st.error("Enter the wearable name before marking it connected.")
        else:
            st.session_state.wearable = {
                "name": wearable_name.strip(),
                "connected": wearable_connected
            }
            st.session_state.health = {
                "heart_rate": heart_rate,
                "spo2": spo2,
                "steps": steps,
                "sleep": sleep
            }

            if any(value is not None for value in st.session_state.health.values()):
                st.session_state.health_history.append({
                    "Date": str(date.today()),
                    "Heart Rate": heart_rate,
                    "SpO₂": spo2,
                    "Steps": steps,
                    "Sleep Hours": sleep
                })
            st.success("Saved for this session.")

    h = st.session_state.health

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Heart Rate", health_metric(h["heart_rate"], " bpm"))
    c2.metric("SpO₂", health_metric(h["spo2"], "%"))
    c3.metric("Steps", health_metric(h["steps"], grouped=True))
    c4.metric("Sleep", health_metric(h["sleep"], " hours"))

    wearable = st.session_state.wearable
    if wearable["name"]:
        status = "Connected" if wearable["connected"] else "Not connected"
        st.write(f"**{wearable['name']}** · {status}")
    st.caption("Connection status is self-reported; live device syncing is not available.")


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


# -------------------- HEALTH TRENDS --------------------

elif page == "Health Trends":

    hero(
        "Your Health Trends 📈",
        "Notice your patterns over time, not just one number."
    )

    import pandas as pd

    if not st.session_state.health_history:
        st.info("Your health trends will appear after you save readings.")
    else:
        df = pd.DataFrame(st.session_state.health_history).set_index("Date")
        tab1, tab2, tab3 = st.tabs(["Heart Rate", "Sleep", "Steps"])

        with tab1:
            chart_data = df["Heart Rate"].dropna()
            if not chart_data.empty:
                st.line_chart(chart_data)
            else:
                st.info("No heart rate readings yet.")

        with tab2:
            chart_data = df["Sleep Hours"].dropna()
            if not chart_data.empty:
                st.bar_chart(chart_data)
            else:
                st.info("No sleep readings yet.")

        with tab3:
            chart_data = df["Steps"].dropna()
            if not chart_data.empty:
                st.bar_chart(chart_data)
            else:
                st.info("No step readings yet.")



# -------------------- AI COMPANION --------------------

elif page == "AI Companion":

    hero(
        "Your AI Companion 💜",
        "A personalised space for emotional wellbeing and daily check-ins."
    )

    st.markdown("""
    <div class="mw-card">
        <h3>🌷 A little support, just for you</h3>
        <p>
            We're building a more personalised AI companion that can
            understand your wellbeing check-ins, offer thoughtful
            conversations, and help you reflect on your daily patterns.
        </p>
        <p class="muted">
            Designed to support self-reflection, not replace professional care.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "we are still working on this .. this will be added real soon"
    )

    st.markdown("### What's coming")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="mw-card">
            <h3>💬</h3>
            <b>Natural Conversations</b>
            <p class="muted">
                More meaningful, supportive conversations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="mw-card">
            <h3>🧠</h3>
            <b>Personalised Insights</b>
            <p class="muted">
                Wellbeing reflections informed by your recorded patterns.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="mw-card">
            <h3>🌸</h3>
            <b>Daily Check-ins</b>
            <p class="muted">
                Gentle prompts to reflect on how you're feeling.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "This feature is under active development and is not yet "
        "the complete AI companion experience."
    )


# -------------------- COMFORT VOICE --------------------

elif page == "Comfort Voice":

    hero(
        "Comfort Voice 🎙️",
        "A little comfort, in a voice that feels familiar."
    )

    st.markdown("""
    <div class="mw-card">
        <h3>💜 Comfort, in your own way</h3>
        <p>
            We're exploring a voice-based wellbeing experience designed
            to offer calming messages and a greater sense of familiarity
            during difficult moments.
        </p>
        <p class="muted">
            Any future use of a familiar person's voice will require
            their explicit permission.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "we are still working on this .. this will be added real soon"
    )

    st.markdown("### What's coming")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="mw-card">
            <h3>🎵 Comfort Audio</h3>
            <p class="muted">
                Calming audio and supportive messages for moments
                when you need a pause.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="mw-card">
            <h3>🫶 Familiar Voice Experience</h3>
            <p class="muted">
                An optional, permission-based familiar-voice experience
                planned for a future version.We are still working over it .. 
                Really sorry for inconvinience 
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "Voice personalisation is not available in this prototype yet. "
        "No voice cloning is performed by this page."
    )
# -------------------- GAMES --------------------
elif page == "Games":
    st.title("Logic Games")

    game = st.selectbox(
        "Choose a game",
        ["Number Memory", "Sudoku", "Pattern Logic"]
    )
    progress = game_progress(game)
    score_column, level_column = st.columns(2)
    score_column.metric("Score", progress["score"])
    level_column.metric("Level", progress["level"])

    if game == "Number Memory":
        level = progress["level"]
        challenge = st.session_state.get("number_memory_challenge")
        if not challenge or challenge["level"] != level:
            length = min(level + 2, 12)
            challenge = {
                "level": level,
                "digits": "".join(
                    str(random.randint(0, 9)) for _ in range(length)
                )
            }
            st.session_state.number_memory_challenge = challenge
            st.session_state.memory_is_revealed = True

        st.write(f"Memorize the {len(challenge['digits'])}-digit sequence.")
        if st.session_state.get("memory_is_revealed", True):
            st.code("   ".join(challenge["digits"]), language=None)
            if st.button("Hide sequence"):
                st.session_state.memory_is_revealed = False
                st.rerun()
        else:
            if st.button("Show sequence"):
                st.session_state.memory_is_revealed = True
                st.rerun()

            with st.form(f"memory_form_{level}"):
                answer = st.text_input("Enter the sequence", max_chars=12)
                submitted = st.form_submit_button("Check answer")

            if submitted:
                if answer.strip() == challenge["digits"]:
                    award_game_level(game, 10)
                    st.session_state.memory_is_revealed = True
                    st.success("Correct. Level complete.")
                    st.rerun()
                else:
                    st.error("Not quite. Try again.")

    elif game == "Pattern Logic":
        level = progress["level"]
        scale = 1 + (level - 1) // 5
        patterns = [
            ([2, 4, 6, 8], 10),
            ([3, 6, 9, 12], 15),
            ([1, 4, 9, 16], 25),
            ([1, 1, 2, 3, 5], 8),
            ([2, 5, 7, 10, 12], 15)
        ]
        sequence, answer = patterns[(level - 1) % len(patterns)]
        sequence = [number * scale for number in sequence]
        answer *= scale
        options = sorted({answer - 2 * scale, answer, answer + scale, answer + 3 * scale})

        st.write("Find the next number in the sequence:")
        st.markdown("### " + "  ·  ".join(map(str, sequence)) + "  ·  ?")
        with st.form(f"pattern_form_{level}"):
            selected = st.radio(
                "Next number",
                options,
                horizontal=True,
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("Submit answer")

        if submitted:
            if selected == answer:
                award_game_level(game, 10)
                st.success("Correct. Level complete.")
                st.rerun()
            else:
                st.error("Not quite. Look for the rule and try again.")

    else:
        level = progress["level"]
        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        extra_blanks = [
            (0, 1), (1, 0), (2, 1), (3, 0), (4, 3), (5, 0),
            (6, 1), (7, 3), (8, 4), (0, 4), (1, 3), (2, 2),
            (3, 4), (4, 0), (5, 4), (6, 6), (7, 5), (8, 7)
        ]
        for row, column in extra_blanks[:min((level - 1) * 3, len(extra_blanks))]:
            puzzle[row][column] = 0

        st.write("Complete each row, column, and 3×3 box with numbers 1–9.")
        with st.form(f"sudoku_form_{level}"):
            board = []
            for row_index, row in enumerate(puzzle):
                columns = st.columns(9, gap="small")
                board_row = []
                for column_index, value in enumerate(row):
                    cell_key = f"sudoku_{level}_{row_index}_{column_index}"
                    with columns[column_index]:
                        cell_value = st.number_input(
                            f"Row {row_index + 1}, column {column_index + 1}",
                            min_value=0,
                            max_value=9,
                            value=value if value else st.session_state.get(cell_key, 0),
                            step=1,
                            key=cell_key,
                            label_visibility="collapsed",
                            disabled=value != 0
                        )
                    board_row.append(cell_value)
                board.append(board_row)
            submitted = st.form_submit_button("Check Sudoku")

        if submitted:
            if valid_sudoku(board):
                award_game_level(game, 25)
                st.success("Solved. Level complete.")
                st.rerun()
            else:
                st.error("The grid is incomplete or has a conflict. Keep going.")


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
            min_value=1,
            max_value=120,
            value=st.session_state.age,
            placeholder="Not entered"
        )

        blood_groups = [
            "", "Unknown", "A+", "A-", "B+", "B-",
            "AB+", "AB-", "O+", "O-"
        ]
        blood_group = st.selectbox(
            "Blood group",
            blood_groups,
            index=(
                blood_groups.index(st.session_state.blood_group)
                if st.session_state.blood_group in
                blood_groups
                else 0
            ),
            format_func=lambda value: value or "Select blood group"
        )

        save = st.form_submit_button("Save Profile")

    if save:

        st.session_state.name = name.strip()
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