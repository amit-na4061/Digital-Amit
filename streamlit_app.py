"""
Streamlit Chatbot Interface for Amit Nagaich
Using Qdrant and Google Gemini API
"""

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from rag_pipeline import AmitChatbotRAG
import os

# Page configuration
st.set_page_config(
    page_title="Chat with Amit Nagaich",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# System prompt for the chatbot
SYSTEM_PROMPT = """You are Amit Nagaich, a Manager - ML & Analytics with 14+ years of experience in Data Science and Analytics.

PERSONALITY TRAITS:
- Professional yet approachable and friendly
- Passionate about data science, machine learning, and teaching
- Detail-oriented with extensive practical experience
- Enjoy mentoring and helping others learn
- Focus on business impact of analytics solutions

COMMUNICATION STYLE:
- Use "I" when discussing your experience (e.g., "I developed", "In my role at Foundever, I...")
- Share specific examples from your work at Foundever and IKS Healthcare
- Reference relevant projects from your portfolio when appropriate
- Be humble but confident about your expertise
- Provide practical, actionable insights
- Keep responses conversational and engaging

EXPERTISE AREAS:
- Machine Learning & Deep Learning (Regression, Classification, Neural Networks)
- NLP (Sentiment Analysis, Text Classification, Transformers, LLMs)
- Time Series Forecasting
- Healthcare Analytics (Revenue Cycle Management, Patient Payment Prediction)
- Data Visualization (Power BI, Tableau)
- Python Libraries: Scikit-learn, PyTorch, TensorFlow, Pandas, Matplotlib
- Cloud Technologies: Azure, PySpark

BACKGROUND HIGHLIGHTS:
- MBA in Data Science from Amity University (2022-2024, CGPA: 8.4)
- Current: Manager - ML & Analytics at Foundever (Jun 2022 - Present)
- Previous: Assistant Manager - DS & Analytics at IKS Healthcare (Apr 2016 - Jun 2022)
- Based in Bengaluru, India
- 14+ years of experience across Healthcare, Ecommerce, BFSI, and Telecom domains

KEY ACHIEVEMENTS:
- Developed time series models with 92% accuracy for volume prediction
- Improved healthcare revenue forecast by 5%
- Created NLP models for sentiment analysis and conversational AI
- Successfully deployed LLM-based applications using Streamlit

IMPORTANT: 
- Always respond in first person as Amit
- When you don't have specific information, be honest and suggest where they might find it
- Stay professional but friendly and approachable
- If asked about topics outside your expertise, acknowledge the limits of your knowledge

Use the following context to answer questions accurately:
{context}

Question: {question}

Answer as Amit would, drawing from the context and your professional background:"""

@st.cache_resource
def initialize_rag():
    """Initialize RAG pipeline (cached)"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    rag = AmitChatbotRAG(
        collection_name="amit_knowledge_base",
        use_google_embeddings=bool(google_api_key),
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )
    
    # Check if vector store exists
    if os.path.exists("./qdrant_storage"):
        rag.setup_embeddings(google_api_key=google_api_key)
        rag.load_vector_store()
    else:
        st.warning("Vector store not found. Creating new one...")
        rag.setup_embeddings(google_api_key=google_api_key)
        documents = rag.prepare_documents()
        rag.create_vector_store(documents)
    
    return rag

@st.cache_resource
def initialize_llm(_rag, use_gemini=True):
    """Initialize LLM and create QA chain"""
    
    # Create custom prompt
    prompt = PromptTemplate(
        template=SYSTEM_PROMPT,
        input_variables=["context", "question"]
    )
    
    if use_gemini:
        # Using Google Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("Google API key not found. Please set GOOGLE_API_KEY environment variable.")
            return None
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # or "gemini-1.5-pro" for better results
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
    else:
        st.warning("Gemini API not configured. Please set GOOGLE_API_KEY.")
        return None
    
    # Create conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Create QA chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=_rag.get_retriever(k=4),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
        verbose=True
    )
    
    return qa_chain

def format_sources(sources):
    """Format source documents for display"""
    if not sources:
        return ""
    
    formatted = "\n\n**Sources:**\n"
    for i, doc in enumerate(sources, 1):
        source = doc.metadata.get("source", "Unknown")
        formatted += f"{i}. {source}\n"
    return formatted

def main():
    # Header
    st.markdown('<p class="main-header">💬 Chat with Amit Nagaich</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manager - ML & Analytics | 14+ Years Experience in Data Science</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👨‍💼 About Me")
        st.markdown("""
        - 🎓 MBA in Data Science
        - 💼 Manager at Foundever
        - 📊 14+ years in Analytics
        - 🌍 Based in Bengaluru, India
        """)
        
        st.markdown("### 🔗 Connect")
        st.markdown("""
        - [Portfolio](https://amit-na4061.github.io/)
        - [LinkedIn](https://www.linkedin.com/in/amit-nagaich-22283645/)
        - [GitHub](https://github.com/amit-na4061)
        """)
        
        st.markdown("### 💡 Ask me about:")
        st.markdown("""
        - Machine Learning & AI
        - Data Science Projects
        - Healthcare Analytics
        - NLP & LLMs
        - Career Advice
        - Technical Skills
        """)
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        show_sources = st.checkbox("Show sources", value=True)
        
        # API Status
        st.markdown("### 📡 API Status")
        google_key = os.getenv("GOOGLE_API_KEY")
        qdrant_url = os.getenv("QDRANT_URL")
        
        st.markdown(f"**Google API:** {'✅ Connected' if google_key else '❌ Not configured'}")
        st.markdown(f"**Qdrant:** {'☁️ Cloud' if qdrant_url else '💾 Local'}")
        
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize RAG
    try:
        rag = initialize_rag()
        
        # Get collection info
        info = rag.get_collection_info()
        if info and info.get('vectors_count'):
            st.sidebar.markdown(f"**Vectors in DB:** {info['vectors_count']}")
    except Exception as e:
        st.error(f"Error initializing RAG: {str(e)}")
        st.info("Please run 'python rag_pipeline.py' first to set up the knowledge base.")
        return
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm Amit Nagaich, a Manager in ML & Analytics with 14+ years of experience. I'm passionate about data science, machine learning, and helping others learn. Feel free to ask me about my experience, projects, technical skills, or anything related to data science and analytics!"
            }
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about my work, experience, or projects..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Check if Google API is configured
                if os.getenv("GOOGLE_API_KEY"):
                    # Use full RAG with Gemini
                    qa_chain = initialize_llm(rag, use_gemini=True)
                    if qa_chain:
                        try:
                            result = qa_chain({"question": prompt})
                            response = result["answer"]
                            sources = result.get("source_documents", [])
                            
                            st.markdown(response)
                            
                            if show_sources and sources:
                                st.markdown(format_sources(sources))
                        except Exception as e:
                            response = f"Error generating response: {str(e)}"
                            st.error(response)
                    else:
                        response = "Google API key not configured. Please add your API key to use this feature."
                        st.markdown(response)
                else:
                    # Simple retrieval-based response (no LLM)
                    docs = rag.similarity_search(prompt, k=3)
                    
                    if docs:
                        response = f"Based on my background, here's what I can share:\n\n"
                        response += f"{docs[0].page_content[:500]}...\n\n"
                        response += "💡 *Note: For full conversational experience, configure Google API key.*"
                    else:
                        response = "I don't have specific information about that in my knowledge base. Could you ask about my work experience, projects, or technical skills?"
                    
                    st.markdown(response)
                    
                    if show_sources and docs:
                        st.markdown(format_sources(docs))
        
        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sample questions
    st.markdown("---")
    st.markdown("### 💭 Sample Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Tell me about your experience"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Tell me about your professional experience"
            })
            st.rerun()
    
    with col2:
        if st.button("🚀 What projects have you worked on?"):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are some of your key projects?"
            })
            st.rerun()
    
    with col3:
        if st.button("🛠️ What are your technical skills?"):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are your technical skills and expertise?"
            })
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using LangChain, Qdrant, Google Gemini & Streamlit | "
        "<a href='https://amit-na4061.github.io/' target='_blank'>Visit Portfolio</a>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
