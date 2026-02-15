# ⚡ Quick Start Guide

## 🎯 Get Running in 5 Minutes

### Step 1: Get Google API Key (2 minutes)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

**Note:** It's FREE! 60 requests per minute.

---

### Step 2: Setup (1 minute)

```bash
# Clone/download the project
cd amit-chatbot

# Create .env file
cp .env.template .env

# Open .env and paste your API key:
# GOOGLE_API_KEY=AIza...your-key-here
```

---

### Step 3: Run (2 minutes)

#### Option A: Docker (Recommended)

```bash
# Start everything
docker-compose up -d

# Initialize knowledge base (first time only)
docker-compose exec api python rag_pipeline.py

# Done! Open your browser:
# http://localhost:8501
```

#### Option B: Python

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize
python rag_pipeline.py

# Run (in separate terminals)
streamlit run streamlit_app.py
uvicorn api_server:app --reload
```

---

## ✅ That's It!

Your chatbot is now running at:
- **Chat UI:** http://localhost:8501
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🎮 Try These Questions

- "What is your experience in machine learning?"
- "Tell me about your projects"
- "What technologies do you work with?"
- "What's your background in healthcare analytics?"

---

## 🌐 Deploy to Internet (FREE)

Want to share your chatbot? Deploy to Streamlit Cloud:

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "My RAG chatbot"
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Connect your repo
# 4. Add your GOOGLE_API_KEY in secrets
# 5. Deploy!
```

Your chatbot will be live at: `https://your-app.streamlit.app`

---

## 🛠️ Common Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f api

# Restart
docker-compose restart

# Rebuild (after code changes)
docker-compose up -d --build
```

---

## 🐛 Troubleshooting

**"API key not found"**
→ Check `.env` file has `GOOGLE_API_KEY=your-key`

**"Docker not starting"**
→ Make sure Docker Desktop is running

**"Port already in use"**
→ Stop other services or change ports in `docker-compose.yml`

**"Vector store error"**
→ Run: `docker-compose exec api python rag_pipeline.py`

---

## 📚 What Next?

- ✅ Add your own content (LinkedIn, projects)
- ✅ Customize the personality
- ✅ Deploy to Streamlit Cloud
- ✅ Embed in your portfolio website

See `README.md` for full documentation.

---

## 💡 Tips

1. **Test locally first** before deploying
2. **Save your API key safely** - never commit it
3. **Start simple** - add features gradually
4. **Use Streamlit Cloud** - easiest deployment

---

**Questions?** Check README.md or open an issue!

**Ready? Let's go! 🚀**

```bash
docker-compose up -d
```
