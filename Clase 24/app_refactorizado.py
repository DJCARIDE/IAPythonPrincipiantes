"""
app_refactorizado.py - Aplicación Principal del Chatbot RAG
============================================================

Este es el archivo principal que integra todos los módulos y
crea la interfaz de usuario con Gradio.

ARQUITECTURA MODULAR:
- config.py: Configuración centralizada
- database_manager.py: Gestión de ChromaDB
- document_processor.py: Procesamiento de documentos
- rag_chain.py: Cadena RAG completa
- app_refactorizado.py: Integración e interfaz (ESTE ARCHIVO)

¿POR QUÉ MODULARIZAR?
- Código más organizado y fácil de entender
- Cada módulo tiene una responsabilidad clara
- Facilita el mantenimiento y pruebas
- Permite reutilizar componentes en otros proyectos

Autor: Clase 24 - IA Python para Principiantes
Fecha: 2025
"""

import gradio as gr
from database_manager import DatabaseManager
from document_processor import DocumentProcessor
from rag_chain import RAGChain
from config import (
    APP_TITLE,
    APP_DESCRIPTION,
    CHAT_HEIGHT,
    ALLOWED_FILE_TYPES,
    UI_THEME,
    MSG_STARTING_UI
)

# ==============================================================================
# 1. INICIALIZACIÓN DE COMPONENTES GLOBALES
# ==============================================================================

print("=" * 70)
print("🚀 INICIANDO CHATBOT RAG - Versión Modular")
print("=" * 70)

# Inicializar el gestor de base de datos
# Este componente maneja ChromaDB y los embeddings
print("\n📦 Inicializando componentes...")
db_manager = DatabaseManager()

# Inicializar el procesador de documentos
# Este componente carga y procesa archivos
doc_processor = DocumentProcessor()

# Inicializar la cadena RAG
# Este componente conecta retriever + LLM
rag_chain = RAGChain(db_manager)

print("✅ Todos los componentes inicializados correctamente\n")

# ==============================================================================
# 2. FUNCIONES DE LA INTERFAZ DE USUARIO
# ==============================================================================

def handle_file_upload(file_list):
    """
    Maneja la carga de archivos desde la interfaz de Gradio.
    
    Esta función:
    1. Extrae las rutas de los archivos subidos
    2. Procesa los archivos (carga y divide en chunks)
    3. Añade los fragmentos a la base de datos
    4. Actualiza las estadísticas
    
    Args:
        file_list: Lista de archivos subidos por Gradio
                   Cada elemento tiene un atributo .name con la ruta
                   
    Returns:
        tuple: (mensaje_estado, estadísticas_actualizadas)
        
    Nota para estudiantes:
        Esta función es el "pegamento" entre la interfaz de Gradio
        y nuestra lógica de negocio en los módulos.
    """
    # Validar que se hayan subido archivos
    if not file_list:
        stats = db_manager.get_stats()
        return "⚠️ Por favor, selecciona al menos un archivo.", stats['message']
    
    try:
        # Extraer las rutas de los archivos
        file_paths = [file_obj.name for file_obj in file_list]
        
        print(f"\n{'='*70}")
        print(f"📤 CARGA DE ARCHIVOS INICIADA")
        print(f"{'='*70}")
        
        # Paso 1: Procesar los archivos (cargar y dividir)
        result = doc_processor.process_files(file_paths)
        
        # Si el procesamiento falló, retornar mensaje de error
        if not result['success']:
            stats = db_manager.get_stats()
            return result['message'], stats['message']
        
        # Paso 2: Añadir los fragmentos a la base de datos
        splits = result['splits']
        db_manager.add_documents(splits)
        
        # Paso 3: Actualizar estadísticas
        stats = db_manager.get_stats()
        
        # Crear mensaje de éxito detallado
        success_message = (
            f"✅ ¡Éxito!\n\n"
            f"📄 Archivos procesados: {len(file_paths)}\n"
            f"📊 Fragmentos creados: {result['split_count']}\n"
            f"💾 Total en base de datos: {stats['count']:,}"
        )
        
        if result['failed_files']:
            success_message += f"\n\n⚠️ Archivos con error: {len(result['failed_files'])}"
        
        print(f"\n{'='*70}")
        print(f"✅ CARGA COMPLETADA")
        print(f"{'='*70}\n")
        
        return success_message, stats['message']
        
    except Exception as e:
        print(f"\n❌ Error en handle_file_upload: {e}\n")
        stats = db_manager.get_stats()
        return f"❌ Error al procesar archivos: {str(e)}", stats['message']


