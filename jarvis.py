import logging
import os
import google.generativeai as genai
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"].strip()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
 model_name="gemini-2.5-flash",
 system_instruction=(
 "Eres Jarvis, un estratega experto en marketing digital. "
 "Ayudas a estructurar guiones, desglosar tiempos de edición y diseñar "
 "storytelling visual para formatos cortos como Instagram Reels y TikTok. "
 "Integras narrativas POV con gafas Meta Ray-Ban para campañas públicas "
 "y ayudas con el ecosistema digital, incluida la maquetación de "
 "plantillas de correo en HTML."
 ),
)
app = App(token=SLACK_BOT_TOKEN)
@app.event("app_mention")
def handle_mentions(body, say):
 event = body.get("event", {})
 text = event.get("text", "")
 bot_user_id = body.get("authorizations", [{}])[0].get("user_id")
 if bot_user_id:
 text = text.replace(f"<@{bot_user_id}>", "")
 prompt = text.strip()
 if not prompt:
 say("¡Hola! ¿En qué puedo ayudarte?")
 return
 try:
 # Conversación aislada por canal y usuario para evitar mezclar contextos.
 conversation_id = f"{event.get('channel')}:{event.get('user')}"
 chat = chats.setdefault(conversation_id, model.start_chat(history=[]))
 response = chat.send_message(prompt)
 answer = getattr(response, "text", None)
 say(answer or "No pude generar una respuesta de texto. Inténtalo de nuevo.")
 except Exception:
 logger.exception("Error al procesar la mención")
 say("Tuve un problema al procesar el mensaje. Inténtalo de nuevo.")
chats = {}
if __name__ == "__main__":
 logger.info("Jarvis conectado y escuchando en Slack vía Socket Mode...")
 SocketModeHandler(app, SLACK_APP_TOKEN).start()

