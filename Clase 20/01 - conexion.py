import openai
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# La librería openai buscará esta variable de entorno por defecto
openai.api_key = os.getenv("OPENAI_API_KEY")

print("¡Librería configurada!")

# Prueba de fuego: Verificar la conexión listando los modelos
try:
    models = openai.models.list()
    print("¡Conexión exitosa con la API de OpenAI!")
except Exception as e:
    print(f"Error de autenticación: {e}")