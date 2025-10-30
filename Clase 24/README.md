# 🤖 Chatbot RAG - Proyecto Educativo

## 📋 Descripción

Este es un proyecto educativo que implementa un **Chatbot RAG (Retrieval Augmented Generation)** completamente funcional. El objetivo es enseñar los conceptos fundamentales de IA, LLMs y arquitectura de software a través de código bien documentado y modularizado.

## 🎯 Objetivos de Aprendizaje

Al estudiar este proyecto, los estudiantes aprenderán:

1. ✅ **RAG (Retrieval Augmented Generation)**: Cómo combinar búsqueda con generación
2. ✅ **Bases de Datos Vectoriales**: ChromaDB y embeddings
3. ✅ **LangChain**: Framework para aplicaciones con LLMs
4. ✅ **Arquitectura Modular**: Separación de responsabilidades
5. ✅ **Buenas Prácticas**: Documentación, comentarios, y organización de código

## 🏗️ Arquitectura del Proyecto

```
codigo/
│
├── 📄 config.py                    # Configuración centralizada
├── 📄 database_manager.py          # Gestión de ChromaDB
├── 📄 document_processor.py        # Procesamiento de documentos
├── 📄 rag_chain.py                 # Implementación de RAG
├── 📄 app_refactorizado.py         # Aplicación principal (NUEVO)
├── 📄 app.py                       # Versión original (monolítica)
│
├── 📄 .env                         # Variables de entorno (API keys)
├── 📄 .env.example                 # Plantilla de variables de entorno
├── 📄 requirements.txt             # Dependencias del proyecto
├── 📄 .gitignore                   # Archivos a ignorar en Git
└── 📄 README.md                    # Este archivo
```

### 📦 Descripción de Módulos

#### 1. `config.py` - Configuración
- **Propósito**: Centralizar toda la configuración
- **Contenido**:
  - Constantes del proyecto
  - Configuración de modelos
  - Plantillas de prompts
  - Mensajes de la aplicación

#### 2. `database_manager.py` - Base de Datos Vectorial
- **Propósito**: Gestionar ChromaDB y embeddings
- **Funcionalidades**:
  - Inicializar embeddings
  - Añadir documentos
  - Crear retrievers
  - Obtener estadísticas
  - Limpiar base de datos

#### 3. `document_processor.py` - Procesamiento de Documentos
- **Propósito**: Cargar y procesar archivos
- **Funcionalidades**:
  - Cargar archivos PDF y TXT
  - Dividir en fragmentos (chunks)
  - Validar documentos
  - Manejo de errores

#### 4. `rag_chain.py` - Cadena RAG
- **Propósito**: Implementar el flujo RAG completo
- **Funcionalidades**:
  - Inicializar LLM
  - Crear cadena RAG con LCEL
  - Hacer consultas
  - Obtener respuestas con fuentes

#### 5. `app_refactorizado.py` - Aplicación Principal
- **Propósito**: Integrar todos los módulos e interfaz
- **Funcionalidades**:
  - Interfaz de usuario con Gradio
  - Gestión de chat
  - Carga de archivos
  - Visualización de estadísticas

## 🚀 Cómo Usar

### 1. Instalación

```bash
# Clonar o descargar el proyecto
cd codigo

# Crear entorno virtual (recomendado)
python -m venv nombre_entorno
nombre_entorno\Scripts\activate  # Windows
source nombre_entorno/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key
# GOOGLE_API_KEY="tu-api-key-aqui"
```

### 3. Ejecución

**Opción A: Versión Modular (Recomendada para aprender)**
```bash
python app_refactorizado.py
```

**Opción B: Versión Original**
```bash
python app.py
```

### 4. Uso de la Interfaz

1. **Cargar Documentos**:
   - Ve a la pestaña "📚 Base de Conocimiento"
   - Sube archivos PDF o TXT
   - Haz clic en "Analizar y Cargar Archivos"

2. **Hacer Preguntas**:
   - Ve a la pestaña "💬 Chatbot"
   - Escribe tu pregunta
   - El chatbot responderá basándose en tus documentos

## 📚 Conceptos Clave

### RAG (Retrieval Augmented Generation)

```
Pregunta → Retriever → Documentos Relevantes → LLM → Respuesta
```

**¿Por qué RAG?**
- ✅ Respuestas basadas en datos reales
- ✅ Reduce "alucinaciones" del LLM
- ✅ Conocimiento actualizable sin reentrenar
- ✅ Transparente: puedes ver las fuentes

