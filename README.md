Conversational B2B Contract Analyst & Procurement Copilot

An enterprise-grade, AI-driven contract analysis platform built to eliminate legal bottlenecks, automate risk assessment, and provide instant answers to complex B2B vendor agreements.

🚀 Overview

Reviewing legal contracts is traditionally time-consuming, expensive, and prone to oversight regarding hidden financial penalties or restrictive clauses. The Conversational B2B Contract Analyst acts as an intelligent procurement copilot. It ingests complex PDF contracts, automatically structures critical metrics upon upload, and empowers users to query the document using natural language—backed by a strict "Never-Lie" hallucination shield.

✨ Key Features

📊 Auto-Extraction Dashboard: Instantly summarizes uploaded agreements upon upload, categorizing key timelines, financial terms, payment obligations, and hidden risk flags.

📄 Native Side-by-Side Document Viewer: Displays the original source PDF side-by-side with the conversational copilot for immediate visual verification.

💬 Interactive Procurement Copilot: Features pre-built quick prompts and a conversational interface to answer targeted legal and financial questions.

🛡️ 'Never-Lie' Security Shield: Powered by advanced Retrieval-Augmented Generation (RAG) guardrails. If requested data is missing from the document, the system explicitly states that the information is not present rather than fabricating legal terms.

🛠️ System Architecture & Tech Stack

Frontend & UI: Streamlit (with custom CSS for a modern, responsive enterprise SaaS layout)

AI Orchestration: LangChain (LCEL - LangChain Expression Language)

Vector Database: ChromaDB (Local semantic vector storage and retrieval)

Generative AI & Embeddings: Google Gemini API (gemini-3.6-flash for reasoning/generation, gemini-embedding-001 for vector embedding)

Document Processing: PyPDF & Recursive Character Text Splitting

💻 Installation & Local Setup

Clone the repository:

git clone https://github.com/YOUR_USERNAME/b2b-contract-analyst.git
cd b2b-contract-analyst



Create and activate a virtual environment:

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate



Install dependencies:

pip install -r requirements.txt



Set up your environment variables:
Create a .env file in the root directory and add your Google Gemini API key:

GOOGLE_API_KEY=your_actual_api_key_here



Run the application:

streamlit run app.py

