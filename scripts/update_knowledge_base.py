import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Load environment variables
load_dotenv()

def load_documents_from_directory(directory_path):
    """Load all text files from a directory."""
    documents = []
    data_dir = Path(directory_path)
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    # Supported file extensions
    extensions = ['.txt', '.md', '.html', '.json']
    
    for file_path in data_dir.rglob('*'):
        if file_path.suffix.lower() in extensions and file_path.is_file():
            print(f"Loading: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        documents.append(Document(
                            page_content=content,
                            metadata={
                                "source": str(file_path),
                                "filename": file_path.name
                            }
                        ))
            except Exception as e:
                print(f"⚠️  Error loading {file_path}: {e}")
    
    return documents

def create_or_update_vector_db():
    """Main function to create/update vector database."""
    try:
        # 1. Validate environment variables
        required_vars = ["GOOGLE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
        
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "amit_portfolio")
        
        print("=" * 60)
        print("🚀 Starting Vector Database Update")
        print("=" * 60)
        
        # 2. Initialize embeddings
        print("\n📦 Initializing embeddings model...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # 3. Load documents
        print("\n📁 Loading documents from data directory...")
        data_directory = Path(__file__).parent.parent / "data"
        documents = load_documents_from_directory(data_directory)
        
        if not documents:
            raise ValueError("No documents found to process")
        
        print(f"✅ Loaded {len(documents)} documents")
        
        # 4. Split documents into chunks
        print("\n✂️  Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        # 5. Upload to Qdrant
        print(f"\n☁️  Uploading to Qdrant (Collection: {collection_name})...")
        vector_store = Qdrant.from_documents(
            chunks,
            embeddings,
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=collection_name,
            force_recreate=True
        )
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Vector database updated")
        print("=" * 60)
        print(f"📊 Statistics:")
        print(f"   - Documents processed: {len(documents)}")
        print(f"   - Total chunks: {len(chunks)}")
        print(f"   - Collection: {collection_name}")
        print(f"   - URL: {os.getenv('QDRANT_URL')}")
        print("=" * 60)
        
        return vector_store
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERROR: {type(e).__name__}")
        print("=" * 60)
        print(f"{e}")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    create_or_update_vector_db()