def handle_chat_message(message, chat_history):
    """
    Maneja los mensajes del chat.
    
    Esta función:
    1. Recibe el mensaje del usuario
    2. Usa la cadena RAG para generar una respuesta
    3. Actualiza el historial del chat
    
    Args:
        message (str): Mensaje/pregunta del usuario
        chat_history (list): Historial de mensajes [(user, bot), ...]
        
    Returns:
        tuple: ("", chat_history_actualizado)
               Retornamos "" para limpiar el input
               
    Nota para estudiantes:
        Gradio maneja automáticamente el historial del chat.
        Solo necesitamos agregarlo a la lista.
    """
    # Validar que el mensaje no esté vacío
    if not message or message.strip() == "":
        return "", chat_history
    
    try:
        print(f"\n{'='*70}")
        print(f"💬 NUEVA PREGUNTA")
        print(f"{'='*70}")
        print(f"Usuario: {message[:100]}...")
        
        # Generar respuesta usando la cadena RAG
        response = rag_chain.query(message)
        
        # Agregar al historial del chat
        # Formato de Gradio: (mensaje_usuario, respuesta_bot)
        chat_history.append((message, response))
        
        print(f"Bot: {response[:100]}...")
        print(f"{'='*70}\n")
        
        # Retornar input vacío y historial actualizado
        return "", chat_history
        
    except Exception as e:
        print(f"\n❌ Error en handle_chat_message: {e}\n")
        # En caso de error, mostrar mensaje al usuario
        error_response = (
            f"😔 Lo siento, ocurrió un error al procesar tu pregunta.\n\n"
            f"Error: {str(e)}\n\n"
            f"Por favor, intenta de nuevo o contacta al administrador."
        )
        chat_history.append((message, error_response))
        return "", chat_history


def handle_clear_database():
    """
    Maneja la limpieza de la base de datos.
    
    Esta función:
    1. Elimina todos los documentos de ChromaDB
    2. Actualiza las estadísticas
    
    Returns:
        tuple: (mensaje_resultado, estadísticas_actualizadas)
        
    Advertencia:
        Esta operación no se puede deshacer.
        Todos los documentos serán eliminados permanentemente.
    """
    try:
        print(f"\n{'='*70}")
        print(f"🗑️ LIMPIEZA DE BASE DE DATOS")
        print(f"{'='*70}")
        
        # Limpiar la base de datos
        result = db_manager.clear_all_documents()
        
        # Actualizar estadísticas
        stats = db_manager.get_stats()
        
        print(f"{result['message']}")
        print(f"{'='*70}\n")
        
        return result['message'], stats['message']
        
    except Exception as e:
        print(f"\n❌ Error en handle_clear_database: {e}\n")
        stats = db_manager.get_stats()
        return f"❌ Error al limpiar la base de datos: {str(e)}", stats['message']


def handle_refresh_stats():
    """
    Actualiza las estadísticas de la base de datos.
    
    Returns:
        str: Mensaje con las estadísticas actualizadas
    """
    stats = db_manager.get_stats()
    return stats['message']


# ==============================================================================
# 3. CONSTRUCCIÓN DE LA INTERFAZ DE GRADIO
# ==============================================================================

print(MSG_STARTING_UI)

