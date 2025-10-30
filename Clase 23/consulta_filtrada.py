import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Definir el modelo y el directorio de la DB (deben ser los mismos)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "db_chroma"

def main(query_text, source_filter=None):
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
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    print(f"Realizando búsqueda por similitud para: '{query_text}'")
    if source_filter:
        print(f"Filtrando por fuente: {source_filter}\n")
    else:
        print()

    # 4. Realizar la búsqueda por similitud CON FILTRO opcional
    if source_filter:
        results = vectordb.similarity_search(
            query_text, 
            k=3,
            filter={"source": source_filter}
        )
    else:
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
    # Uso: python consulta_filtrada.py "¿Qué es LangChain?" datos.txt
    if len(sys.argv) > 1:
        query = sys.argv[1]
        source = sys.argv[2] if len(sys.argv) > 2 else None
        main(query, source)
    else:
        print("Error: Debes pasar tu consulta como argumento.")
        print("Ejemplo: python consulta_filtrada.py '¿Qué es LangChain?'")
        print("O con filtro: python consulta_filtrada.py '¿Qué es LangChain?' datos.txt")
