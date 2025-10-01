import os
from dotenv import load_dotenv
from groq import Groq

# Cargar las variables de entorno (la API key)
load_dotenv()

# Configurar el cliente de Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def resumir_texto(texto_largo):
    print("🤖 Enviando texto a la IA para resumir...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente experto en resumir textos en 3 puntos clave."
            },
            {
                "role": "user",
                "content": f"Por favor, resume el siguiente texto: '{texto_largo}'",
            }
        ],
        model="llama-3.1-8b-instant", # Modelo rápido y potente
    )
    resumen = chat_completion.choices[0].message.content
    return resumen

# Ejemplo de uso
articulo = """La inteligencia artificial (IA) está transformando el mundo a una velocidad vertiginosa, marcando un antes y
un después en la forma en que trabajamos, nos comunicamos y vivimos. Lo que hasta hace pocos años parecía ciencia ficción 
hoy es una realidad palpable: desde la automatización de tareas repetitivas en fábricas y oficinas hasta la creación de arte,
música y literatura mediante algoritmos avanzados, las aplicaciones de la IA parecen no tener límites.

Empresas de todos los sectores, desde la salud hasta la banca, pasando por la educación, la industria energética y 
el entretenimiento, están invirtiendo miles de millones de dólares en desarrollar sus propias capacidades de IA. El objetivo 
no es solo optimizar procesos internos o reducir costos, sino también mejorar la precisión en la toma de decisiones 
estratégicas, anticipar tendencias del mercado y, sobre todo, crear productos y servicios innovadores que antes resultaban 
impensables. La IA se ha convertido en un factor diferencial clave para la competitividad global.

Sin embargo, este rápido avance también trae consigo una serie de desafíos éticos, sociales y legales que deben ser abordados
con seriedad. Surgen preguntas fundamentales: ¿cómo garantizar que los algoritmos sean justos y no reproduzcan sesgos? 
¿Qué impacto tendrá la automatización en los empleos tradicionales? ¿Cómo se deben regular el uso de los datos y la privacidad 
de los ciudadanos? ¿Qué responsabilidades deben asumir las empresas y los gobiernos ante posibles consecuencias negativas 
de estas tecnologías?

La respuesta a estas cuestiones exige un esfuerzo conjunto de científicos, legisladores, empresas 
y la sociedad en general. Solo a través de un marco ético sólido y políticas claras será posible aprovechar el enorme 
potencial de la inteligencia artificial sin dejar de lado la protección de los derechos humanos y la equidad social. 
En definitiva, la IA representa una herramienta poderosa que, bien utilizada, puede impulsar el progreso y el bienestar global,
pero cuyo desarrollo requiere responsabilidad, transparencia y un debate inclusivo.
"""

resumen_generado = resumir_texto(articulo)
print("\n✅ Resumen generado:")
print(resumen_generado)