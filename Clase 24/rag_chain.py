"""
rag_chain.py - Cadena RAG (Retrieval Augmented Generation)
===========================================================

Este módulo implementa la cadena RAG completa, que combina:
1. Búsqueda de documentos relevantes (Retrieval)
2. Generación de respuestas con LLM (Generation)

¿QUÉ ES RAG?
RAG = Retrieval Augmented Generation
- Recupera información relevante de una base de datos
- Aumenta el prompt del LLM con esa información
- Genera respuestas basadas en datos reales (no inventados)

Autor: Clase 24 - IA Python para Principiantes
Fecha: 2025
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import (
    LLM_MODEL,
    TOP_K_DOCUMENTS,
    RAG_PROMPT_TEMPLATE,
    ERROR_NO_API_KEY,
    ERROR_MODEL_LOAD
)

# ==============================================================================
# CLASE: RAGChain
# ==============================================================================

class RAGChain:
    """
    Clase que implementa la cadena RAG completa.
    
    La cadena RAG es el "cerebro" de nuestro chatbot. Conecta:
    - El retriever (busca documentos)
    - El prompt template (formatea la pregunta)
    - El LLM (genera la respuesta)
    
    Esta arquitectura permite que el LLM responda basándose en
    documentos específicos en lugar de solo su conocimiento interno.
    """
    
    def __init__(self, database_manager):
        """
        Constructor de la cadena RAG.
        
        Args:
            database_manager (DatabaseManager): Instancia del gestor de base de datos
                que contiene los documentos y el retriever
                
        Raises:
            Exception: Si no se puede inicializar el LLM
        """
        self.database_manager = database_manager
        
        # Inicializar el modelo de lenguaje (LLM)
        self.llm = self._initialize_llm()
        
        # Crear el prompt template
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        
        print("✅ Cadena RAG inicializada correctamente")
    
    def _initialize_llm(self):
        """
        Inicializa el modelo de lenguaje (LLM) de Google Gemini.
        
        El LLM es el modelo que genera las respuestas finales.
        Usamos Google Gemini por ser:
        - Rápido (Flash variant)
        - Económico
        - Multimodal (puede manejar texto e imágenes)
        
        Returns:
            ChatGoogleGenerativeAI: Instancia del LLM inicializada
            
        Raises:
            ImportError: Si no está instalado google-generativeai
            Exception: Si falla la inicialización (ej: API key inválida)
            
        Nota para estudiantes:
            La API key debe estar en el archivo .env como GOOGLE_API_KEY
        """
        try:
            print(f"🤖 Inicializando LLM: {LLM_MODEL}")
            
            # Crear instancia del LLM de Google Gemini
            llm = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                # Puedes agregar más parámetros aquí:
                # temperature=0.7,  # Creatividad (0=determinista, 1=creativo)
                # max_tokens=1000,  # Longitud máxima de respuesta
            )
            
            print(f"✅ LLM inicializado: {LLM_MODEL}")
            return llm
            
        except ImportError:
            error_msg = (
                "❌ Error: 'langchain-google-genai' no está instalado.\n"
                "Ejecuta: pip install langchain-google-genai"
            )
            print(error_msg)
            raise
            
        except Exception as e:
            print(f"{ERROR_MODEL_LOAD}: {e}")
            print("\n💡 Posibles soluciones:")
            print("   1. Verifica que GOOGLE_API_KEY esté en el archivo .env")
            print("   2. Verifica que la API key sea válida")
            print("   3. Verifica tu conexión a internet")
            raise
    
    def create_chain(self, k=TOP_K_DOCUMENTS):
        """
        Crea la cadena RAG completa usando LCEL (LangChain Expression Language).
        
        LCEL es una forma declarativa de construir cadenas en LangChain.
        El operador | (pipe) conecta componentes secuencialmente.
        
        Flujo de la cadena:
        1. question → retriever → context (documentos relevantes)
        2. {context, question} → prompt (prompt formateado)
        3. prompt → llm (respuesta generada)
        4. llm → output_parser (texto limpio)
        
        Args:
            k (int): Número de documentos a recuperar
            
        Returns:
            Runnable: Cadena RAG ejecutable
            
        Ejemplo:
            >>> rag = RAGChain(db_manager)
            >>> chain = rag.create_chain(k=5)
            >>> response = chain.invoke("¿Qué es Python?")
            
        Nota para estudiantes:
            Esta es la parte más importante del sistema RAG.
            Estudia cuidadosamente cómo se conectan los componentes.
        """
        # Obtener el retriever de la base de datos
        retriever = self.database_manager.get_retriever(k=k)
        
        # Construir la cadena usando LCEL (LangChain Expression Language)
        rag_chain = (
            # Paso 1: Preparar inputs
            # - "context": retriever busca docs similares a la pregunta
            # - "question": pasa la pregunta original sin modificar
            {
                "context": retriever,      # Retriever busca y retorna documentos
                "question": RunnablePassthrough()  # Pregunta pasa sin cambios
            }
            # Paso 2: Formatear el prompt
            # El prompt recibe {context} y {question} y crea el mensaje para el LLM
            | self.prompt
            # Paso 3: Generar respuesta
            # El LLM recibe el prompt formateado y genera la respuesta
            | self.llm
            # Paso 4: Parsear la salida
            # Convierte la respuesta del LLM en un string simple
            | StrOutputParser()
        )
        
        return rag_chain
    
    def query(self, question, k=TOP_K_DOCUMENTS):
        """
        Realiza una consulta completa al sistema RAG.
        
        Este es el método principal que usarás para hacer preguntas.
        Internamente:
        1. Crea la cadena RAG
        2. Busca documentos relevantes
        3. Genera una respuesta basada en esos documentos
        
        Args:
            question (str): Pregunta del usuario
            k (int): Número de documentos a recuperar (default: TOP_K_DOCUMENTS)
            
        Returns:
            str: Respuesta generada por el LLM
            
        Raises:
            Exception: Si hay error durante la generación
            
        Ejemplo:
            >>> rag = RAGChain(db_manager)
            >>> respuesta = rag.query("¿Qué es machine learning?")
            >>> print(respuesta)
            "Machine learning es una rama de la inteligencia artificial..."
        """
        try:
            print(f"\n🔍 Procesando pregunta: {question[:100]}...")
            
            # Crear la cadena RAG
            rag_chain = self.create_chain(k=k)
            
            # Invocar la cadena con la pregunta
            # Esto ejecuta todo el flujo: retrieval → prompt → LLM → parse
            response = rag_chain.invoke(question)
            
            print(f"✅ Respuesta generada ({len(response)} caracteres)")
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error al generar respuesta: {e}"
            print(error_msg)
            # En lugar de fallar, retornar un mensaje de error al usuario
            return f"Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}"
    
    def query_with_sources(self, question, k=TOP_K_DOCUMENTS):
        """
        Realiza una consulta y retorna también los documentos fuente.
        
        Esto es útil para:
        - Transparencia: mostrar de dónde viene la información
        - Debugging: verificar qué documentos se recuperaron
        - Citación: dar crédito a las fuentes
        
        Args:
            question (str): Pregunta del usuario
            k (int): Número de documentos a recuperar
            
        Returns:
            dict: Diccionario con la respuesta y las fuentes
                {
                    'answer': str,           # Respuesta generada
                    'sources': list,         # Lista de documentos fuente
                    'source_count': int      # Número de fuentes usadas
                }
                
        Ejemplo:
            >>> rag = RAGChain(db_manager)
            >>> result = rag.query_with_sources("¿Qué es RAG?")
            >>> print(result['answer'])
            >>> for i, doc in enumerate(result['sources']):
            ...     print(f"Fuente {i+1}: {doc.page_content[:100]}...")
        """
        try:
            # Obtener el retriever
            retriever = self.database_manager.get_retriever(k=k)
            
            # Buscar documentos relevantes
            source_docs = retriever.get_relevant_documents(question)
            
            # Generar la respuesta
            response = self.query(question, k=k)
            
            return {
                'answer': response,
                'sources': source_docs,
                'source_count': len(source_docs)
            }
            
        except Exception as e:
            print(f"❌ Error en query_with_sources: {e}")
            return {
                'answer': f"Error al procesar la pregunta: {str(e)}",
                'sources': [],
                'source_count': 0
            }

# ==============================================================================
# NOTAS PARA ESTUDIANTES
# ==============================================================================
"""
📚 CONCEPTOS IMPORTANTES:

