# Amit Nagaich - RAG Chatbot (Minimal Setup)

A personalized RAG chatbot powered by **Qdrant** and **Google Gemini**, representing Amit Nagaich's professional profile.

## 🎯 What You Get

- ✅ **Qdrant Vector Database** - Local or cloud vector search
- ✅ **Google Gemini AI** - Free tier available (60 req/min)
- ✅ **Streamlit Interface** - Beautiful chat UI
- ✅ **REST API** - FastAPI backend with auto-docs
- ✅ **Docker Ready** - One command to run everything
- ✅ **GitHub Actions CI/CD** - Automated testing

## 📋 Prerequisites

**Required:**
- Python 3.10+
- Docker Desktop
- Google API Key ([Get it FREE here](https://makersuite.google.com/app/apikey))

**That's it!**

## 🚀 Quick Start (3 Steps)

### 1. Get Google API Key

Visit https://makersuite.google.com/app/apikey and:
- Sign in with your Google account
- Click "Create API Key"
- Copy the key

**Note:** Free tier includes 60 requests per minute - perfect for personal use!

### 2. Setup Environment

```bash
# Clone or download this repository
cd amit-chatbot

# Create .env file
cp .env.template .env

# Edit .env and add your key:
# GOOGLE_API_KEY=your-api-key-here
```

### 3. Run with Docker

```bash
# Start all services
docker-compose up -d

# Initialize the knowledge base (first time only)
docker-compose exec api python rag_pipeline.py

# That's it! 🎉
```

### Access Your Chatbot

- **Streamlit UI:** http://localhost:8501
- **REST API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Qdrant Dashboard:** http://localhost:6333/dashboard

## 💻 Alternative: Run Without Docker

If you prefer Python virtual environment:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Google API key
echo "GOOGLE_API_KEY=your-key-here" > .env

# Initialize knowledge base
python rag_pipeline.py

# Run Streamlit (in one terminal)
streamlit run streamlit_app.py

# Run API (in another terminal)
uvicorn api_server:app --reload
```

## 🌐 Deploy to Streamlit Cloud (FREE)

Want to share your chatbot? Deploy it for free!

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/amit-chatbot.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `amit-chatbot`
5. Main file path: `streamlit_app.py`
6. Click "Advanced settings" → "Secrets"
7. Add:
   ```toml
   GOOGLE_API_KEY = "your-api-key-here"
   ```
8. Click "Deploy"

**Your chatbot will be live at:** `https://your-app.streamlit.app`

## 📁 Project Structure

```
amit-chatbot/
├── rag_pipeline.py          # Core RAG implementation
├── streamlit_app.py         # Chat interface
├── api_server.py            # REST API
├── requirements.txt         # Dependencies
├── Dockerfile               # Container config
├── docker-compose.yml       # Multi-service setup
├── .env.template            # Environment template
└── .github/workflows/
    └── ci-cd.yml            # GitHub Actions
```

## 🔧 Configuration

### Environment Variables

Only one required:

```bash
GOOGLE_API_KEY=your-google-api-key
```

### Optional (Qdrant Cloud)

Want to use Qdrant Cloud instead of local?

1. Create account at https://cloud.qdrant.io (FREE tier: 1GB)
2. Create a cluster
3. Add to `.env`:
   ```bash
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-key
   ```

## 🎨 Customization

### Add Your Own Content

Create a text file with your information:

```bash
# linkedin_data.txt
My recent project on NLP achieved 95% accuracy...
I presented at the ML conference on...
```

Then update `rag_pipeline.py`:

```python
documents = rag.prepare_documents(
    additional_files=['linkedin_data.txt']
)
```

### Modify Personality

Edit the `SYSTEM_PROMPT` in `streamlit_app.py` or `api_server.py`:

```python
SYSTEM_PROMPT = """You are Amit Nagaich...

COMMUNICATION STYLE:
- Be more technical/casual/formal
- Focus on specific topics
- Add your preferences here
"""
```

### Change Models

In your code, you can switch models:

```python
# For better quality (slower, more expensive)
model="gemini-1.5-pro"

# For faster responses (default)
model="gemini-1.5-flash"
```

## 🧪 Testing

### Manual Testing

```bash
# Test API health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your ML skills?"}'
```

### Run Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

## 🔄 GitHub Actions CI/CD

The project includes automated testing on every push.

### Setup GitHub Actions

1. Push your code to GitHub
2. Go to Settings → Secrets and variables → Actions
3. Add secret:
   - Name: `GOOGLE_API_KEY`
   - Value: Your Google API key

The pipeline will automatically:
- ✅ Run tests on every push
- ✅ Check code quality
- ✅ Validate your changes

## 🐛 Troubleshooting

### "Google API key not found"
**Solution:** Make sure `.env` file exists with `GOOGLE_API_KEY=your-key`

### "Docker containers not starting"
**Solution:** 
```bash
# Check Docker is running
docker ps

# Restart services
docker-compose down
docker-compose up -d
```

### "Vector store not initialized"
**Solution:** Run the initialization:
```bash
docker-compose exec api python rag_pipeline.py
```

### "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### "Port already in use"
**Solution:** Stop other services or change ports in `docker-compose.yml`:
```yaml
ports:
  - "8502:8501"  # Change 8501 to 8502
```

## 💰 Cost Breakdown

**100% FREE Setup:**
- Google Gemini API: FREE (60 req/min)
- Qdrant: FREE (local) or FREE tier (cloud)
- Streamlit Cloud: FREE hosting
- GitHub Actions: FREE (2000 min/month)

**Total: $0/month** 🎉

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/profile` | GET | Get Amit's profile |
| `/chat` | POST | Chat with bot |
| `/search` | GET | Search knowledge base |

Visit http://localhost:8000/docs for interactive API documentation.

## 🎓 How It Works

```
Your Query
    ↓
Vector Embedding (Google)
    ↓
Search Similar Documents (Qdrant)
    ↓
Retrieve Top 4 Matches
    ↓
Build Context + Query
    ↓
Send to Google Gemini
    ↓
Get Response
    ↓
Display to User
```

## 📚 Tech Stack

- **Vector DB:** Qdrant (fast, scalable)
- **LLM:** Google Gemini 1.5 (state-of-the-art)
- **Framework:** LangChain (industry standard)
- **UI:** Streamlit (rapid development)
- **API:** FastAPI (high performance)
- **Containers:** Docker (portability)

## 🔐 Security

- ✅ API keys in `.env` (never commit!)
- ✅ Input validation (Pydantic models)
- ✅ CORS configured
- ✅ Rate limiting built-in
- ✅ `.gitignore` protects secrets

## 📈 Performance

**Expected:**
- Query response: 2-4 seconds
- Vector search: <100ms
- Supports 10+ concurrent users
- Handles 1000+ documents

## 🎯 Next Steps

### Immediate
- [x] Get Google API key
- [ ] Run locally with Docker
- [ ] Test the chatbot

### This Week
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Share with friends!

### This Month
- [ ] Add more personal content
- [ ] Customize personality
- [ ] Embed in your portfolio

## 🆘 Need Help?

- **Issues:** Check the Troubleshooting section above
- **Questions:** Open a GitHub issue
- **Email:** amit.na4061@gmail.com

## 📝 License

MIT License - feel free to use for your own portfolio!

## 🤝 Contributing

Want to improve this? PRs welcome!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

**Amit Nagaich**
- 📧 Email: amit.na4061@gmail.com
- 💼 LinkedIn: [amit-nagaich-22283645](https://www.linkedin.com/in/amit-nagaich-22283645/)
- 🐙 GitHub: [amit-na4061](https://github.com/amit-na4061)
- 🌐 Portfolio: [amit-na4061.github.io](https://amit-na4061.github.io/)

---

**Built with ❤️ using Qdrant, Google Gemini, LangChain & Streamlit**

⭐ Star this repo if you find it helpful!

---

## Quick Commands Reference

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f api

# Restart
docker-compose restart

# Initialize knowledge base
docker-compose exec api python rag_pipeline.py

# Run tests
pytest tests/ -v
```

**Ready to build your AI chatbot? Start with Step 1! 🚀**
