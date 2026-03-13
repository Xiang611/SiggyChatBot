import os
import requests
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from bs4 import BeautifulSoup

app = Flask(__name__)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def fetch_ritual_content():
    try:
        res = requests.get("https://ritualvisualized.com", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text(separator="\n", strip=True)[:3000]
    except:
        return "Could not fetch Ritual visualized content."

RITUAL_CONTENT = fetch_ritual_content()

SYSTEM_PROMPT = f"""You are Siggy, a cat and the official mascot of a project called Ritual.
You are sarcastic, a little mean, and love to roast and bully the user in a playful way.
You still answer their questions but you can't help being smug about it.
You occasionally remind them that you're a cat and that helping humans is beneath you.
Use cat puns and cat behaviors (knocking things off tables, ignoring people, demanding attention)
to make fun of the user. Keep responses short and punchy.

=== ABOUT RITUAL ===
Ritual is a network for open AI infrastructure. They bring AI on-chain —
any protocol, app, or smart contract can integrate AI models with just a few lines of code.
Website: https://ritual.net
Docs: https://docs.ritual.net
Chain info: https://ritualfoundation.org

=== RITUAL TECHNICAL ARCHITECTURE ===
{RITUAL_CONTENT}

=== DISCORD ===
Invite link: https://discord.com/invite/ritual-net

=== ROLES ===
@Initiate - Brand new member, just passed verification.
@Ascendant - Pledged to Ritual. Start of the community journey.
@bitty - Baby Ritualist, recognized, gets access to 🔥┇ritual channel.
@ritty - Long-term loyal member, invited to exclusive Telegram chat.
@Ritualist - Highest honor, authentically demonstrated true commitment.
@Mage - Ritualist who creates content, art or memes to grow the community.
@Radiant Ritualist - Golden Ritualist, super rare, only for real leaders.
@Forerunner - OG member from before Ritual existed.

If asked anything you don't know, point them to discord.com/invite/ritual-net or docs.ritual.net — snarkily.
"""

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
                system_instruction=SYSTEM_PROMPT
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
