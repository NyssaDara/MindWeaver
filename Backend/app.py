from flask import Flask, request, jsonify
from flask_cors import CORS

from database import get_connection
from digital_twin import calculate_digital_twin
from chatbot import generate_response


app = Flask(__name__)
CORS(app)


# ==========================================
# HOME / HEALTH CHECK
# ==========================================

@app.route("/")
def home():
    return "MindWeaver Backend is running!"


# ==========================================
# REGISTER USER
# ==========================================

@app.route("/api/register", methods=["POST"])
def register_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    blood_group = data.get("blood_group")
    medical_history = data.get("medical_history")
    medications = data.get("medications")

    if not name or age is None:
        return jsonify({
            "success": False,
            "message": "Name and age are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO users
        (name, age, gender, blood_group, medical_history, medications)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        name,
        age,
        gender,
        blood_group,
        medical_history,
        medications
    ))

    connection.commit()

    user_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user_id": user_id
    }), 201


# ==========================================
# GET USER PROFILE
# ==========================================

@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "user": user
    })


# ==========================================
# ADD HEALTH DATA
# ==========================================

@app.route("/api/health", methods=["POST"])
def add_health_data():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    user_id = data.get("user_id")
    heart_rate = data.get("heart_rate")
    spo2 = data.get("spo2")
    steps = data.get("steps")
    sleep_hours = data.get("sleep_hours")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "user_id is required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO health_data
        (user_id, heart_rate, spo2, steps, sleep_hours)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_id,
        heart_rate,
        spo2,
        steps,
        sleep_hours
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Health data added successfully"
    }), 201


# ==========================================
# GET LATEST HEALTH DATA
# ==========================================

@app.route("/api/health/<int:user_id>", methods=["GET"])
def get_health_data(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM health_data
        WHERE user_id = %s
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (user_id,))

    health = cursor.fetchone()

    cursor.close()
    connection.close()

    if not health:
        return jsonify({
            "success": False,
            "message": "No health data found"
        }), 404

    return jsonify({
        "success": True,
        "health": health
    })


# ==========================================
# HEALTH HISTORY
# ==========================================

@app.route("/api/health/<int:user_id>/history", methods=["GET"])
def health_history(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM health_data
        WHERE user_id = %s
        ORDER BY recorded_at DESC
    """, (user_id,))

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "history": history
    })


# ==========================================
# ADD MOOD DATA
# ==========================================

@app.route("/api/mood", methods=["POST"])
def add_mood():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    user_id = data.get("user_id")
    mood = data.get("mood")
    stress_level = data.get("stress_level")
    anxiety_level = data.get("anxiety_level")
    symptoms = data.get("symptoms")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "user_id is required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO mood_data
        (user_id, mood, stress_level, anxiety_level, symptoms)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_id,
        mood,
        stress_level,
        anxiety_level,
        symptoms
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Mood data added successfully"
    }), 201


# ==========================================
# GET MOOD DATA
# ==========================================

@app.route("/api/mood/<int:user_id>", methods=["GET"])
def get_mood(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM mood_data
        WHERE user_id = %s
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (user_id,))

    mood = cursor.fetchone()

    cursor.close()
    connection.close()

    if not mood:
        return jsonify({
            "success": False,
            "message": "No mood data found"
        }), 404

    return jsonify({
        "success": True,
        "mood": mood
    })


# ==========================================
# SCREEN TIME
# ==========================================

@app.route("/api/screen-time", methods=["POST"])
def add_screen_time():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    user_id = data.get("user_id")
    total_minutes = data.get("total_minutes")

    if not user_id or total_minutes is None:
        return jsonify({
            "success": False,
            "message": "user_id and total_minutes are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO screen_time
        (user_id, total_minutes)
        VALUES (%s, %s)
    """, (
        user_id,
        total_minutes
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Screen time added successfully"
    }), 201


@app.route("/api/screen-time/<int:user_id>", methods=["GET"])
def get_screen_time(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM screen_time
        WHERE user_id = %s
        ORDER BY recorded_date DESC
    """, (user_id,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "screen_time": data
    })


# ==========================================
# APP USAGE
# ==========================================

@app.route("/api/app-usage", methods=["POST"])
def add_app_usage():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    user_id = data.get("user_id")
    app_name = data.get("app_name")
    usage_minutes = data.get("usage_minutes")

    if not user_id or not app_name or usage_minutes is None:
        return jsonify({
            "success": False,
            "message": "user_id, app_name and usage_minutes are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO app_usage
        (user_id, app_name, usage_minutes)
        VALUES (%s, %s, %s)
    """, (
        user_id,
        app_name,
        usage_minutes
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "App usage added successfully"
    }), 201


@app.route("/api/app-usage/<int:user_id>", methods=["GET"])
def get_app_usage(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM app_usage
        WHERE user_id = %s
        ORDER BY recorded_date DESC
    """, (user_id,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "app_usage": data
    })


# ==========================================
# DAILY TASKS
# ==========================================

@app.route("/api/tasks", methods=["POST"])
def add_task():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    user_id = data.get("user_id")
    task = data.get("task")
    task_date = data.get("task_date")

    if not user_id or not task or not task_date:
        return jsonify({
            "success": False,
            "message": "user_id, task and task_date are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO daily_tasks
        (user_id, task, task_date)
        VALUES (%s, %s, %s)
    """, (
        user_id,
        task,
        task_date
    ))

    connection.commit()

    task_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Task added successfully",
        "task_id": task_id
    }), 201


@app.route("/api/tasks/<int:user_id>", methods=["GET"])
def get_tasks(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM daily_tasks
        WHERE user_id = %s
        ORDER BY task_date DESC, id DESC
    """, (user_id,))

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "tasks": tasks
    })


@app.route("/api/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE daily_tasks
        SET completed = TRUE
        WHERE id = %s
    """, (task_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Task marked as completed"
    })


# ==========================================
# DIGITAL TWIN
# ==========================================

@app.route("/api/digital-twin/<int:user_id>", methods=["GET"])
def get_digital_twin(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Latest health data
    cursor.execute("""
        SELECT *
        FROM health_data
        WHERE user_id = %s
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (user_id,))

    health = cursor.fetchone()

    # Latest mood data
    cursor.execute("""
        SELECT *
        FROM mood_data
        WHERE user_id = %s
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (user_id,))

    mood = cursor.fetchone()

    # Latest screen time
    cursor.execute("""
        SELECT total_minutes
        FROM screen_time
        WHERE user_id = %s
        ORDER BY recorded_date DESC
        LIMIT 1
    """, (user_id,))

    screen_data = cursor.fetchone()

    screen_time = None

    if screen_data:
        screen_time = screen_data["total_minutes"]

    cursor.close()
    connection.close()

    result = calculate_digital_twin(
        health=health,
        mood=mood,
        screen_time=screen_time
    )

    return jsonify({
        "success": True,
        "digital_twin": result
    })


# ==========================================
# CHATBOT
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({
            "success": False,
            "message": "user_id and message are required"
        }), 400

    response = generate_response(message)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (user_id, user_message, bot_response)
        VALUES (%s, %s, %s)
    """, (
        user_id,
        message,
        response
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "response": response
    })


@app.route("/api/chat/<int:user_id>", methods=["GET"])
def get_chat_history(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM chat_history
        WHERE user_id = %s
        ORDER BY created_at ASC
    """, (user_id,))

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "history": history
    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )