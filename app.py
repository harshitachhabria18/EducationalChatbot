import os
import markdown
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, render_template, session
from flask_session import Session

# Load environment variables from .env file
load_dotenv()

print("Loaded API Key:", os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")

# Use server-side sessions to avoid 4KB cookie size limit
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = "/tmp/flask_session_data"
Session(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Create models once at startup
checker_model = genai.GenerativeModel(model_name)
main_model = genai.GenerativeModel(model_name)


@app.route("/", methods=["GET"])
def index():
    history = session.get("history", [])
    return render_template("form.html", history=history)


@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.form.get("prompt", "").strip()
    concise = request.form.get("concise") == "yes"

    # STEP 0: Block empty input
    if not user_input:
        history = session.get("history", [])
        return render_template("form.html", history=history)

    # STEP 1: Classify the question
    classification_prompt = (
        "Answer only 'yes' or 'no'.\n"
        "Is the following question something a student or curious person might want to learn about? "
        "This includes school subjects like science, math, history, geography, and language, "
        "but ALSO general knowledge topics like sports, nature, culture, technology, "
        "famous people, animals, current events, and everyday curiosities. "
        "Only say 'no' if the question is clearly non-educational such as personal chit-chat, "
        "jokes, or harmful requests.\n"
        "Do NOT say anything else.\n\n"
        f"Question: {user_input}"
    )

    try:
        check_response = checker_model.generate_content(classification_prompt)
        verdict = check_response.text.strip().lower()
        is_educational = verdict.startswith("yes")
    except Exception as e:
        history = session.get("history", [])
        history.append({
            "question": user_input,
            "answer": f"Classification error: {str(e)}",
            "is_error": True
        })
        session["history"] = history
        session.modified = True
        return render_template("form.html", history=history)

    # Load history from session
    history = session.get("history", [])

    # STEP 2: Reject non-educational questions
    if not is_educational:
        history.append({
            "question": user_input,
            "answer": "This chatbot only answers educational questions. Please ask something related to learning, subjects, or academics.",
            "is_error": True
        })
        session["history"] = history
        session.modified = True
        return render_template("form.html", history=history)

    # STEP 3: Build system instruction
    system_instruction = (
        "You are an expert educational assistant. "
        "Only provide helpful, accurate answers on educational topics like "
        "science, history, mathematics, geography, and language learning."
    )
    if concise:
        system_instruction += (
            " Keep your answer brief and to the point, "
            "but make sure all key concepts are still covered."
        )

    full_prompt = f"{system_instruction}\n\nUser: {user_input}"

    # STEP 4: Generate the answer
    try:
        response = main_model.generate_content(full_prompt)
        answer = markdown.markdown(response.text)
    except Exception as e:
        history.append({
            "question": user_input,
            "answer": f"Error generating response: {str(e)}",
            "is_error": True
        })
        session["history"] = history
        session.modified = True
        return render_template("form.html", history=history)

    # STEP 5: Save to session and return
    history.append({
        "question": user_input,
        "answer": answer,
        "is_error": False
    })
    session["history"] = history
    session.modified = True
    return render_template("form.html", history=history)


@app.route("/clear", methods=["POST"])
def clear_history():
    session.pop("history", None)
    session.modified = True
    return render_template("form.html", history=[])


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)