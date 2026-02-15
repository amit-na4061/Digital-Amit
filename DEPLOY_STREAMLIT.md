# 🚀 Deploy to Streamlit Cloud (FREE)

## Why Streamlit Cloud?

- ✅ **100% FREE** - No credit card needed
- ✅ **5-minute setup** - Super easy
- ✅ **Auto-deploy** - Updates from GitHub automatically
- ✅ **Custom URL** - Get your own link
- ✅ **Always online** - 24/7 availability

## Prerequisites

- ✅ GitHub account (free)
- ✅ Streamlit Cloud account (free - sign up with GitHub)
- ✅ Your code pushed to GitHub
- ✅ Google API Key

## Step-by-Step Deployment

### Step 1: Push to GitHub (5 minutes)

If you haven't already:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: RAG chatbot"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/amit-na4061/amit-chatbot.git
git branch -M main
git push -u origin main
```

---

### Step 2: Sign Up for Streamlit Cloud (1 minute)

1. Go to https://share.streamlit.io
2. Click **"Sign up"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit

That's it!

---

### Step 3: Deploy Your App (3 minutes)

1. **Click "New app"** button

2. **Fill in the details:**
   - Repository: `YOUR_USERNAME/amit-chatbot`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Click "Advanced settings"**

4. **Add Secrets** (Important!):
   ```toml
   # Copy-paste this into the secrets box:
   GOOGLE_API_KEY = "your-actual-api-key-here"
   ```
   
   Optional (if using Qdrant Cloud):
   ```toml
   GOOGLE_API_KEY = "your-api-key"
   QDRANT_URL = "https://your-cluster.qdrant.io"
   QDRANT_API_KEY = "your-qdrant-key"
   ```

5. **Click "Deploy"**

6. **Wait 2-3 minutes** while it builds

7. **Done!** Your app is live! 🎉

---

### Step 4: Access Your App

Your chatbot will be available at:
```
https://amit-chatbot-yourusername.streamlit.app
```

Or your custom name:
```
https://your-custom-name.streamlit.app
```

---

## Post-Deployment

### Test Your App

1. Open the URL
2. Try asking questions:
   - "What is your ML experience?"
   - "Tell me about your projects"
   - "What technologies do you use?"

### Share Your App

Share your URL with:
- Potential employers
- Colleagues
- Friends
- On LinkedIn
- On your resume

### Update Your App

Every time you push to GitHub, Streamlit automatically redeploys!

```bash
# Make changes to your code
git add .
git commit -m "Updated chatbot personality"
git push origin main

# Streamlit Cloud automatically redeploys (2-3 minutes)
```

---

## Customization

### Change App Name

1. Go to https://share.streamlit.io
2. Click on your app
3. Click **Settings** → **General**
4. Change the URL slug
5. Save

### Add a Custom Domain (Optional)

Streamlit Cloud allows custom domains on paid plans, but the free `.streamlit.app` domain works great!

---

## Monitoring

### View Logs

1. Go to your app on share.streamlit.io
2. Click **"Manage app"**
3. View logs in real-time

### Check Status

1. Your app automatically sleeps after inactivity
2. First visit after sleep takes ~30 seconds to wake
3. Subsequent visits are instant

### Resource Limits (Free Tier)

- **Memory:** 1 GB
- **CPU:** Shared
- **Bandwidth:** Unlimited
- **Apps:** Up to 3 apps

This is perfect for personal projects!

---

## Troubleshooting

### App Won't Start

**Check:**
1. Is `streamlit_app.py` in the root directory?
2. Are secrets configured correctly?
3. Check the logs for errors

**Common fixes:**
```bash
# Make sure requirements.txt is complete
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Updated dependencies"
git push
```

### "API Key Not Found"

**Solution:**
1. Go to app settings
2. Click **Secrets**
3. Verify `GOOGLE_API_KEY` is set
4. Reboot app

### "Vector Store Error"

**Solution:**
The app needs to initialize the knowledge base on first run.

Add this to your `streamlit_app.py` (already included):
```python
if os.path.exists("./qdrant_storage"):
    rag.load_vector_store()
else:
    # Auto-initialize on first run
    documents = rag.prepare_documents()
    rag.create_vector_store(documents)
```

### Slow Response Times

**Solutions:**
1. Use `gemini-1.5-flash` (faster than pro)
2. Reduce retrieval chunks (k=2 instead of k=4)
3. Consider upgrading to Streamlit paid tier

---

## GitHub Actions Integration

Your app automatically redeploys when GitHub Actions succeeds.

The workflow in `.github/workflows/ci-cd.yml`:
1. Runs tests
2. Checks code quality
3. If successful, Streamlit auto-deploys

---

## Embed in Your Portfolio

Want to embed in your website?

```html
<iframe 
  src="https://amit-chatbot-yourusername.streamlit.app/?embed=true" 
  width="100%" 
  height="800px" 
  frameborder="0">
</iframe>
```

Add `?embed=true` to hide Streamlit branding.

---

## Upgrading (Optional)

If your app becomes popular:

**Streamlit Cloud Pro** ($20/month):
- More resources
- Custom domain
- No sleep mode
- Priority support

But the **free tier is perfect** for personal projects!

---

## Alternative: Use the API Only

Don't want to deploy the Streamlit UI? Deploy just the API:

**Option 1: Google Cloud Run**
```bash
gcloud run deploy amit-chatbot-api \
  --source . \
  --region us-central1
```

**Option 2: Railway** (similar to Heroku, easier)
1. Go to https://railway.app
2. Connect GitHub
3. Deploy!

---

## Best Practices

### 1. Keep Secrets Secure
- ✅ Never commit `.env` to GitHub
- ✅ Use Streamlit Cloud secrets
- ✅ Rotate API keys periodically

### 2. Monitor Usage
- Check Google API usage in console
- Monitor Streamlit app logs
- Set up budget alerts (optional)

### 3. Optimize Performance
- Cache embeddings
- Use faster models
- Minimize API calls

### 4. Regular Updates
- Update dependencies monthly
- Add new content regularly
- Improve based on feedback

---

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed successfully
- [ ] Secrets configured (GOOGLE_API_KEY)
- [ ] App tested and working
- [ ] URL shared with others
- [ ] GitHub Actions passing

---

## What's Next?

1. **Customize** - Add your content, adjust personality
2. **Share** - Post on LinkedIn, add to resume
3. **Monitor** - Check logs, gather feedback
4. **Improve** - Iterate based on usage

---

## Need Help?

- **Streamlit Docs:** https://docs.streamlit.io/
- **Community Forum:** https://discuss.streamlit.io/
- **This Project:** Check README.md

---

**Your chatbot is now live! Share it with the world! 🌍**

Example URL: https://amit-chatbot-demo.streamlit.app
