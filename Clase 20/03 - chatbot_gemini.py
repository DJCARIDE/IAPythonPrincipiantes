import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables del archivo .env
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise EnvironmentError("La variable de entorno GEMINI_API_KEY no está definida.")

genai.configure(api_key=gemini_api_key)

print("¡Gemini configurado!")

class Chatbot:
    def __init__(self, system_prompt: str):
        """Inicializa el chatbot con un prompt de sistema."""
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt,
        )
        self.chat = self.model.start_chat(history=[])

    def talk(self, user_message: str) -> str:
        """Envía un mensaje de usuario y obtiene una respuesta."""
        response = self.chat.send_message(user_message)
        if not response.text:
            raise RuntimeError("La API de Gemini no devolvió texto en la respuesta.")
        return response.text.strip()

# --- Punto de entrada de la aplicación ---
if __name__ == "__main__":
    mi_chatbot = Chatbot("Eres un asistente servicial y amigable.")
    print("Chatbot Gemini iniciado. Escribe 'salir' para terminar.")

    while True:
        entrada = input("Tú: ")
        if entrada.lower() == "salir":
            break

        respuesta = mi_chatbot.talk(entrada)
        print(f"Asistente: {respuesta}")
