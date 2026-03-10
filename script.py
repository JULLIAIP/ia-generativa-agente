import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 1. Configuração da API (Substitua pela sua chave)
os.environ["OPENAI_API_KEY"] = "sua_chave_aqui"

def criar_mock_com_rag(caminho_especificacao, query_endpoint):
    # 2. Carregamento e Chunking
    # Suporta PDF ou Texto (OpenAPI spec)
    loader = PyPDFLoader(caminho_especificacao) if caminho_especificacao.endswith('.pdf') else TextLoader(caminho_especificacao)
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    textos = text_splitter.split_documents(documentos)

    # 3. Vector Store (RAG)
    vectorstore = Chroma.from_documents(
        documents=textos, 
        embedding=OpenAIEmbeddings(),
        collection_name="api_specs"
    )

    # 4. Prompt de Sistema focado em Mocking
    template_prompt = """
    Você é um desenvolvedor sênior. Use os trechos da especificação da API abaixo para criar um mock funcional.
    O mock deve ser um script em Node.js usando Express.
    Inclua exemplos de dados realistas baseados nos tipos definidos.
    
    Contexto da Especificação: {context}
    Pergunta do Usuário: {question}
    
    Resposta (Código do Mock):
    """

    # 5. Chain de Inferência
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
    )

    print(f"--- Gerando Mock para: {query_endpoint} ---")
    resposta = qa_chain.invoke(f"Crie o código de um mock para o endpoint {query_endpoint} seguindo o contexto.")
    return resposta["result"]

# Exemplo de uso
# spec_path = "api_v1_docs.pdf"
# print(criar_mock_com_rag(spec_path, "POST /users/create"))