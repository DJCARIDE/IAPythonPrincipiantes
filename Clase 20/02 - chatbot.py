import openai
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# La librería openai buscará esta variable de entorno por defecto
openai.api_key = os.getenv("OPENAI_API_KEY")

print("¡Librería configurada!")

class Chatbot:
    def __init__(self, system_prompt: str):
        """Inicializa el chatbot con un prompt de sistema."""
        self.messages = [{"role": "system", "content": system_prompt}]

    def talk(self, user_message: str) -> str:
        """Envía un mensaje de usuario y obtiene una respuesta."""
        self.messages.append({"role": "user", "content": user_message})

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages
        )

        assistant_response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response

# --- Punto de entrada de la aplicación ---
if __name__ == "__main__":
    # Ejercicio práctico para los alumnos:
    # 1. Cambiar el system_prompt para que el bot sea un traductor de Python a JavaScript.
    # 2. Hacer que el bot actúe como un personaje famoso.
    mi_chatbot = Chatbot("Eres un asistente servicial y amigable.")
    print("Chatbot iniciado. Escribe 'salir' para terminar.")

    while True:
        entrada = input("Tú: ")
        if entrada.lower() == "salir":
            break

        respuesta = mi_chatbot.talk(entrada)
        print(f"Asistente: {respuesta}")