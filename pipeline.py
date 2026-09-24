import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Initialize Gemini Models (UPDATED to the latest 2026 supported models)
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def ingest_pdf(file_path):
    """Reads the PDF, chunks it, and saves it to a local Chroma database."""
    # 1. Load the document
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Chunking (The Paper Shredder)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Vector DB (The Smart Filing Cabinet)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")
    return vectorstore

def get_rag_chain(vectorstore):
    """Sets up the modern LCEL retrieval logic with the 'Never-Lie' security shield."""
    # We are increasing 'k' from 4 to 10. 
    # Now the AI will read 10 chunks at a time before answering!
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    
    # The Strict Prompt to prevent hallucinations
    system_prompt = (
        "You are a B2B Contract Analyst Copilot. "
        "Use the following retrieved contract text chunks to answer the question. "
        "If the requested information is not explicitly written in these chunks, you MUST clearly state: "
        "'This information is not present in the contract.' "
        "Do not invent or guess any legal terms, dates, or financial penalties. "
        "\n\nContext:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Helper to format retrieved chunks into readable text
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    # The Modern LCEL Pipeline (Bypasses the old 'chains' import entirely!)
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def auto_extract_metrics(vectorstore):
    """Automatically extracts timelines, financials, and risks upon upload."""
    chain = get_rag_chain(vectorstore)
    
    query = (
        "Summarize the most important details of this contract. "
        "Provide exactly 3 bullet points for: 1. Key Timeline (dates), "
        "2. Financial Terms (costs/penalties), and 3. Risk Flags (lock-ins or traps)."
    )
    
    # Run the query through our new LCEL chain
    response = chain.invoke(query)
    return response