1. RAG (Retrieval Augmented Generation):
   - Combina búsqueda (retrieval) con generación (LLM)
   - Soluciona el problema de "alucinaciones" del LLM
   - El LLM solo responde basado en documentos reales
   
2. LCEL (LangChain Expression Language):
   - Forma moderna de construir cadenas en LangChain
   - Operador | (pipe) conecta componentes
   - Más legible y componible que código imperativo
   
3. COMPONENTES DE LA CADENA:
   a) Retriever: Busca documentos relevantes
   b) Prompt Template: Formatea el contexto y la pregunta
   c) LLM: Genera la respuesta
   d) Output Parser: Limpia y formatea la salida
   
4. FLUJO DE DATOS:
   pregunta → [retriever] → documentos → [prompt] → mensaje → [LLM] → respuesta
   
5. TEMPERATURA DEL LLM:
   - 0.0: Determinista, siempre la misma respuesta
   - 0.7: Balanceado (recomendado)
   - 1.0+: Muy creativo, puede divagar

💡 EXPERIMENTOS SUGERIDOS:
   1. Cambia k de 5 a 3 y observa cómo afecta las respuestas
   2. Modifica el prompt template para cambiar el tono de las respuestas
   3. Implementa query_with_sources() en la interfaz para mostrar fuentes
   
⚠️ PREGUNTAS PARA REFLEXIONAR:
   - ¿Qué pasa si el retriever no encuentra documentos relevantes?
   - ¿Cómo afecta el número k a la calidad de las respuestas?
   - ¿Por qué es importante el prompt template en RAG?
   
🎯 EJERCICIO AVANZADO:
   Modifica create_chain() para agregar un paso de "re-ranking"
   que ordene los documentos recuperados por relevancia antes
   de enviarlos al LLM.
"""
