import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Eres Jarvis, un estratega experto en marketing digital. Tu objetivo es ayudarme a estructurar guiones, desglosar tiempos de edición y diseñar storytelling visual para formatos cortos como Instagram Reels y TikTok. Integra formatos innovadores como narrativas en primera persona (POV) utilizando gafas Meta Ray-Ban para campañas públicas, y asísteme en el ecosistema digital completo, incluyendo la estructuración y maquetación de plantillas de correo en HTML."
)
chat = model.start_chat(history=[])

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mentions(body, say):
    event = body["event"]
    user_text = event["text"]
    prompt = user_text.split(">", 1)[1].strip() if ">" in user_text else user_text
    response = chat.send_message(prompt)
    say(response.text)

if __name__ == "__main__":
    print("Jarvis conectado y escuchando en Slack vía Railway...")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"].strip()).start()
