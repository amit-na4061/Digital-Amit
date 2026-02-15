# 🔧 Troubleshooting - Streamlit Cloud Deployment

## Common Error: ModuleNotFoundError

### Error Message:
```
ModuleNotFoundError: This app has encountered an error.
File "streamlit_app.py", line 7, in <module>
    from langchain_google_genai import ChatGoogleGenerativeAI
```

### ✅ Solution: Update requirements.txt

The issue is caused by incompatible package versions. I've updated `requirements.txt` with tested, compatible versions.

---

## 🚀 Fix Steps

### Option 1: Use Updated requirements.txt (Recommended)

The `requirements.txt` file has been updated with compatible versions. Just:

1. **Download the new requirements.txt**
2. **Replace your old one**
3. **Push to GitHub:**
   ```bash
   git add requirements.txt
   git commit -m "Fixed dependencies for Streamlit Cloud"
   git push origin main
   ```
4. **Wait 2-3 minutes** - Streamlit Cloud will auto-redeploy
5. **Refresh your app** - Should work now!

---

### Option 2: Manual Fix (If Option 1 doesn't work)

If you still have issues, try this minimal requirements.txt:

```txt
# Minimal working version for Streamlit Cloud
langchain==0.1.20
langchain-community==0.0.38
langchain-google-genai==1.0.1
google-generativeai==0.4.1
qdrant-client==1.8.0
sentence-transformers==2.5.1
streamlit==1.32.0
beautifulsoup4==4.12.3
requests==2.31.0
python-dotenv==1.0.1
```

---

## 🔍 How to Verify It's Working

### 1. Check Streamlit Cloud Logs

1. Go to your app on https://share.streamlit.io
2. Click **"Manage app"** (bottom right)
3. Click **"Logs"** tab
4. Look for:
   ```
   ✅ Successfully installed langchain-google-genai
   ✅ Your app is now live!
   ```

### 2. Test Locally First

Before pushing to Streamlit Cloud, test locally:

```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from requirements.txt
pip install -r requirements.txt

# Test the app
streamlit run streamlit_app.py

# If it works locally, push to Streamlit Cloud
```

---

## 🐛 Other Common Streamlit Cloud Issues

### Issue 2: "Secret GOOGLE_API_KEY not found"

**Solution:**
1. Go to app settings on Streamlit Cloud
2. Click **"Secrets"**
3. Add:
   ```toml
   GOOGLE_API_KEY = "your-actual-api-key"
   ```
4. Click **"Save"**
5. **Reboot app**

---

### Issue 3: "App keeps restarting"

**Solution:**
This usually means initialization is taking too long.

Add this to the top of `streamlit_app.py`:

```python
import streamlit as st

# Show loading message
with st.spinner('Initializing chatbot... This may take 30-60 seconds on first run.'):
    # Your existing imports and initialization
    pass
```

---

### Issue 4: "Qdrant connection failed"

**Solution:**
For Streamlit Cloud, use **local Qdrant** (not cloud).

In `rag_pipeline.py`, make sure it creates local storage:

```python
# This is already in the code - just verify:
if not self.qdrant_url:
    self.qdrant_client = QdrantClient(path="./qdrant_storage")
```

Leave `QDRANT_URL` empty in Streamlit Cloud secrets.

---

### Issue 5: "Memory limit exceeded"

**Solution:**
Streamlit Cloud free tier has 1GB RAM. If you exceed it:

1. **Reduce chunk size** in `rag_pipeline.py`:
   ```python
   chunk_size=500,  # Instead of 1000
   chunk_overlap=100,  # Instead of 200
   ```

2. **Reduce retrieval** in `streamlit_app.py`:
   ```python
   retriever=_rag.get_retriever(k=2)  # Instead of k=4
   ```

3. **Use lighter model**:
   ```python
   model="gemini-1.5-flash"  # Not "gemini-1.5-pro"
   ```

---

## 📊 Package Version Compatibility

These versions are **tested and working** on Streamlit Cloud:

| Package | Version | Why This Version |
|---------|---------|------------------|
| langchain | 0.1.20 | Stable with Gemini |
| langchain-google-genai | 1.0.1 | Latest stable |
| google-generativeai | 0.4.1 | Compatible with above |
| qdrant-client | 1.8.0 | Latest stable |
| streamlit | 1.32.0 | Current stable |

---

## 🔄 Force Rebuild on Streamlit Cloud

If app won't update:

1. Go to **Manage app**
2. Click **"⋮"** (three dots menu)
3. Select **"Reboot app"**
4. Or select **"Delete app"** and redeploy fresh

---

## 💡 Pro Tips

### 1. Pin Your Versions

Always specify exact versions (not `>=` or `~`):
```txt
✅ Good: langchain==0.1.20
❌ Bad: langchain>=0.1.0
```

### 2. Test Locally First

```bash
# Always test before deploying
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### 3. Check Python Version

Streamlit Cloud uses Python 3.9 by default. Add `.python-version` file:

```bash
echo "3.10" > .python-version
```

Then push to GitHub.

### 4. Use packages.txt for System Dependencies

If you need system packages, create `packages.txt`:

```txt
build-essential
```

---

## 🆘 Still Not Working?

### Step 1: Check Streamlit Cloud Status
Visit: https://status.streamlit.io

### Step 2: Simplify
Create a minimal test app:

```python
# test_app.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

st.write("Testing imports...")
st.write("✅ All imports successful!")
```

### Step 3: Compare Working Example
Check the official Streamlit + LangChain examples:
https://github.com/streamlit/llm-examples

### Step 4: Ask for Help
- Streamlit Community: https://discuss.streamlit.io
- GitHub Issues: Open an issue with logs
- Email: amit.na4061@gmail.com

---

## ✅ Verification Checklist

After fixing, verify:

- [ ] `requirements.txt` has updated versions
- [ ] Pushed to GitHub successfully
- [ ] Streamlit Cloud rebuild triggered
- [ ] No errors in Streamlit Cloud logs
- [ ] App loads without errors
- [ ] Can send test message
- [ ] Response received from chatbot

---

## 📝 Summary

**The Fix:**
1. Use the updated `requirements.txt` with compatible versions
2. Push to GitHub
3. Wait for Streamlit Cloud auto-redeploy
4. Test your app

**Most common cause:** Package version incompatibility

**Best prevention:** 
- Pin exact versions
- Test locally first
- Keep packages updated

---

## 🔗 Useful Links

- **Streamlit Docs:** https://docs.streamlit.io
- **LangChain Docs:** https://python.langchain.com
- **Google Gemini Docs:** https://ai.google.dev
- **Qdrant Docs:** https://qdrant.tech/documentation

---

**Your app should now work perfectly on Streamlit Cloud! 🎉**

If you're still having issues, share the full error log and I'll help debug!