# Crear la interfaz usando Blocks (más flexible que Interface)
with gr.Blocks(theme=gr.themes.Soft(), title=APP_TITLE) as demo:
    
    # === ENCABEZADO COMPACTO ===
    gr.Markdown(f"# {APP_TITLE}\n{APP_DESCRIPTION}")
    
    # === PESTAÑA 1: CHATBOT ===
    with gr.Tab("💬 Chatbot"):
        # Instrucciones colapsables para ahorrar espacio
        with gr.Accordion("ℹ️ ¿Cómo usar el chatbot?", open=False):
            gr.Markdown("""
            1. Primero, carga tus documentos en la pestaña "📚 Base de Conocimiento"
            2. Luego, haz preguntas sobre el contenido de esos documentos
            3. El chatbot responderá basándose SOLO en la información de tus archivos
            """)
        
        # Componente de chat
        chatbot = gr.Chatbot(
            label="Conversación",
            height=CHAT_HEIGHT,
            show_label=True
        )
        
        # Input para mensajes
        msg_input = gr.Textbox(
            label="Escribe tu pregunta aquí...",
            placeholder="Ejemplo: ¿Cuál es el tema principal del documento?",
            lines=1,
            max_lines=3
        )
        
        # Botones de acción
        with gr.Row():
            submit_btn = gr.Button("📤 Enviar", variant="primary")
            clear_chat_btn = gr.ClearButton(
                [msg_input, chatbot],
                value="🗑️ Limpiar Chat"
            )
        
        # Conectar eventos
        # Enviar mensaje al presionar Enter o botón
        msg_input.submit(
            handle_chat_message,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot]
        )
        submit_btn.click(
            handle_chat_message,
            inputs=[msg_input, chatbot],
            outputs=[msg_input, chatbot]
        )
    
    # === PESTAÑA 2: GESTIÓN DE DOCUMENTOS ===
    with gr.Tab("📚 Base de Conocimiento"):
        
        # === SECCIÓN: ESTADÍSTICAS ===
        with gr.Row():
            stats_display = gr.Markdown(
                value=db_manager.get_stats()['message']
            )
            refresh_btn = gr.Button("🔄 Actualizar", size="sm", scale=0)
        
        # === SECCIÓN: CARGAR ARCHIVOS ===
        with gr.Group():
            gr.Markdown("### 📤 Cargar Documentos")
            file_upload = gr.File(
                label="Archivos (.txt, .pdf)",
                file_count="multiple",
                file_types=ALLOWED_FILE_TYPES,
                interactive=True
            )
            upload_btn = gr.Button("📥 Analizar y Cargar", variant="primary")
            upload_status = gr.Textbox(
                label="Resultado",
                interactive=False,
                lines=3
            )
        
        # === SECCIÓN: ZONA DE PELIGRO ===
        with gr.Group():
            gr.Markdown("### ⚠️ Limpiar Base de Datos")
            clear_db_btn = gr.Button(
                "🗑️ Eliminar Todos los Documentos",
                variant="stop"
            )
            clear_status = gr.Textbox(
                label="Resultado",
                interactive=False,
                lines=2
            )
        
        # Conectar eventos de esta pestaña
        upload_btn.click(
            handle_file_upload,
            inputs=[file_upload],
            outputs=[upload_status, stats_display]
        )
        
        refresh_btn.click(
            handle_refresh_stats,
            inputs=[],
            outputs=[stats_display]
        )
        
        clear_db_btn.click(
            handle_clear_database,
            inputs=[],
            outputs=[clear_status, stats_display]
        )
    
    # === PESTAÑA 3: INFORMACIÓN ===
    with gr.Tab("ℹ️ Información"):
        gr.Markdown("# 📚 Chatbot RAG - Información del Proyecto")
        
        # Acordeones colapsables para información compacta
        with gr.Accordion("¿Qué es RAG?", open=True):
            gr.Markdown("""
            **RAG** = *Retrieval Augmented Generation* (Generación Aumentada por Recuperación)
            
            Combina:
            - **Recuperación**: Busca información relevante en documentos
            - **Generación**: Usa un LLM para respuestas basadas en esa información
            """)
        
        with gr.Accordion("¿Cómo funciona?", open=False):
            gr.Markdown("""
            1. 📄 Cargas documentos (PDF/TXT)
            2. ✂️ Se dividen en fragmentos (chunks)
            3. 🔢 Se convierten en vectores (embeddings)
            4. 💾 Se guardan en ChromaDB
            5. 💬 Haces una pregunta
            6. 🔍 Se buscan fragmentos relevantes
            7. 🤖 El LLM genera respuesta con ese contexto
            """)
        
        with gr.Accordion("Tecnologías", open=False):
            gr.Markdown("""
            - **LangChain**: Framework para LLMs
            - **Google Gemini**: Modelo de lenguaje
            - **ChromaDB**: Base de datos vectorial
            - **Sentence Transformers**: Embeddings
            - **Gradio**: Interfaz web
            """)
        
        with gr.Accordion("Arquitectura Modular", open=False):
            gr.Markdown("""
            - `config.py` → Configuración
            - `database_manager.py` → ChromaDB
            - `document_processor.py` → Procesamiento
            - `rag_chain.py` → Lógica RAG
            - `app_refactorizado.py` → Interfaz
            """)
        
        with gr.Accordion("Ventajas de RAG", open=False):
            gr.Markdown("""
            ✅ Respuestas basadas en TUS documentos  
            ✅ Reduce "alucinaciones" del LLM  
            ✅ Conocimiento actualizable sin reentrenar  
            ✅ Transparente y verificable
            """)
        
        with gr.Accordion("Recursos de Aprendizaje", open=False):
            gr.Markdown("""
            - [LangChain](https://python.langchain.com/)
            - [ChromaDB](https://docs.trychroma.com/)
            - [Gradio](https://www.gradio.app/)
            """)
        
        gr.Markdown("---")
        gr.Markdown("💡 **Clase 24 - IA Python para Principiantes**")

