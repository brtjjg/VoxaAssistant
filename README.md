# WhatsApp AI Business Assistant

Complete WhatsApp chatbot with AI (OpenAI), lead management, broadcasts, analytics, and subscription plans.

## Features
- 🤖 AI-powered WhatsApp responses (GPT-3.5)
- 📊 Dashboard with analytics
- 👥 Lead management
- 📢 Broadcast messaging
- 🔔 Real-time notifications
- 💰 Subscription plans (Free/Starter/Pro)
- 🔒 Security logs & API keys
- 🌍 Multi-language & voice message support

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your credentials
6. Run: `python app.py`
7. Open `http://localhost:5000`

## Environment Variables
See `.env.example` for all required variables.

## Webhook Setup (WhatsApp)
- Use ngrok: `ngrok http 5000`
- Set webhook URL in Meta Developer App: `https://your-ngrok-url/webhook`
- Verify token = `WHATSAPP_VERIFY_TOKEN` value

## License
MIT
