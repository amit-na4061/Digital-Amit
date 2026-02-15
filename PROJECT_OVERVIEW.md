# 📦 Project Overview

## What This Is

A **personal AI chatbot** that represents you (Amit Nagaich) using:
- Your portfolio content
- Your projects and experience
- RAG (Retrieval-Augmented Generation) technology
- Google's free Gemini API

## What You Can Do

1. **Run Locally** - Test on your computer
2. **Deploy Free** - Share on Streamlit Cloud
3. **Customize** - Add your own content
4. **Integrate** - Embed in your portfolio

## Requirements

**Absolutely Required:**
- Google API Key (FREE - get at https://makersuite.google.com/app/apikey)
- Docker Desktop OR Python 3.10+

**That's all!**

## File Overview

### Core Files (Don't Delete!)
- `rag_pipeline.py` - Loads your data and creates vector database
- `streamlit_app.py` - Chat interface
- `api_server.py` - REST API
- `requirements.txt` - Python packages
- `docker-compose.yml` - Runs everything together

### Configuration
- `.env.template` - Copy this to `.env` and add your API key
- `.gitignore` - Protects your secrets

### Optional
- `.github/workflows/ci-cd.yml` - Automated testing
- `tests/` - Unit tests
- `Dockerfile` - For containerization

## Quick Start

```bash
# 1. Get API key from Google
# 2. Create .env file
cp .env.template .env
# Add your GOOGLE_API_KEY

# 3. Run
docker-compose up -d
docker-compose exec api python rag_pipeline.py

# 4. Open browser
# http://localhost:8501
```

## How It Works

```
Your Question
    ↓
Converts to vector (embedding)
    ↓
Searches your knowledge base (Qdrant)
    ↓
Finds relevant information
    ↓
Sends to Google Gemini
    ↓
Gets intelligent response
    ↓
Shows you the answer
```

## What's Included

✅ **Local Qdrant** - Vector database (no cloud needed)
✅ **Google Gemini** - AI language model (60 req/min free)
✅ **Streamlit UI** - Beautiful chat interface
✅ **REST API** - For programmatic access
✅ **Docker Setup** - One command to run
✅ **GitHub Actions** - Automated testing
✅ **Full Documentation** - README, guides, examples

## Cost

**$0/month** - Everything can run for free!

- Google Gemini: FREE tier (60 requests/min)
- Qdrant: FREE (runs locally on your computer)
- Streamlit Cloud: FREE hosting
- GitHub Actions: FREE (2000 minutes/month)

## Deployment Options

1. **Local** (Your computer)
   - Cost: $0
   - Setup: 5 minutes
   - Use: Testing and development

2. **Streamlit Cloud** (Internet)
   - Cost: $0
   - Setup: 10 minutes
   - Use: Share with others
   - URL: `https://your-app.streamlit.app`

3. **Your Portfolio** (Embedded)
   - Cost: $0
   - Setup: 15 minutes
   - Use: Professional showcase

## Customization

### Add Your Content
Create `my_data.txt` with your information:
```
I recently completed a project on...
My experience includes...
I'm skilled in...
```

Then in `rag_pipeline.py`:
```python
documents = rag.prepare_documents(
    additional_files=['my_data.txt']
)
```

### Change Personality
Edit `SYSTEM_PROMPT` in `streamlit_app.py`:
```python
SYSTEM_PROMPT = """
You are Amit Nagaich...
[Customize the personality here]
"""
```

### Adjust Models
In the code:
```python
# Faster (default)
model="gemini-1.5-flash"

# Smarter (slower)
model="gemini-1.5-pro"
```

## Architecture

```
┌─────────────────┐
│   Streamlit UI  │
│   (Port 8501)   │
└────────┬────────┘
         │
┌────────▼────────┐
│   FastAPI       │
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│Qdrant │ │ Google  │
│Vector │ │ Gemini  │
│  DB   │ │   API   │
└───────┘ └─────────┘
```

## File Structure

```
amit-chatbot/
├── rag_pipeline.py        # Core RAG logic
├── streamlit_app.py       # Chat UI
├── api_server.py          # REST API
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Run everything
├── .env.template          # Config template
├── README.md              # Full docs
├── QUICKSTART.md          # 5-min guide
└── .github/workflows/
    └── ci-cd.yml          # Auto testing
```

## Next Steps

1. **Today:** Run it locally
2. **This Week:** Deploy to Streamlit Cloud
3. **This Month:** Customize and add content
4. **Ongoing:** Keep improving!

## Support

- **Full Documentation:** `README.md`
- **Quick Start:** `QUICKSTART.md`
- **Issues:** GitHub Issues
- **Email:** amit.na4061@gmail.com

## License

MIT - Use freely for your own projects!

---

**Ready to start?** Open `QUICKSTART.md` for 5-minute setup guide! 🚀