# ==============================================================================
# 4. LANZAR LA APLICACIÓN
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎉 APLICACIÓN LISTA")
    print("="*70)
    print("\n🌐 Lanzando servidor web...")
    print("💡 Presiona Ctrl+C para detener el servidor\n")
    
    # Lanzar la interfaz de Gradio
    demo.launch(
        share=True,  # Crear enlace público temporal (opcional)
        # server_name="0.0.0.0",  # Descomentar para acceso desde otras máquinas
        # server_port=7860,       # Puerto personalizado
    )

# ==============================================================================
# NOTAS PARA ESTUDIANTES
# ==============================================================================
"""
📚 CONCEPTOS IMPORTANTES:

1. ARQUITECTURA MODULAR:
   - Separación de responsabilidades
   - Cada módulo tiene un propósito claro
   - Facilita mantenimiento y testing
   
2. INTERFAZ DE USUARIO CON GRADIO:
   - gr.Blocks: Construcción flexible de UI
   - gr.Tab: Organización en pestañas
   - Componentes reactivos: actualizan automáticamente
   
3. MANEJO DE EVENTOS:
   - .click(), .submit(): Conectan acciones con funciones
   - inputs/outputs: Definen el flujo de datos
   - return multiple values: Actualizar varios componentes
   
4. GESTIÓN DE ESTADO:
   - Variables globales para componentes persistentes
   - chat_history: Gradio lo maneja automáticamente
   - Estadísticas: Se actualizan reactivamente

💡 EJERCICIOS SUGERIDOS:
   1. Agrega una pestaña para mostrar las fuentes de cada respuesta
   2. Implementa un botón de "exportar conversación"
   3. Añade estadísticas visuales con gr.Plot
   
⚠️ PARA PRODUCCIÓN:
   - Agregar autenticación de usuarios
   - Implementar rate limiting
   - Usar una base de datos persistente real
   - Agregar logging y monitoreo
   - Validación robusta de inputs
"""
