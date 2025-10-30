"""
document_processor.py - Procesador de Documentos
================================================

Este módulo maneja la carga y procesamiento de documentos.
Convierte archivos (PDF, TXT) en fragmentos pequeños listos para
ser almacenados en la base de datos vectorial.

¿POR QUÉ DIVIDIR DOCUMENTOS EN FRAGMENTOS (CHUNKS)?
- Los LLMs tienen límite de tokens de entrada
- Fragmentos pequeños permiten búsquedas más precisas
- Cada fragmento puede recuperarse independientemente

Autor: Clase 24 - IA Python para Principiantes
Fecha: 2025
"""

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

# ==============================================================================
# CLASE: DocumentProcessor
# ==============================================================================

class DocumentProcessor:
    """
    Clase que procesa documentos para el sistema RAG.
    
    Responsabilidades:
    1. Cargar archivos (TXT, PDF)
    2. Dividir documentos en fragmentos (chunks)
    3. Validar y preparar documentos para la base de datos
    
    Esta clase implementa el patrón de diseño "Single Responsibility Principle":
    cada clase tiene una única responsabilidad bien definida.
    """
    
    def __init__(self, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        """
        Constructor del procesador de documentos.
        
        Args:
            chunk_size (int): Tamaño de cada fragmento en caracteres
            chunk_overlap (int): Superposición entre fragmentos consecutivos
            
        Nota para estudiantes:
            La superposición ayuda a mantener el contexto entre chunks.
            Por ejemplo, si una oración está dividida entre dos chunks,
            la superposición asegura que ambos tengan la oración completa.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Inicializar el divisor de texto
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    def load_file(self, file_path):
        """
        Carga un archivo y retorna su contenido como documento de LangChain.
        
        Soporta:
        - Archivos TXT (texto plano)
        - Archivos PDF (documentos)
        
        Args:
            file_path (str): Ruta al archivo a cargar
            
        Returns:
            list: Lista de documentos de LangChain cargados
            
        Raises:
            ValueError: Si el tipo de archivo no es soportado
            Exception: Si hay error al cargar el archivo
            
        Ejemplo:
            >>> processor = DocumentProcessor()
            >>> docs = processor.load_file("documento.pdf")
            >>> print(f"Cargadas {len(docs)} páginas")
        """
        try:
            # Determinar el tipo de archivo por su extensión
            if file_path.endswith(".pdf"):
                # Usar PyPDFLoader para archivos PDF
                # Este loader extrae el texto de cada página del PDF
                loader = PyPDFLoader(file_path)
                print(f"📄 Cargando PDF: {file_path}")
                
            elif file_path.endswith(".txt"):
                # Usar TextLoader para archivos de texto
                # Importante: especificar encoding para evitar errores
                loader = TextLoader(file_path, encoding='utf-8')
                print(f"📝 Cargando TXT: {file_path}")
                
            else:
                # Tipo de archivo no soportado
                raise ValueError(
                    f"Tipo de archivo no soportado: {file_path}\n"
                    f"Solo se aceptan archivos .txt y .pdf"
                )
            
            # Cargar el documento usando el loader apropiado
            documents = loader.load()
            
            print(f"✅ Archivo cargado: {len(documents)} documento(s)")
            return documents
            
        except Exception as e:
            print(f"❌ Error al cargar {file_path}: {e}")
            raise
    
    def load_multiple_files(self, file_paths):
        """
        Carga múltiples archivos de forma secuencial.
        
        Esta función procesa una lista de archivos y combina todos
        los documentos en una sola lista.
        
        Args:
            file_paths (list): Lista de rutas a archivos
            
        Returns:
            tuple: (documentos_cargados, archivos_con_error)
                - documentos_cargados (list): Lista con todos los documentos
                - archivos_con_error (list): Lista de archivos que fallaron
                
        Ejemplo:
            >>> processor = DocumentProcessor()
            >>> files = ["doc1.pdf", "doc2.txt", "doc3.pdf"]
            >>> docs, errors = processor.load_multiple_files(files)
            >>> print(f"Cargados: {len(docs)}, Errores: {len(errors)}")
        """
        all_documents = []
        failed_files = []
        
        print(f"\n📚 Procesando {len(file_paths)} archivo(s)...\n")
        
        # Procesar cada archivo individualmente
        for file_path in file_paths:
            try:
                # Intentar cargar el archivo
                documents = self.load_file(file_path)
                all_documents.extend(documents)
                
            except Exception as e:
                # Si falla, agregar a la lista de errores
                print(f"⚠️ Saltando archivo con error: {file_path}")
                failed_files.append(file_path)
        
        # Mostrar resumen
        print(f"\n📊 Resumen de carga:")
        print(f"   ✅ Exitosos: {len(file_paths) - len(failed_files)}")
        print(f"   ❌ Con errores: {len(failed_files)}")
        print(f"   📄 Total documentos: {len(all_documents)}\n")
        
        return all_documents, failed_files
    
    def split_documents(self, documents):
        """
        Divide documentos en fragmentos (chunks) más pequeños.
        
        ¿Por qué dividir?
        - Los documentos grandes no caben en el contexto del LLM
        - Fragmentos pequeños permiten búsqueda más precisa
        - Cada fragmento puede ser recuperado independientemente
        
        Proceso:
        1. RecursiveCharacterTextSplitter intenta dividir por párrafos
        2. Si un párrafo es muy grande, divide por oraciones
        3. Si una oración es muy grande, divide por caracteres
        
        Args:
            documents (list): Lista de documentos de LangChain
            
        Returns:
            list: Lista de fragmentos (chunks) de documentos
            
        Ejemplo:
            >>> processor = DocumentProcessor()
            >>> docs = processor.load_file("libro.pdf")  # 500 páginas
            >>> chunks = processor.split_documents(docs)
            >>> print(f"Dividido en {len(chunks)} fragmentos")
            Dividido en 2450 fragmentos
        """
        if not documents:
            print("⚠️ No hay documentos para dividir")
            return []
        
        print(f"✂️ Dividiendo {len(documents)} documento(s) en fragmentos...")
        print(f"   📏 Tamaño del fragmento: {self.chunk_size} caracteres")
        print(f"   🔗 Superposición: {self.chunk_overlap} caracteres")
        
        # Dividir los documentos usando el text splitter
        splits = self.text_splitter.split_documents(documents)
        
        print(f"✅ Creados {len(splits)} fragmentos\n")
        
        return splits
    
    def process_files(self, file_paths):
        """
        Método principal: carga y procesa archivos en un solo paso.
        
        Este es el método "todo en uno" que ejecuta:
        1. Carga de archivos
        2. División en fragmentos
        3. Validación del resultado
        
        Args:
            file_paths (list): Lista de rutas a archivos
            
        Returns:
            dict: Diccionario con el resultado del procesamiento
                {
                    'success': bool,        # True si todo fue exitoso
                    'splits': list,         # Lista de fragmentos procesados
                    'document_count': int,  # Número de documentos originales
                    'split_count': int,     # Número de fragmentos creados
                    'failed_files': list,   # Archivos que fallaron
                    'message': str          # Mensaje descriptivo
                }
                
        Ejemplo:
            >>> processor = DocumentProcessor()
            >>> files = ["doc1.pdf", "doc2.txt"]
            >>> result = processor.process_files(files)
            >>> if result['success']:
            ...     print(f"Procesados {result['split_count']} fragmentos")
        """
        # Validar entrada
        if not file_paths:
            return {
                'success': False,
                'splits': [],
                'document_count': 0,
                'split_count': 0,
                'failed_files': [],
                'message': "⚠️ No se proporcionaron archivos para procesar"
            }
        
        # Paso 1: Cargar archivos
        documents, failed_files = self.load_multiple_files(file_paths)
        
        # Verificar si se cargó algún documento
        if not documents:
            return {
                'success': False,
                'splits': [],
                'document_count': 0,
                'split_count': 0,
                'failed_files': failed_files,
                'message': "❌ No se pudieron cargar documentos válidos"
            }
        
        # Paso 2: Dividir documentos en fragmentos
        splits = self.split_documents(documents)
        
        # Verificar si se crearon fragmentos
        if not splits:
            return {
                'success': False,
                'splits': [],
                'document_count': len(documents),
                'split_count': 0,
                'failed_files': failed_files,
                'message': "❌ Los documentos están vacíos o no se pudieron dividir"
            }
        
        # Éxito: retornar resultado completo
        return {
            'success': True,
            'splits': splits,
            'document_count': len(documents),
            'split_count': len(splits),
            'failed_files': failed_files,
            'message': f"✅ Procesados {len(splits)} fragmentos de {len(documents)} documento(s)"
        }

# ==============================================================================
# NOTAS PARA ESTUDIANTES
# ==============================================================================
"""
📚 CONCEPTOS IMPORTANTES:

1. CHUNKING (FRAGMENTACIÓN):
   - Dividir texto largo en piezas más pequeñas
   - Crítico para RAG: permite búsqueda precisa
   - Balance entre contexto y precisión
   
2. TEXT SPLITTER:
   - RecursiveCharacterTextSplitter es "inteligente"
   - Intenta dividir por párrafos primero
   - Mantiene oraciones completas cuando es posible
   - La superposición evita pérdida de contexto
   
3. LOADERS:
   - Cada tipo de archivo necesita un loader específico
   - PyPDFLoader: extrae texto de PDFs página por página
   - TextLoader: lee archivos de texto plano
   - LangChain tiene loaders para muchos formatos
   
4. MANEJO DE ERRORES:
   - try/except para capturar errores
   - raise para propagar errores críticos
   - Retornar diccionarios con información detallada
   
5. DOCUMENTACIÓN:
   - Cada método tiene un docstring explicativo
   - Los ejemplos ayudan a entender el uso
   - Los comentarios aclaran decisiones de diseño

💡 EXPERIMENTOS SUGERIDOS:
   1. Cambia CHUNK_SIZE a 500 y observa cuántos fragmentos se crean
   2. Prueba CHUNK_OVERLAP = 0 y compara la calidad de las respuestas
   3. Agrega soporte para archivos .docx (usa DocxLoader de LangChain)
   
⚠️ PREGUNTAS PARA REFLEXIONAR:
   - ¿Qué pasa si el chunk es muy pequeño (ej: 100 caracteres)?
   - ¿Por qué es importante la superposición entre chunks?
   - ¿Cómo afecta el tamaño del chunk a la velocidad de búsqueda?
"""
