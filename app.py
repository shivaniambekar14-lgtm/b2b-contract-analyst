import streamlit as st
import base64
import os
from pipeline import ingest_pdf, get_rag_chain, auto_extract_metrics

st.set_page_config(
    page_title="B2B Contract Analyst", 
    page_icon="⚖️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    /* Premium Off-White App Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Sleek Dark Mode Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
        min-width: 450px !important;
    }
    
    /* Sidebar Text Colors */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #94A3B8 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    
    /* Main Typography */
    h1 {
        color: #1E293B !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px;
        padding-bottom: 5px;
    }
    
    /* Floating Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    
    /* Dashboard Expander Styling */
    [data-testid="stExpander"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    /* Custom divider */
    hr {
        border-color: #E2E8F0;
        margin-top: 30px;
        margin-bottom: 30px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="750" type="application/pdf" style="border-radius: 12px; border: 1px solid #CBD5E1; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚖️ Workspace")
    st.markdown("Upload a vendor contract to begin the analysis.")
    
    uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])
    
    if uploaded_file is not None:
        st.markdown("---")
        if st.button("🗑️ Reset / Clear Workspace", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            if os.path.exists("temp_contract.pdf"):
                os.remove("temp_contract.pdf")
            st.rerun()

    st.markdown("---")
    st.markdown("**System Architecture**")
    st.markdown("🔹 **Frontend:** Streamlit\n🔹 **Vector DB:** Chroma\n🔹 **LLM Brain:** Gemini 3.6 Flash\n🔹 **Pipeline:** LangChain LCEL")

st.title("Conversational B2B Contract Analyst")

if uploaded_file is None:
    st.info("👈 Please upload a PDF contract in the sidebar on the left to activate the Copilot.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📊 Auto-Extraction")
        st.markdown("Automatically identifies key timelines, financial penalties, and hidden traps upon upload.")
    with col2:
        st.markdown("### 💬 Interactive Chat")
        st.markdown("Ask complex legal questions in plain English and get grounded, accurate answers.")
    with col3:
        st.markdown("### 🛡️ 'Never-Lie' Shield")
        st.markdown("Powered by RAG architecture to completely eliminate AI hallucinations.")

else:
    temp_path = "temp_contract.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    with st.spinner("Analyzing contract and extracting metrics..."):
        if "vectorstore" not in st.session_state:
            st.session_state.vectorstore = ingest_pdf(temp_path)
            st.session_state.summary = auto_extract_metrics(st.session_state.vectorstore)
            
    st.success("✅ Document Ingested & Analyzed!")
    
    with st.expander("📊 Auto-Generated Contract Summary (Timelines, Financials, Risks)", expanded=True):
        st.write(st.session_state.summary)

    st.markdown("---")
    
    col_pdf, col_chat = st.columns([1, 1], gap="large")
    
    with col_pdf:
        st.subheader("📄 Original Document")
        display_pdf(temp_path)
        
    with col_chat:
        st.subheader("💬 Procurement Copilot")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        st.markdown("**⚡ Quick Prompts:**")
        qcol1, qcol2, qcol3 = st.columns(3)
        quick_prompt = None
        with qcol1:
            if st.button("🚨 Termination"):
                quick_prompt = "What are the terms and conditions for terminating this contract?"
        with qcol2:
            if st.button("💰 Financials"):
                quick_prompt = "What are the financial terms, fees, and penalties mentioned?"
        with qcol3:
            if st.button("🛡️ Liabilities"):
                quick_prompt = "What are the liability and indemnification clauses?"

        prompt = st.chat_input("Ask a question (e.g., 'What is the penalty for late delivery?')...")
        
        if quick_prompt:
            prompt = quick_prompt

        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            chain = get_rag_chain(st.session_state.vectorstore)
            answer = chain.invoke(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})