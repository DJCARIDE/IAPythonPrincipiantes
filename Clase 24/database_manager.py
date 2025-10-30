"""
database_manager.py - Gestor de la Base de Datos Vectorial
==========================================================

Este módulo maneja todas las operaciones relacionadas con ChromaDB,
nuestra base de datos vectorial que almacena los embeddings de los documentos.

¿QUÉ ES UNA BASE DE DATOS VECTORIAL?
- Almacena vectores numéricos (embeddings) de texto
- Permite buscar documentos similares usando matemáticas vectoriales
- Es fundamental para sistemas RAG (Retrieval Augmented Generation)

Autor: Clase 24 - IA Python para Principiantes
Fecha: 2025
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import (
    PERSIST_DIRECTORY,
    EMBEDDING_MODEL,
    DEVICE,
    MSG_LOADING_MODELS,
    MSG_MODELS_LOADED
)

# ==============================================================================
# CLASE: DatabaseManager
# ==============================================================================

class DatabaseManager:
    """
    Clase que maneja todas las operaciones de la base de datos vectorial.
    
    Esta clase encapsula (agrupa) todas las funcionalidades relacionadas
    con ChromaDB, haciendo el código más organizado y fácil de mantener.
    
    Atributos:
        embeddings: Modelo que convierte texto en vectores numéricos
        vectordb: Cliente de ChromaDB para almacenar y buscar vectores
    """
    
    def __init__(self):
        """
        Constructor de la clase. Se ejecuta automáticamente al crear una instancia.
        
        Inicializa:
        1. El modelo de embeddings (convierte texto en números)
        2. La conexión con ChromaDB
        """
        print(MSG_LOADING_MODELS)
        
        # Inicializar el modelo de embeddings
        # Este modelo convierte texto en vectores de números
        self.embeddings = self._initialize_embeddings()
        
        # Inicializar la base de datos vectorial ChromaDB
        self.vectordb = self._initialize_database()
        
        print(MSG_MODELS_LOADED)
    
    def _initialize_embeddings(self):
        """
        Inicializa el modelo de embeddings de Hugging Face.
        
        Los embeddings son representaciones numéricas del texto que capturan
        su significado semántico. Textos similares tienen embeddings similares.
        
        Returns:
            HuggingFaceEmbeddings: Modelo de embeddings listo para usar
            
        Nota para estudiantes:
            El prefijo '_' indica que es un método "privado" (para uso interno)
        """
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,  # Modelo de Hugging Face a usar
            model_kwargs={'device': DEVICE}  # Usar CPU o GPU
        )
        return embeddings
    
    def _initialize_database(self):
        """
        Inicializa la conexión con ChromaDB.
        
        ChromaDB es una base de datos vectorial que:
        - Almacena embeddings de documentos
        - Permite buscar documentos similares rápidamente
        - Persiste los datos en disco para no perderlos
        
        Returns:
            Chroma: Cliente de ChromaDB inicializado
        """
        vectordb = Chroma(
            persist_directory=PERSIST_DIRECTORY,  # Carpeta donde se guardan los datos
            embedding_function=self.embeddings     # Función para crear embeddings
        )
        return vectordb
    
    def add_documents(self, documents):
        """
        Añade documentos a la base de datos vectorial.
        
        Proceso:
        1. Los documentos se convierten en embeddings
        2. Los embeddings se almacenan en ChromaDB
        3. Se pueden buscar más tarde usando similaridad vectorial
        
        Args:
            documents (list): Lista de documentos procesados por LangChain
            
        Returns:
            int: Número de documentos añadidos
            
        Ejemplo:
            >>> db_manager = DatabaseManager()
            >>> db_manager.add_documents([doc1, doc2, doc3])
            3
        """
        try:
            # Añadir los documentos a ChromaDB
            # ChromaDB automáticamente crea los embeddings usando self.embeddings
            self.vectordb.add_documents(documents)
            
            # Retornar el número de documentos añadidos
            return len(documents)
            
        except Exception as e:
            print(f"❌ Error al añadir documentos: {e}")
            raise
    
    def get_retriever(self, k=5):
        """
        Crea un 'retriever' para buscar documentos relevantes.
        
        Un retriever es un objeto que busca los documentos más similares
        a una pregunta dada, usando búsqueda vectorial.
        
        Args:
            k (int): Número de documentos a recuperar (default: 5)
            
        Returns:
            VectorStoreRetriever: Objeto que busca documentos similares
            
        Nota para estudiantes:
            Este retriever se usa en la cadena RAG para encontrar contexto
            relevante antes de generar una respuesta.
        """
        retriever = self.vectordb.as_retriever(
            search_kwargs={"k": k}  # Recuperar los k documentos más similares
        )
        return retriever
    
    def get_stats(self):
        """
        Obtiene estadísticas de la base de datos.
        
        Esto es útil para:
        - Mostrar al usuario cuántos documentos hay cargados
        - Depurar problemas
        - Monitorear el uso de la base de datos
        
        Returns:
            dict: Diccionario con estadísticas de la base de datos
                {
                    'count': int,      # Número total de fragmentos
                    'status': str,     # Estado de la base de datos
                    'message': str     # Mensaje formateado para mostrar
                }
        """
        try:
            # Acceder a la colección interna de ChromaDB
            collection = self.vectordb._collection
            
            # Contar cuántos documentos hay almacenados
            count = collection.count()
            
            # Crear el mensaje de estado
            if count == 0:
                status = "empty"
                message = "📊 **Estado:** Base de conocimiento vacía (0 fragmentos)"
            else:
                status = "active"
                message = (
                    f"📊 **Estado:** Base de conocimiento activa\n\n"
                    f"✅ **Total de fragmentos:** {count:,}\n\n"
                    f"💡 Puedes hacer preguntas sobre el contenido cargado."
                )
            
            return {
                'count': count,
                'status': status,
                'message': message
            }
            
        except Exception as e:
            # Si hay un error, retornar información del error
            return {
                'count': 0,
                'status': 'error',
                'message': f"⚠️ Error al obtener estadísticas: {e}"
            }
    
    def clear_all_documents(self):
        """
        Elimina todos los documentos de la base de datos.
        
        PRECAUCIÓN: Esta operación no se puede deshacer.
        Todos los documentos se eliminarán permanentemente.
        
        Returns:
            dict: Resultado de la operación
                {
                    'success': bool,      # True si se limpió correctamente
                    'deleted_count': int, # Número de documentos eliminados
                    'message': str        # Mensaje descriptivo
                }
        """
        try:
            # Acceder a la colección de ChromaDB
            collection = self.vectordb._collection
            
            # Obtener el número de documentos antes de borrar
            count = collection.count()
            
            # Si ya está vacía, no hacer nada
            if count == 0:
                return {
                    'success': True,
                    'deleted_count': 0,
                    'message': "La base de datos ya estaba vacía."
                }
            
            # Obtener todos los IDs de los documentos
            all_ids = collection.get()['ids']
            
            # Eliminar todos los documentos por sus IDs
            if all_ids:
                collection.delete(ids=all_ids)
            
            # Retornar resultado exitoso
            return {
                'success': True,
                'deleted_count': count,
                'message': f"✅ Base de datos limpiada exitosamente. Se eliminaron {count} fragmentos."
            }
            
        except Exception as e:
            # Si hay un error, retornar información del error
            return {
                'success': False,
                'deleted_count': 0,
                'message': f"❌ Error al limpiar la base de datos: {e}"
            }

# ==============================================================================
# NOTAS PARA ESTUDIANTES
# ==============================================================================
"""
📚 CONCEPTOS IMPORTANTES:

1. PROGRAMACIÓN ORIENTADA A OBJETOS (POO):
   - Organizamos el código en clases
   - Una clase es como un "molde" para crear objetos
   - Los objetos tienen atributos (datos) y métodos (funciones)
   
2. EMBEDDINGS:
   - Representaciones numéricas del texto
   - Capturan el significado semántico
   - Permiten calcular similaridad entre textos
   
3. BASE DE DATOS VECTORIAL:
   - Almacena vectores en lugar de tablas tradicionales
   - Optimizada para búsqueda por similaridad
   - Fundamental para RAG y búsqueda semántica
   
4. RETRIEVER:
   - Componente que busca documentos relevantes
   - Usa similaridad vectorial (distancia coseno)
   - Retorna los k documentos más similares

5. ENCAPSULACIÓN:
   - Agrupar datos y funciones relacionadas en una clase
   - Ocultar detalles de implementación (métodos privados con _)
   - Facilita el mantenimiento y reuso del código

💡 EJERCICIO PROPUESTO:
   Intenta modificar el número de documentos recuperados (k)
   y observa cómo afecta a las respuestas del chatbot.
"""
