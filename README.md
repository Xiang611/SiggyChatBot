# Flask Gemini Chatbot

A simple chatbot powered by Google Gemini (free), ready to deploy on Render.com.

## Project Structure

```
flask-chatbot/
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Chat UI
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
└── README.md
```

## Customization

In `app.py`, find this line and change the system prompt to give your bot a personality:

```python
system="You are a helpful assistant.",  # 👈 Customize this!
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run the app
python app.py
```

Then open http://localhost:5000

## Deploy to Render (free)

1. Push this folder to a **GitHub repo**
2. Go to https://render.com and click **"New Web Service"**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — just click **Deploy**
5. Go to your service → **Environment** → add:
   - Key: `GEMINI_API_KEY`
   - Value: your key from https://aistudio.google.com
6. Redeploy — your chatbot is live at `https://your-app.onrender.com` 🎉

## Share with Testers

Just send them the Render URL. No login or install needed.
