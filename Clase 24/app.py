import gradio as gr
import os
import shutil
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- Importaciones de LangChain (basadas en tus scripts) ---
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- Nuevas Importaciones para el Chatbot ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. Configuración Global y Carga de Modelos ---
# (Cargamos los modelos caros UNA SOLA VEZ al inicio)

print("Cargando modelos globales...")

# Variables (igual que en tus scripts)
PERSIST_DIRECTORY = "db_chroma"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Inicializar el modelo de Embeddings (Open-Source)
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'}
)

# Inicializar el LLM (Google Gemini)
# ¡Asegúrate de tener la variable de entorno GOOGLE_API_KEY!
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
except ImportError:
    print("Error: 'google-generativeai' no está instalado. Ejecuta: pip install google-generativeai")
    exit()
except Exception as e:
    print(f"Error al cargar el LLM. ¿Estableciste la GOOGLE_API_KEY? Error: {e}")
    # Si usas OpenAI, descomenta la siguiente línea y comenta la de Gemini:
    # from langchain_openai import ChatOpenAI
    # llm = ChatOpenAI(model="gpt-3.5-turbo")
    exit()


# Inicializar el cliente de la base de datos vectorial
# Esto se conecta al directorio persistente si existe, 
# o se prepara para crearlo.
vectordb = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings
)

