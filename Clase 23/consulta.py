import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Definir el modelo y el directorio de la DB (deben ser los mismos)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "db_chroma"

def main(query_text):
    if not query_text:
        print("Por favor, proporciona un texto para la consulta.")
        return

    print("Cargando modelo de embeddings y base de datos...")
    
    # 2. Cargar el modelo de Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'}
    )

    # 3. Cargar la base de datos vectorial persistente
    # OJO: Esta vez no usamos 'from_documents', sino que cargamos
    # la que ya existe desde el disco.
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    print(f"Realizando búsqueda MMR para: '{query_text}'\n")

    # 4. Realizar la búsqueda
    # Hay diferentes métodos de búsqueda:
    
    # MÉTODO 1: Búsqueda simple por similitud (comentado)
    # Este método devuelve los documentos más similares a la consulta.
    # Problema: Puede devolver resultados muy parecidos entre sí (redundantes).
    # results = vectordb.similarity_search(query_text, k=3)
    
    # MÉTODO 2: MMR (Maximum Marginal Relevance) - Búsqueda con diversidad
    # MMR balancea dos cosas:
    # 1) Relevancia: Qué tan relacionado está el documento con tu pregunta
    # 2) Diversidad: Evita resultados repetitivos o muy similares entre sí
    # 
    # Parámetros:
    # - k=3: Queremos 3 documentos finales
    # - fetch_k=20: Primero busca 20 candidatos, luego elige los 3 más diversos
    # - lambda_mult=0.5: Balance entre relevancia (1.0) y diversidad (0.0)
    #   * 0.5 = Balance equilibrado (recomendado)
    #   * 1.0 = Solo importa relevancia (como similarity_search)
    #   * 0.0 = Solo importa diversidad
    # results = vectordb.max_marginal_relevance_search(
    #     query_text, 
    #     k=3,
    #     fetch_k=20,
    #     lambda_mult=0.5
    # )

    results = vectordb.similarity_search(query_text, k=3)

    if not results:
        print("No se encontraron resultados relevantes.")
        return

    # 5. Mostrar los resultados
    print("Resultados encontrados:\n" + "="*30)
    for i, doc in enumerate(results):
        print(f"Resultado {i+1}:")
        print(f"Fuente: {doc.metadata.get('source', 'N/A')}")
        print(f"Página: {doc.metadata.get('page', 'N/A')}") # Útil para PDFs
        print("Contenido:")
        print(doc.page_content)
        print("-" * 30)

if __name__ == "__main__":
    # La consulta se pasa como argumento en la terminal
    if len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        print("Error: Debes pasar tu consulta como argumento.")
        print("Ejemplo: python consulta.py '¿Qué es LangChain?'")