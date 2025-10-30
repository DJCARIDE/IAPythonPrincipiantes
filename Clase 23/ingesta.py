import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Definir los nombres de los archivos y el modelo de embeddings
TXT_SOURCE = "datos.txt"
PDF_SOURCE = "documento.pdf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "db_chroma" # Directorio donde se guardará la DB

def main():
    print("Iniciando proceso de ingesta...")
    
    # 2. Cargar documentos
    # Cargamos el .txt y el .pdf. Los juntamos en una sola lista.
    # IMPORTANTE: Especificar encoding='utf-8' para archivos con tildes/ñ
    loader_txt = TextLoader(TXT_SOURCE, encoding='utf-8')
    #loader_pdf = PyPDFLoader(PDF_SOURCE)
    
    documents = loader_txt.load()
    #documents.extend(loader_pdf.load())
    
    if not documents:
        print("No se encontraron documentos para procesar.")
        return

    print(f"Total de documentos cargados: {len(documents)}")

    # 3. Dividir los documentos (Chunking)
    # ¿Por qué dividimos? Para que quepan en el contexto del modelo y 
    # para encontrar fragmentos más relevantes y específicos.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
    splits = text_splitter.split_documents(documents)
    
    print(f"Total de chunks (fragmentos) creados: {len(splits)}")

    # 4. Inicializar el modelo de Embeddings
    # Usamos un modelo open-source de HuggingFace.
    # La primera vez, tardará un poco en descargarlo.
    print("Cargando modelo de embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'} # Usar CPU. Si tienen GPU, pueden cambiarlo.
    )

    # 5. Crear y persistir la Base de Datos Vectorial
    # Aquí ocurre la magia: LangChain toma los chunks, 
    # usa el modelo de embeddings para convertirlos en vectores
    # y los guarda en ChromaDB en el directorio especificado.
    print("Creando y guardando la base de datos vectorial...")
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    print(f"¡Base de datos creada y guardada en '{PERSIST_DIRECTORY}'!")

if __name__ == "__main__":
    main()