# Plantilla de Prompt para RAG
RAG_PROMPT_TEMPLATE = """
Eres un asistente de IA experto. Tu tarea es responder la pregunta del usuario basándote únicamente en el siguiente contexto.
Si la información no está en el contexto, di amablemente que no tienes esa información.

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""
rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

# --- 2. Lógica de la Aplicación (Funciones) ---

def add_to_knowledge_base(file_list):
    """
    Función para la pestaña "Cargar Archivos".
    Procesa los archivos y los añade a ChromaDB.
    """
    if not file_list:
        stats = get_knowledge_base_stats()
        return "Por favor, selecciona al menos un archivo.", stats

    print(f"Procesando {len(file_list)} archivo(s)...")
    
    # 1. Cargar documentos (adaptado de ingesta.py)
    documents = []
    for file_obj in file_list:
        file_path = file_obj.name
        print(f"Cargando {file_path}")
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            print(f"Archivo no soportado: {file_path}")
            continue
        documents.extend(loader.load())

    if not documents:
        stats = get_knowledge_base_stats()
        return "No se pudieron cargar documentos válidos (solo .txt y .pdf).", stats

    # 2. Dividir documentos (adaptado de ingesta.py)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
    splits = text_splitter.split_documents(documents)
    
    if not splits:
        stats = get_knowledge_base_stats()
        return "Los documentos están vacíos o no se pudieron dividir.", stats

    # 3. Añadir a la base de datos (Usamos .add_documents para añadir)
    print(f"Añadiendo {len(splits)} chunks a la base de datos...")
    vectordb.add_documents(splits)
    print("¡Archivos procesados y añadidos a la base de datos!")
    
    # Obtener estadísticas actualizadas
    stats = get_knowledge_base_stats()
    
    return f"¡Éxito! Se añadieron {len(splits)} fragmentos de {len(file_list)} archivo(s).", stats

def respond_chat(message, chat_history):
    """
    Función para el Chatbot.
    Construye y ejecuta la cadena RAG completa.
    """
    print(f"Recibida pregunta: {message}")

    # 1. Crear el Retriever (adaptado de consulta.py)
    # Esto busca en la 'vectordb' que ya está cargada
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    # 2. Construir la cadena RAG con LCEL
    # Esta es la "tubería" (pipe) que define el flujo de RAG
    rag_chain = (
        # El diccionario de entrada pasa el contexto y la pregunta
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt  # 1. El contexto y la pregunta van al prompt
        | llm         # 2. El prompt formateado va al LLM
        | StrOutputParser() # 3. Extraemos la respuesta de texto del LLM
    )

    # 3. Invocar la cadena
    print("Invocando cadena RAG...")
    response = rag_chain.invoke(message)
    
    chat_history.append((message, response))
    print(f"Respuesta generada: {response}")
    
    return "", chat_history

def clear_knowledge_base():
    """
    Función para limpiar la base de datos eliminando todos los documentos.
    """
    global vectordb
    try:
        print("Limpiando base de datos...")
        
        # Obtener todos los IDs de la colección
        collection = vectordb._collection
        
        # Verificar si hay documentos
        count = collection.count()
        if count == 0:
            print("La base de datos ya estaba vacía.")
            stats = get_knowledge_base_stats()
            return "La base de datos ya estaba vacía.", stats
        
        # Obtener todos los IDs y eliminarlos
        all_ids = collection.get()['ids']
        if all_ids:
            collection.delete(ids=all_ids)
            print(f"Se eliminaron {count} fragmentos de la base de datos.")
        
        stats = get_knowledge_base_stats()
        return f"✅ Base de datos limpiada exitosamente. Se eliminaron {count} fragmentos.", stats
        
    except Exception as e:
        print(f"Error al limpiar la base de datos: {e}")
        stats = get_knowledge_base_stats()
        return f"❌ Error al limpiar la base de datos: {e}\n\nSi el problema persiste, reinicia la aplicación.", stats

def get_knowledge_base_stats():
    """
    Obtiene estadísticas de la base de conocimiento.
    Retorna un string formateado con las estadísticas.
    """
    try:
        # Obtener la colección de ChromaDB
        collection = vectordb._collection
        count = collection.count()
        
        if count == 0:
            return " **Estado:** Base de conocimiento vacía (0 fragmentos)"
        else:
            return f" **Estado:** Base de conocimiento activa\n\n **Total de fragmentos:** {count:,}\n\n Puedes hacer preguntas sobre el contenido cargado."
    except Exception as e:
        return f" Error al obtener estadísticas: {e}"

# --- 3. Interfaz de Gradio ---

print("Iniciando interfaz de Gradio...")

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Chatbot RAG con LangChain y Gradio\nChatea con tus documentos. Sube archivos en la pestaña 'Base de Conocimiento'.")

    with gr.Tab("💬 Chatbot"):
        chatbot = gr.Chatbot(label="Chat", height=400)
        msg_input = gr.Textbox(label="Escribe tu pregunta aquí...", lines=1, max_lines=3)
        
        with gr.Row():
            submit_btn = gr.Button("📤 Enviar", variant="primary")
            clear_button = gr.ClearButton([msg_input, chatbot], value="🗑️ Limpiar Chat")
        
        # Conectar la función de chat
        msg_input.submit(respond_chat, [msg_input, chatbot], [msg_input, chatbot])
        submit_btn.click(respond_chat, [msg_input, chatbot], [msg_input, chatbot])

    with gr.Tab("📚 Base de Conocimiento"):
        
        # Estadísticas compactas
        with gr.Row():
            stats_display = gr.Markdown(value=get_knowledge_base_stats())
            refresh_button = gr.Button("🔄 Actualizar", size="sm", scale=0)
        
        # Cargar archivos
        with gr.Group():
            gr.Markdown("### 📤 Cargar Documentos")
            file_upload = gr.File(
                label="Archivos (.txt, .pdf)",
                file_count="multiple",
                file_types=[".txt", ".pdf"]
            )
            upload_button = gr.Button("📥 Analizar y Cargar", variant="primary")
            status_output = gr.Textbox(label="Resultado", interactive=False, lines=3)
        
        # Limpiar base de datos
        with gr.Group():
            gr.Markdown("### ⚠️ Limpiar Base de Datos")
            clear_db_button = gr.Button("🗑️ Eliminar Todos los Documentos", variant="stop")
            clear_status_output = gr.Textbox(label="Resultado", interactive=False, lines=2)
        
        # Conectar eventos
        upload_button.click(
            add_to_knowledge_base, 
            inputs=[file_upload], 
            outputs=[status_output, stats_display]
        )
        
        refresh_button.click(
            get_knowledge_base_stats,
            inputs=[],
            outputs=[stats_display]
        )
        
        # Conectar la función de limpiado
        clear_db_button.click(
            clear_knowledge_base, 
            inputs=[], 
            outputs=[clear_status_output, stats_display]
        )

# --- 4. Lanzar la Aplicación ---
if __name__ == "__main__":
    demo.launch(share=True) # share=True para crear un enlace público temporal