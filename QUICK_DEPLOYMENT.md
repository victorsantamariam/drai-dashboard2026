# 🚀 DRAI Dashboard - Quick Deployment Guide

## 5-Minute Cloud Deployment (Render + Vercel)

### Prerequisites
- GitHub account
- Render account (render.com)
- Vercel account (vercel.com)

---

## PASO 1: Preparar GitHub Repository (5 min)

```bash
# Navigate to your project folder
cd drai-dashboard

# Initialize git
git init
git add .
git commit -m "DRAI Dashboard Full-Stack App"

# Create repository on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/drai-dashboard.git
git branch -M main
git push -u origin main
```

---

## PASO 2: Deploy Backend to Render (3 min)

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository (`drai-dashboard`)
4. Fill in:
   - **Name**: `drai-dashboard-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend-requirements.txt`
   - **Start Command**: `gunicorn backend-app:app`
   - **Plan**: `Free`
5. Click **"Create Web Service"**
6. ⏳ Wait 2-3 minutes for deployment
7. Copy your backend URL (looks like `https://drai-dashboard-backend.onrender.com`)

**Save this URL!** ⭐

---

## PASO 3: Deploy Frontend to Vercel (3 min)

### Step 3a: Update Backend URL

Edit `frontend-app.html` line ~305:

Change:
```javascript
const API_BASE = process.env.REACT_APP_API || 'http://localhost:5000';
```

To:
```javascript
const API_BASE = 'https://drai-dashboard-backend.onrender.com';
```

Commit and push:
```bash
git add frontend-app.html
git commit -m "Update API URL for Render backend"
git push
```

### Step 3b: Deploy on Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Click **"Deploy"** (default settings are fine)
4. ⏳ Wait 1-2 minutes
5. Copy your Vercel URL (looks like `https://drai-dashboard.vercel.app`)

---

## ✅ DONE! Your app is live!

| Component | URL |
|-----------|-----|
| 🎨 Frontend | https://drai-dashboard.vercel.app |
| 📡 Backend | https://drai-dashboard-backend.onrender.com |
| API Health | https://drai-dashboard-backend.onrender.com/api/health |

---

## 🧪 Test It

1. Open: https://drai-dashboard.vercel.app
2. Upload a DOCX or ZIP file
3. Click "Procesar Archivos"
4. View your dashboard! 📊

---

## ⚠️ Troubleshooting

### CORS Error?
The backend has CORS enabled. If still getting errors:
1. Check backend URL in `frontend-app.html`
2. Verify `/api/health` returns 200
3. Wait 5 minutes (Render cold starts)

### 502 Error on Render?
1. Go to Render dashboard
2. Check "Logs" tab
3. Look for Python errors
4. Click "Manual Deploy" to restart

### Blank Page on Vercel?
1. Open DevTools (F12)
2. Check Console for errors
3. Check Network tab for API calls
4. Clear cache (Ctrl+Shift+Delete)

---

## 📌 Important URLs

```
Frontend:          https://drai-dashboard.vercel.app
Backend:           https://drai-dashboard-backend.onrender.com
API Upload:        https://drai-dashboard-backend.onrender.com/api/upload
API Health Check:  https://drai-dashboard-backend.onrender.com/api/health
```

---

## 🔄 Making Changes

After you make changes locally:

```bash
git add .
git commit -m "Your changes"
git push
```

Both Render and Vercel will automatically redeploy! 🚀

---

## 💡 Pro Tips

- **Cold Starts**: Free tier Render services sleep after 15 min inactivity. First request takes 30 sec.
- **File Size**: Keep files under 50MB
- **Rate Limiting**: Add rate limiting for production use
- **Database**: Consider upgrading to PostgreSQL when you need persistent storage

---

**Questions?** Check `SETUP_GUIDE.md` for detailed instructions and troubleshooting.
