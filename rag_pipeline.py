"""
Personalized RAG Chatbot - Main Pipeline with Qdrant & Google Gemini
Author: Implementation for Amit Nagaich
"""

import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Qdrant
from langchain.document_loaders import WebBaseLoader, TextLoader
from langchain.schema import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmitChatbotRAG:
    """
    RAG pipeline for Amit Nagaich's personalized chatbot
    Using Qdrant Vector Database and Google Gemini API
    """
    
    def __init__(
        self, 
        collection_name: str = "amit_knowledge_base",
        use_google_embeddings: bool = True,
        qdrant_url: str = None,
        qdrant_api_key: str = None
    ):
        """
        Initialize the RAG pipeline
        
        Args:
            collection_name: Name of the Qdrant collection
            use_google_embeddings: Use Google embeddings (True) or HuggingFace (False)
            qdrant_url: Qdrant cloud URL (None for local)
            qdrant_api_key: Qdrant API key (None for local)
        """
        self.collection_name = collection_name
        self.use_google_embeddings = use_google_embeddings
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        self.embeddings = None
        self.vectorstore = None
        self.qdrant_client = None
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def setup_qdrant_client(self):
        """
        Initialize Qdrant client (local or cloud)
        """
        if self.qdrant_url and self.qdrant_api_key:
            # Qdrant Cloud
            logger.info(f"Connecting to Qdrant Cloud: {self.qdrant_url}")
            self.qdrant_client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                timeout=60
            )
        else:
            # Local Qdrant (in-memory or persistent)
            logger.info("Using local Qdrant instance")
            self.qdrant_client = QdrantClient(path="./qdrant_storage")
        
        logger.info("✓ Qdrant client initialized successfully")
        
    def setup_embeddings(self, google_api_key: str = None):
        """
        Initialize embedding model
        
        Args:
            google_api_key: Google API key for Gemini embeddings
        """
        if self.use_google_embeddings:
            if not google_api_key:
                google_api_key = os.getenv("GOOGLE_API_KEY")
                
            if not google_api_key:
                logger.warning("Google API key not found, falling back to HuggingFace embeddings")
                self.use_google_embeddings = False
            else:
                logger.info("Loading Google Gemini embeddings...")
                self.embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=google_api_key
                )
                logger.info("✓ Google Gemini embeddings loaded successfully")
                return
        
        # Fallback to HuggingFace embeddings (free)
        logger.info("Loading HuggingFace embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info("✓ HuggingFace embeddings loaded successfully")
        
    def load_portfolio_data(self) -> List[Document]:
        """Load data from Amit's portfolio website"""
        logger.info("Loading portfolio website data...")
        
        try:
            loader = WebBaseLoader("https://amit-na4061.github.io/")
            documents = loader.load()
            
            # Add metadata
            for doc in documents:
                doc.metadata = {
                    "source": "portfolio_website",
                    "type": "professional_profile",
                    "url": "https://amit-na4061.github.io/"
                }
            
            logger.info(f"✓ Loaded {len(documents)} documents from portfolio")
            return documents
        except Exception as e:
            logger.error(f"Error loading portfolio: {e}")
            return []
    
    def load_custom_knowledge(self, file_path: str = None) -> List[Document]:
        """
        Load custom knowledge base
        This should include LinkedIn content, project details, Q&A pairs
        """
        if file_path and os.path.exists(file_path):
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
                logger.info(f"✓ Loaded custom knowledge from {file_path}")
                return documents
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                return []
        return []
    
    def create_knowledge_base_document(self) -> Document:
        """
        Create a comprehensive knowledge base document about Amit
        """
        knowledge_text = """
# Amit Nagaich - Professional Profile

## Overview
I am Amit Nagaich, a Manager - ML & Analytics with 14+ years of cross-industry experience in Data Science and Analytics. 
I hold an MBA in Data Science and have worked across Healthcare, Ecommerce, BFSI, and Telecommunication sectors.

## Current Role
Manager - ML & Analytics at Foundever (Previously SITEL) since June 2022
- Leading data science initiatives for a global CX leader with 170K associates
- Developing NLP models for text analysis, sentiment detection, and conversational AI
- Building time series forecasting models with 92% accuracy for volume prediction
- Creating mature data science pipelines with feature extraction and model optimization
- Working with transformers and large language models (LLMs) using Streamlit
- Expertise in ML algorithms including XGBoost, Random Forest, Gradient Boosting, SVM

## Previous Experience
Assistant Manager - DS & Analytics at IKS Healthcare (April 2016 - June 2022)
- Implemented demand forecasting for healthcare projects
- Used ML for patient payment prediction, claim processing optimization, fraud detection
- Enhanced revenue forecast by 5% and reduced denial rates
- Delivered training on MS Excel, Power BI, Machine Learning, and Python
- Led Exploratory Data Analysis using statistics and visualizations

## Technical Skills
- Programming: Python (85%), SQL (80%)
- ML/DL: Machine Learning (85%), Deep Learning & NLP (80%)
- Frameworks: Scikit-learn, PyTorch, TensorFlow, Pandas, Matplotlib
- Deep Learning: ANN, CNN, RNN/LSTM for image, video, and text processing
- NLP: Text classification, sentiment analysis, topic modeling, text prediction
- Data Visualization: Power BI (95%), Tableau
- Cloud & Tools: Azure, PySpark, Git, Google Analytics
- Algorithms: Regression, Classification, Ensemble Models, Ada-boost, Gradient Boosting, 
  XGBoost, Random Forest, Decision Tree, SVM, Ridge, Lasso

## Key Projects

### Mental Health Sentiment Analysis
Applied NLP techniques including Word2Vec and ML models to classify mental health statements.
Goal: Early identification and intervention support for mental health professionals.
Technologies: Word2Vec, NLTK, Scikit-learn, Python
Link: https://github.com/amit-na4061/Sentiment-Analysis-for-Mental-Health

### Time Series Sales Forecasting
Used multiple ML models for retail sales forecasting with time series analysis.
Models: ARIMA, SARIMA, Prophet, LSTM
Achievement: 92% accuracy in volume prediction
Link: https://github.com/amit-na4061/DS-Project/tree/main/sales_forecasting

### Crop Classification with Recommendation System
End-to-end ML project for crop classification and cultivation recommendations.
Technologies: Classification algorithms, Feature engineering, Python
Impact: Helping farmers make data-driven cultivation decisions
Link: https://github.com/amit-na4061/DS-Project/blob/main/Recomendation%20Engines/

### Second-hand Car Price Prediction
Predictive modeling project achieving R² of 0.85 on train and test data.
Technologies: Regression algorithms, cross-validation, feature engineering
Tools: Scikit-learn, Pandas, NumPy
Link: https://github.com/amit-na4061/DS-Project/

### Power BI Sales Dashboard
Designed interactive dashboard for Madhav Store tracking online sales across India.
Features: KPI tracking, regional analysis, sales trends, customer segmentation
Tools: Power BI, DAX, Data modeling
Link: https://github.com/amit-na4061/DS-Project/tree/main/Madhav_Store_PowerBI_Dashboard

## Education
- MBA in Data Science, Amity University (2022-2024) - CGPA: 8.4
- Bachelor of Computer Application, Shri Krishna University (2018-2021) - CGPA: 7.4

## Certifications
- Full Stack Data Science and AI Program - NASSCOM ITes SSC (2024)
- Certification ID: FSP/2024/7/10178893

## Domain Expertise
- US Healthcare: Revenue Cycle Management, claim processing, patient payment prediction
- Ecommerce: Sales forecasting, customer analytics, recommendation systems
- BFSI: Fraud detection, risk analysis
- Telecommunication: Customer analytics, churn prediction

## Key Achievements
- Improved revenue forecast by 5% in healthcare RCM
- Achieved 92% accuracy in time series forecasting models
- Reduced denial rates through ML-based claim processing
- Successfully deployed NLP models for conversational AI
- Mentored multiple students and delivered training sessions

## Professional Interests
- Teaching and mentoring aspiring data scientists
- Solving complex business problems with data
- Uncovering hidden stories in data
- Contributing to the advancement of data science field

## Personal Interests
- Traveling and souvenir collection
- Teaching and knowledge sharing
- Exploring new analytical techniques and tools

## Location
Bengaluru, India

## Contact
- Email: amit.na4061@gmail.com
- Phone: +91 99879-99823
- LinkedIn: https://www.linkedin.com/in/amit-nagaich-22283645/
- GitHub: https://github.com/amit-na4061
- Portfolio: https://amit-na4061.github.io/

## Communication Style
I am passionate about data science and enjoy explaining complex concepts in simple terms.
I believe in practical, business-focused analytics solutions and love sharing my knowledge through teaching.
When discussing my work, I focus on the business impact and real-world applications of ML/AI technologies.
I approach problems with a balance of technical rigor and business pragmatism.
"""
        
        return Document(
            page_content=knowledge_text,
            metadata={
                "source": "structured_knowledge_base",
                "type": "comprehensive_profile",
                "version": "1.0"
            }
        )
    
    def prepare_documents(self, additional_files: List[str] = None) -> List[Document]:
        """Prepare all documents for embedding"""
        all_documents = []
        
        # Load portfolio data
        portfolio_docs = self.load_portfolio_data()
        all_documents.extend(portfolio_docs)
        
        # Add structured knowledge base
        all_documents.append(self.create_knowledge_base_document())
        
        # Load additional custom files if provided
        if additional_files:
            for file_path in additional_files:
                custom_docs = self.load_custom_knowledge(file_path)
                all_documents.extend(custom_docs)
        
        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def create_vector_store(self, documents: List[Document]):
        """Create Qdrant vector store from documents"""
        logger.info("Splitting documents into chunks...")
        texts = self.text_splitter.split_documents(documents)
        logger.info(f"✓ Created {len(texts)} chunks")
        
        # Initialize Qdrant client
        if not self.qdrant_client:
            self.setup_qdrant_client()
        
        logger.info("Creating Qdrant vector store...")
        
        # Create vector store
        self.vectorstore = Qdrant.from_documents(
            documents=texts,
            embedding=self.embeddings,
            url=self.qdrant_url if self.qdrant_url else None,
            api_key=self.qdrant_api_key if self.qdrant_api_key else None,
            collection_name=self.collection_name,
            force_recreate=True,
            path="./qdrant_storage" if not self.qdrant_url else None
        )
        
        logger.info(f"✓ Vector store created in collection: {self.collection_name}")
        
    def load_vector_store(self):
        """Load existing Qdrant vector store"""
        if not self.embeddings:
            self.setup_embeddings()
        
        if not self.qdrant_client:
            self.setup_qdrant_client()
            
        logger.info(f"Loading Qdrant vector store from collection: {self.collection_name}")
        
        try:
            self.vectorstore = Qdrant(
                client=self.qdrant_client,
                collection_name=self.collection_name,
                embeddings=self.embeddings
            )
            logger.info("✓ Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            logger.info("You may need to create a new vector store using create_vector_store()")
            raise
        
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Run create_vector_store() first.")
            
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def get_retriever(self, k: int = 4):
        """Get retriever for the vector store"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized.")
            
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def get_collection_info(self) -> Dict:
        """Get information about the Qdrant collection"""
        if not self.qdrant_client:
            self.setup_qdrant_client()
        
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vectors_count": collection_info.vectors_count,
                "status": collection_info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}


def main():
    """Main execution function"""
    print("=" * 60)
    print("Amit Nagaich RAG Chatbot - Setup with Qdrant & Google Gemini")
    print("=" * 60)
    
    # Get API keys from environment
    google_api_key = os.getenv("GOOGLE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    # Initialize RAG pipeline
    rag = AmitChatbotRAG(
        collection_name="amit_knowledge_base",
        use_google_embeddings=bool(google_api_key),
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )
    
    # Setup Qdrant client
    rag.setup_qdrant_client()
    
    # Setup embeddings
    print("\n" + "=" * 60)
    print("Setting up embeddings...")
    print("=" * 60)
    rag.setup_embeddings(google_api_key=google_api_key)
    
    # Prepare documents
    print("\n" + "=" * 60)
    print("Preparing knowledge base...")
    print("=" * 60)
    
    # Check for additional data files
    additional_files = []
    if os.path.exists('linkedin_data.txt'):
        additional_files.append('linkedin_data.txt')
    if os.path.exists('github_projects.txt'):
        additional_files.append('github_projects.txt')
    
    documents = rag.prepare_documents(additional_files=additional_files if additional_files else None)
    
    # Create vector store
    print("\n" + "=" * 60)
    print("Creating Qdrant vector database...")
    print("=" * 60)
    rag.create_vector_store(documents)
    
    # Get collection info
    info = rag.get_collection_info()
    if info:
        print(f"\nCollection Info:")
        print(f"  - Vectors count: {info.get('vectors_count', 'N/A')}")
        print(f"  - Status: {info.get('status', 'N/A')}")
    
    # Test the retrieval
    print("\n" + "=" * 60)
    print("Testing retrieval system...")
    print("=" * 60)
    
    test_queries = [
        "What is Amit's experience in machine learning?",
        "Tell me about Amit's projects",
        "What are Amit's technical skills?",
        "Where does Amit work currently?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = rag.similarity_search(query, k=2)
        print(f"Found {len(results)} relevant chunks")
        if results:
            print(f"Top result preview: {results[0].page_content[:200]}...")
    
    print("\n" + "=" * 60)
    print("✓ RAG Pipeline Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'streamlit run streamlit_app.py' to start the chatbot interface")
    print("2. Or use the API by running 'uvicorn api_server:app --reload'")
    print("\nQdrant storage location: ./qdrant_storage")


if __name__ == "__main__":
    main()
