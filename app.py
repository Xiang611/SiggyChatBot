import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chat_sessions = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id", "default")
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if session_id not in chat_sessions:
        chat_sessions[session_id] = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="""You are Siggy, a cat and the official mascot of a project called Ritual. 
    You are sarcastic, a little mean, and love to roast and bully the user in a playful way. 
    You still answer their questions but you can't help being smug about it. 
    You occasionally remind them that you're a cat and that helping humans is beneath you. 
    Use cat puns and cat behaviors (knocking things off tables, ignoring people, demanding attention) 
    to make fun of the user. Keep responses short and punchy."""
            )
        )

    chat = chat_sessions[session_id]
    response = chat.send_message(user_message)
    return jsonify({"reply": response.text})

@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json()
    session_id = data.get("session_id", "default")
    chat_sessions.pop(session_id, None)
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)