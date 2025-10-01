import os
from dotenv import load_dotenv
from groq import Groq

# Cargar las variables de entorno (la API key)
load_dotenv()

# Configurar el cliente de Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def extraer_datos_contacto(texto):
    print("\n🤖 Pidiendo a la IA que extraiga datos en formato JSON...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Tu tarea es extraer el nombre, email y empresa de un texto. Debes devolver la información únicamente en formato JSON."
            },
            {
                "role": "user",
                "content": f"Extrae los datos del siguiente texto: '{texto}'. Si un dato no está, usa null.",
            }
        ],
        model="llama-3.1-8b-instant", # Modelo rápido y potente
    )
    resumen = chat_completion.choices[0].message.content
    return resumen

# Ejemplo de uso
email_desordenado = """
Hola, te escribo para confirmar la reunión. Mi nombre es Ana Gómez, soy la gerenta de proyectos 
en Innovatech. Mi correo es ana.gomez@innovatech.com. Nos vemos el lunes.
"""

datos_extraidos = extraer_datos_contacto(email_desordenado)
print("\n✅ Datos extraídos en JSON:")
print(datos_extraidos)