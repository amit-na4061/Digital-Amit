"""
FastAPI Backend for Amit Nagaich Chatbot
Using Qdrant and Google Gemini API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uvicorn
import os
from datetime import datetime
from rag_pipeline import AmitChatbotRAG
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Amit Nagaich Chatbot API",
    description="RAG-powered chatbot using Qdrant and Google Gemini",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt
SYSTEM_PROMPT = """You are Amit Nagaich, a Manager - ML & Analytics with 14+ years of experience.

RESPOND AS AMIT IN FIRST PERSON:
- Use "I" when discussing your experience
- Reference specific projects and achievements
- Be professional yet approachable
- Share practical insights from your work at Foundever and IKS Healthcare

EXPERTISE: ML, Deep Learning, NLP, Healthcare Analytics, Time Series Forecasting, Data Visualization

Context from knowledge base:
{context}

Question: {question}

Answer (as Amit):"""

# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message/question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    include_sources: bool = Field(True, description="Include source documents in response")
    max_sources: int = Field(3, description="Maximum number of source documents to return")

class SourceDocument(BaseModel):
    content: str
    source: str
    metadata: Dict

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[List[SourceDocument]] = None
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    message: str
    vector_store_ready: bool
    api_configured: bool
    vectors_count: Optional[int] = None

class ProfileResponse(BaseModel):
    name: str
    role: str
    experience_years: int
    location: str
    email: str
    linkedin: str
    github: str
    portfolio: str
    skills: List[str]
    domains: List[str]

# Global variables
rag_pipeline = None
qa_chains = {}  # Store QA chains per session

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global rag_pipeline
    
    logger.info("Initializing RAG pipeline...")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    rag_pipeline = AmitChatbotRAG(
        collection_name="amit_knowledge_base",
        use_google_embeddings=bool(google_api_key),
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )
    
    # Check if vector store exists
    if os.path.exists("./qdrant_storage") or qdrant_url:
        try:
            rag_pipeline.setup_embeddings(google_api_key=google_api_key)
            rag_pipeline.load_vector_store()
            logger.info("✓ RAG pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            logger.info("Creating new vector store...")
            rag_pipeline.setup_embeddings(google_api_key=google_api_key)
            documents = rag_pipeline.prepare_documents()
            rag_pipeline.create_vector_store(documents)
    else:
        logger.info("Vector store not found. Creating new one...")
        rag_pipeline.setup_embeddings(google_api_key=google_api_key)
        documents = rag_pipeline.prepare_documents()
        rag_pipeline.create_vector_store(documents)
        logger.info("✓ New vector store created")

def get_or_create_qa_chain(session_id: str):
    """Get existing QA chain or create new one for session"""
    if session_id not in qa_chains:
        # Check for Google API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # or "gemini-1.5-pro"
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Create prompt
        prompt = PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["context", "question"]
        )
        
        # Create memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=rag_pipeline.get_retriever(k=4),
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": prompt}
        )
        
        qa_chains[session_id] = qa_chain
    
    return qa_chains[session_id]

@app.get("/", response_model=Dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Amit Nagaich Chatbot API",
        "version": "2.0.0",
        "tech_stack": {
            "vector_db": "Qdrant",
            "llm": "Google Gemini",
            "framework": "LangChain"
        },
        "endpoints": {
            "chat": "/chat",
            "profile": "/profile",
            "health": "/health",
            "search": "/search"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    vector_store_ready = rag_pipeline is not None and rag_pipeline.vectorstore is not None
    api_configured = bool(os.getenv("GOOGLE_API_KEY"))
    
    vectors_count = None
    if vector_store_ready:
        try:
            info = rag_pipeline.get_collection_info()
            vectors_count = info.get('vectors_count')
        except:
            pass
    
    return HealthResponse(
        status="healthy" if (vector_store_ready and api_configured) else "degraded",
        message="All systems operational" if (vector_store_ready and api_configured) else "Some services unavailable",
        vector_store_ready=vector_store_ready,
        api_configured=api_configured,
        vectors_count=vectors_count
    )

@app.get("/profile", response_model=ProfileResponse)
async def get_profile():
    """Get Amit's profile information"""
    return ProfileResponse(
        name="Amit Nagaich",
        role="Manager - ML & Analytics",
        experience_years=14,
        location="Bengaluru, India",
        email="amit.na4061@gmail.com",
        linkedin="https://www.linkedin.com/in/amit-nagaich-22283645/",
        github="https://github.com/amit-na4061",
        portfolio="https://amit-na4061.github.io/",
        skills=[
            "Python", "SQL", "Machine Learning", "Deep Learning", "NLP",
            "Power BI", "Tableau", "TensorFlow", "PyTorch", "Scikit-learn"
        ],
        domains=[
            "Healthcare", "Ecommerce", "BFSI", "Telecommunication"
        ]
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - main interaction point
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
        
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Get or create QA chain for this session
        try:
            qa_chain = get_or_create_qa_chain(session_id)
            
            # Get response
            result = qa_chain({"question": request.message})
            response_text = result["answer"]
            source_docs = result.get("source_documents", [])
            
        except ValueError as e:
            # Fallback to simple retrieval if no API key
            docs = rag_pipeline.similarity_search(request.message, k=request.max_sources)
            
            if docs:
                response_text = f"Based on my background:\n\n{docs[0].page_content[:500]}..."
                response_text += "\n\n💡 Note: For full conversational experience, configure Google API key."
                source_docs = docs
            else:
                response_text = "I don't have specific information about that. Please ask about my work experience, projects, or technical skills."
                source_docs = []
        
        # Format sources
        sources = None
        if request.include_sources and source_docs:
            sources = [
                SourceDocument(
                    content=doc.page_content[:200] + "...",
                    source=doc.metadata.get("source", "unknown"),
                    metadata=doc.metadata
                )
                for doc in source_docs[:request.max_sources]
            ]
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            sources=sources,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    if session_id in qa_chains:
        del qa_chains[session_id]
        return {"message": f"Session {session_id} cleared"}
    return {"message": "Session not found"}

@app.get("/search")
async def search_knowledge_base(query: str, k: int = 5):
    """
    Search the knowledge base directly
    Useful for debugging or testing retrieval
    """
    try:
        if not rag_pipeline:
            raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
        
        results = rag_pipeline.similarity_search(query, k=k)
        
        return {
            "query": query,
            "results": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """Simple demo page"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat with Amit Nagaich</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            #chat-container {
                border: 1px solid #ddd;
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                margin-bottom: 20px;
                background-color: white;
                border-radius: 8px;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
                max-width: 80%;
            }
            .user {
                background-color: #e3f2fd;
                margin-left: auto;
                text-align: right;
            }
            .assistant {
                background-color: #f5f5f5;
            }
            #input-container {
                display: flex;
                gap: 10px;
            }
            #message-input {
                flex: 1;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #1976d2;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 4px;
            }
            button:hover {
                background-color: #1565c0;
            }
            .loading {
                text-align: center;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💬 Chat with Amit Nagaich</h1>
            <p>Manager - ML & Analytics | 14+ Years Experience</p>
            <p style="color: #666;">Powered by Qdrant & Google Gemini</p>
        </div>
        
        <div id="chat-container"></div>
        
        <div id="input-container">
            <input type="text" id="message-input" placeholder="Ask me anything about my work...">
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value;
                if (!message) return;
                
                // Display user message
                addMessage(message, 'user');
                input.value = '';
                
                // Show loading
                const loadingDiv = addMessage('Thinking...', 'loading');
                
                // Send to API
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });
                    
                    const data = await response.json();
                    
                    // Remove loading message
                    loadingDiv.remove();
                    
                    // Add assistant response
                    addMessage(data.response, 'assistant');
                } catch (error) {
                    loadingDiv.remove();
                    addMessage('Error: ' + error.message, 'assistant');
                }
            }
            
            function addMessage(text, role) {
                const container = document.getElementById('chat-container');
                const div = document.createElement('div');
                div.className = 'message ' + role;
                div.textContent = text;
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
                return div;
            }
            
            document.getElementById('message-input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
            
            // Welcome message
            addMessage("Hi! I'm Amit Nagaich. Ask me about my experience, projects, or data science expertise!", 'assistant');
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
