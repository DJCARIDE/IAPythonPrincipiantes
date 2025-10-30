# ============================================================================
# PASO SIGUIENTE: CONECTAR UN LLM PARA RESPONDER PREGUNTAS CON RAG
# ============================================================================
# Este es un ejemplo conceptual de cómo conectar tu base vectorial con un LLM
# para crear un sistema de Preguntas y Respuestas (RAG = Retrieval Augmented Generation)

# IMPORTS ACTUALIZADOS (estructura moderna de LangChain)
# -------------------------------------------------------
# Para LLMs, ahora cada proveedor tiene su propio paquete:
# from langchain_openai import ChatOpenAI        # Para OpenAI/ChatGPT
# from langchain_anthropic import ChatAnthropic  # Para Claude
# from langchain_google_genai import ChatGoogleGenerativeAI  # Para Gemini
# from langchain_ollama import ChatOllama        # Para modelos locales con Ollama
# from langchain_groq import ChatGroq            # Para Groq (rápido y gratuito)

# Para las chains de Q&A:
# from langchain.chains import RetrievalQA  # ⚠️ DEPRECADO
# from langchain.chains import create_retrieval_chain  # ✅ RECOMENDADO (nuevo)
# from langchain.chains.combine_documents import create_stuff_documents_chain

# Para la base vectorial:
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma


# EJEMPLO 1: USANDO OPENAI (requiere API key y créditos)
# -------------------------------------------------------
# import os
# os.environ["OPENAI_API_KEY"] = "tu-api-key-aqui"
# 
# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",  # o "gpt-4"
#     temperature=0  # 0 = más determinista, 1 = más creativo
# )


# EJEMPLO 2: USANDO GROQ (gratuito, rápido, requiere API key)
# ------------------------------------------------------------
# import os
# os.environ["GROQ_API_KEY"] = "tu-api-key-aqui"
# 
# from langchain_groq import ChatGroq
# llm = ChatGroq(
#     model="llama-3.1-70b-versatile",  # Modelo gratuito y potente
#     temperature=0
# )


# EJEMPLO 3: USANDO OLLAMA (100% local, sin API key, sin internet)
# -----------------------------------------------------------------
# Primero instala Ollama desde: https://ollama.ai
# Luego descarga un modelo: ollama pull llama3.2
# 
# from langchain_ollama import ChatOllama
# llm = ChatOllama(
#     model="llama3.2",  # o "mistral", "phi3", etc.
#     temperature=0
# )


# CARGAR LA BASE VECTORIAL
# -------------------------
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     model_kwargs={'device': 'cpu'}
# )
# 
# vectordb = Chroma(
#     persist_directory="db_chroma",
#     embedding_function=embeddings
# )
# 
# # Crear el retriever (recuperador de documentos)
# retriever = vectordb.as_retriever(
#     search_type="mmr",  # Usar MMR para diversidad
#     search_kwargs={"k": 3, "fetch_k": 20}  # Parámetros de búsqueda
# )


# MÉTODO ANTIGUO (DEPRECADO) ⚠️
# ------------------------------
# from langchain.chains import RetrievalQA
# 
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",  # "stuff" mete todos los docs en el prompt
#     retriever=retriever
# )
# respuesta = qa_chain.run("¿Qué es LangChain?")  # .run() está deprecado
# print(respuesta)


# MÉTODO MODERNO (RECOMENDADO) ✅
# --------------------------------
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# 
# # 1. Crear un prompt personalizado
# system_prompt = (
#     "Eres un asistente útil. Usa el siguiente contexto para responder la pregunta. "
#     "Si no sabes la respuesta, di que no lo sabes. No inventes información.\n\n"
#     "Contexto: {context}"
# )
# 
# prompt = ChatPromptTemplate.from_messages([
#     ("system", system_prompt),
#     ("human", "{input}")
# ])
# 
# # 2. Crear la chain de documentos
# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# 
# # 3. Crear la chain de recuperación completa
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)
# 
# # 4. Hacer una pregunta (usa .invoke() en vez de .run())
# resultado = rag_chain.invoke({"input": "¿Qué es LangChain?"})
# 
# print("Respuesta:", resultado["answer"])
# print("\nDocumentos usados:")
# for i, doc in enumerate(resultado["context"]):
#     print(f"{i+1}. Fuente: {doc.metadata.get('source')}")


# ALTERNATIVA SIMPLE: RETRIEVER + LLM DIRECTO
# --------------------------------------------
# Esta es la forma más simple si solo quieres ver cómo funciona:
# 
# pregunta = "¿Qué es LangChain?"
# 
# # 1. Recuperar documentos relevantes
# docs = retriever.invoke(pregunta)
# 
# # 2. Crear el contexto
# contexto = "\n\n".join([doc.page_content for doc in docs])
# 
# # 3. Crear el prompt manualmente
# prompt_text = f"""Responde la siguiente pregunta basándote en el contexto proporcionado.
# Si no puedes responder con el contexto dado, di que no lo sabes.
# 
# Contexto:
# {contexto}
# 
# Pregunta: {pregunta}
# 
# Respuesta:"""
# 
# # 4. Enviar al LLM
# respuesta = llm.invoke(prompt_text)
# print(respuesta.content)