### Embeddings

Son representaciones numéricas del texto que capturan su significado:

```python
"El gato duerme" → [0.2, 0.8, -0.3, ..., 0.5]  # Vector de 384 dimensiones
"El felino descansa" → [0.19, 0.81, -0.29, ..., 0.48]  # Vector similar
```

### Chunking

Dividir documentos largos en fragmentos manejables:

```
Documento (10,000 palabras)
    ↓
Chunks (1500 caracteres cada uno)
    ↓
~40 fragmentos
```

### LCEL (LangChain Expression Language)

Sintaxis declarativa para construir cadenas:

```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

## 🔧 Personalización

### Cambiar el Modelo LLM

En `config.py`:
```python
LLM_MODEL = "gemini-1.5-pro"  # Más potente pero más lento
```

### Ajustar Tamaño de Chunks

En `config.py`:
```python
CHUNK_SIZE = 1000      # Chunks más pequeños
CHUNK_OVERLAP = 100    # Menos superposición
```

### Modificar el Prompt

En `config.py`, edita `RAG_PROMPT_TEMPLATE`:
```python
RAG_PROMPT_TEMPLATE = """
Eres un profesor experto. Explica la respuesta paso a paso...
"""
```

## 📊 Comparación: Monolítico vs Modular

| Aspecto | app.py (Original) | app_refactorizado.py (Modular) |
|---------|-------------------|--------------------------------|
| **Líneas de código por archivo** | ~270 | ~200 por módulo |
| **Facilidad de lectura** | Media | Alta |
| **Facilidad de mantenimiento** | Baja | Alta |
| **Reusabilidad** | Baja | Alta |
| **Testing** | Difícil | Fácil |
| **Documentación** | Básica | Extensa |

## 🧪 Ejercicios Propuestos

### Nivel Básico
1. Cambia el tema de Gradio en `config.py`
2. Modifica el prompt para que responda en otro idioma
3. Ajusta `CHUNK_SIZE` y observa los cambios

### Nivel Intermedio
4. Agrega soporte para archivos `.docx`
5. Implementa `query_with_sources()` en la interfaz
6. Añade un contador de tokens en las respuestas

### Nivel Avanzado
7. Implementa un sistema de caché para respuestas
8. Agrega re-ranking de documentos recuperados
9. Crea un modo "conversacional" con memoria

## 🐛 Solución de Problemas

### Error: "No module named 'gradio'"
```bash
pip install gradio
```

### Error: "GOOGLE_API_KEY not found"
```bash
# Verifica que .env exista y tenga:
GOOGLE_API_KEY="tu-key-aqui"
```

### Error: "models/gemini-pro not found"
```python
# En config.py, cambia a:
LLM_MODEL = "gemini-1.5-flash"
```

### La base de datos no se puede borrar
- Usa el botón "Limpiar" en lugar de borrar archivos manualmente
- Si persiste, reinicia la aplicación

## 📖 Recursos Adicionales

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Gradio Docs](https://www.gradio.app/)
- [Google Gemini API](https://ai.google.dev/)

## 🤝 Contribuciones

Este es un proyecto educativo. Se aceptan:
- ✅ Mejoras en la documentación
- ✅ Ejercicios adicionales
- ✅ Correcciones de bugs
- ✅ Traducciones

## 📝 Notas para Instructores

### Secuencia de Enseñanza Sugerida

1. **Sesión 1**: Conceptos básicos (RAG, embeddings, vectores)
2. **Sesión 2**: Revisar `config.py` y `database_manager.py`
3. **Sesión 3**: Estudiar `document_processor.py`
4. **Sesión 4**: Analizar `rag_chain.py` y LCEL
5. **Sesión 5**: Integración en `app_refactorizado.py`
6. **Sesión 6**: Ejercicios prácticos y personalización

### Puntos Clave a Enfatizar

- 🎯 **Modularización**: Por qué y cómo separar responsabilidades
- 🎯 **Documentación**: Importancia de docstrings y comentarios
- 🎯 **RAG**: Ventajas sobre LLMs puros
- 🎯 **Embeddings**: Cómo funciona la búsqueda vectorial

## 📄 Licencia

Este proyecto es de código abierto con fines educativos.

---

💡 **Proyecto creado para Clase 24 - IA Python para Principiantes**

🎓 **¿Preguntas?** Revisa los comentarios en el código - ¡están ahí para ayudarte!
