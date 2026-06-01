# DRAI Dashboard - Full-Stack Web Application Setup Guide

## 🎯 Overview

This is a complete Full-Stack web application for uploading and processing DOCX/ZIP files with an interactive dashboard. The application consists of:

- **Backend**: Flask API (Python) running on Render
- **Frontend**: React Single-Page Application running on Vercel
- **Processing**: Extracts data from DOCX files and generates analytics

---

## 📋 Prerequisites

Before you start, you'll need:

1. **Git** installed on your computer
2. **Python 3.9+** (for local testing)
3. **Node.js 18+** (optional, for local testing)
4. GitHub account (for deploying to Render and Vercel)
5. Render account (free tier): https://render.com
6. Vercel account (free tier): https://vercel.com

---

## 🚀 Quick Start (Local Testing)

### Step 1: Prepare Files

Create a project folder on your computer:

```bash
mkdir drai-dashboard
cd drai-dashboard
```

Copy these files to your project folder:
- `backend-app.py`
- `backend-requirements.txt`
- `frontend-app.html`
- `Procfile`
- `.env.example`

### Step 2: Set Up Backend

```bash
# Create a Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r backend-requirements.txt

# Run the backend server
python backend-app.py
```

The backend will be available at: `http://localhost:5000`

### Step 3: Serve Frontend

Open a new terminal and:

```bash
# Navigate to your project folder
cd drai-dashboard

# Start a simple HTTP server
python3 -m http.server 3000
```

The frontend will be available at: `http://localhost:3000/frontend-app.html`

### Step 4: Test the Application

1. Open your browser to `http://localhost:3000/frontend-app.html`
2. Drag and drop a DOCX or ZIP file
3. Click "Procesar Archivos"
4. View the results in the dashboard

---

## 🌐 Deploy to Cloud (Free Tier)

### Part 1: Deploy Backend to Render

#### 1.1 Push Code to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: DRAI Dashboard Full-Stack Application"

# Create a repository on GitHub.com and follow the instructions to push
git remote add origin https://github.com/YOUR_USERNAME/drai-dashboard.git
git branch -M main
git push -u origin main
```

#### 1.2 Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your GitHub repositories

#### 1.3 Deploy Backend

1. Click "New +" → "Web Service"
2. Select your `drai-dashboard` repository
3. Configure:
   - **Name**: `drai-dashboard-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend-requirements.txt`
   - **Start Command**: `gunicorn backend-app:app`
   - **Plan**: Select "Free"
4. Click "Create Web Service"

Wait for the deployment to complete. Your backend URL will look like:
```
https://drai-dashboard-backend.onrender.com
```

**Save this URL!** You'll need it for the frontend.

### Part 2: Deploy Frontend to Vercel

#### 2.1 Update Frontend API Configuration

Before deploying, you need to update the frontend to use your Render backend URL.

Edit `frontend-app.html` and find this line (around line 305):

```javascript
const API_BASE = process.env.REACT_APP_API || 'http://localhost:5000';
```

Update it to:

```javascript
const API_BASE = 'https://drai-dashboard-backend.onrender.com';
```

Or keep it flexible for environment variables.

#### 2.2 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub

#### 2.3 Deploy Frontend

1. Go to https://vercel.com/new
2. Import your GitHub repository (`drai-dashboard`)
3. Configure:
   - **Framework Preset**: `Other` (static files)
   - **Root Directory**: `.` (root)
   - **Build Command**: Leave empty
   - **Output Directory**: `.`
4. Add Environment Variables:
   - **REACT_APP_API**: `https://drai-dashboard-backend.onrender.com`
5. Click "Deploy"

Wait for deployment to complete. Your frontend URL will look like:
```
https://drai-dashboard.vercel.app
```

Your application is now live! 🎉

---

## 🔧 Configuration

### Environment Variables

After deployment, you may need to update environment variables:

#### Render Backend
1. Go to your Render service dashboard
2. Click "Environment"
3. Add variables:
   - `FLASK_ENV`: `production`
   - `FRONTEND_URL`: Your Vercel frontend URL

#### Vercel Frontend
1. Go to your Vercel project settings
2. Click "Environment Variables"
3. Add/update:
   - `REACT_APP_API`: Your Render backend URL

### CORS Configuration

The backend is configured for CORS. If you get CORS errors:

1. Edit `backend-app.py`
2. Find the line with `CORS(app)`
3. Update it to specify allowed origins:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://drai-dashboard.vercel.app"],
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 📁 File Structure

```
drai-dashboard/
├── backend-app.py              # Flask API server
├── backend-requirements.txt     # Python dependencies
├── frontend-app.html           # React single-page app
├── Procfile                    # Render deployment config
├── vercel.json                 # Vercel deployment config
├── .env.example                # Environment variables template
├── SETUP_GUIDE.md             # This file
└── .gitignore                 # Git ignore file (create this)
```

### Create `.gitignore`

```
venv/
__pycache__/
*.pyc
.DS_Store
.env
*.log
uploads/
```

---

## 🛠️ API Endpoints

### POST /api/upload
Upload DOCX or ZIP files for processing.

**Request**:
```
Content-Type: multipart/form-data
Files: multiple DOCX or ZIP files
```

**Response**:
```json
{
  "success": true,
  "report_id": 1,
  "data": {
    "total_files": 2,
    "total_tables": 5,
    "total_activities": 1500,
    "files_processed": [
      {"name": "file1.docx", "activities": 750},
      {"name": "file2.docx", "activities": 750}
    ]
  }
}
```

### GET /api/health
Check if the API is running.

**Response**:
```json
{"status": "ok", "message": "Backend running"}
```

### GET /api/reports
Get all processed reports.

**Response**:
```json
{
  "reports": [
    {"id": 1, "timestamp": "2026-06-01T12:00:00", "consolidated": {...}}
  ]
}
```

### GET /api/reports/<id>
Get a specific report by ID.

### DELETE /api/reports/<id>
Delete a report.

### GET /api/export/<id>
Export a report as JSON.

---

## 🐛 Troubleshooting

### Issue: CORS Error in Browser Console

**Problem**: "Access to XMLHttpRequest has been blocked by CORS policy"

**Solution**:
1. Check the backend URL in `frontend-app.html`
2. Verify CORS configuration in `backend-app.py`
3. Ensure Render backend is running (`/api/health` returns 200)

### Issue: 502 Bad Gateway on Render

**Problem**: Backend returns 502 error

**Solution**:
1. Check Render logs: Go to your service → "Logs"
2. Verify all dependencies are in `backend-requirements.txt`
3. Check for syntax errors in `backend-app.py`
4. Restart the service: Click "Manual Deploy"

### Issue: Frontend Shows Blank Page

**Problem**: No content displays

**Solution**:
1. Open browser DevTools (F12) and check Console for errors
2. Check Network tab to verify API calls
3. Ensure `API_BASE` URL is correct in `frontend-app.html`
4. Clear browser cache (Ctrl+Shift+Delete)

### Issue: File Upload Fails

**Problem**: "Error al procesar archivos"

**Solution**:
1. Verify file is valid DOCX or ZIP
2. Check file size (should be under 50MB per file)
3. Check backend logs on Render for specific error
4. Verify ZIP files contain valid DOCX files

---

## 📊 Data Processing

### What Gets Extracted

The backend automatically extracts:
- **Tables**: All tables from DOCX files
- **Paragraphs**: All text content
- **Numbers**: Numbers found in document text
- **Totals**: Sum of first 10 numbers per file

### Processing Flow

```
Upload Files
    ↓
Validate Format (DOCX/ZIP)
    ↓
Extract Content (tables, text, numbers)
    ↓
Consolidate Data
    ↓
Generate Report
    ↓
Display Dashboard
```

---

## 🔐 Security Considerations

For production use, consider:

1. **File Size Limits**: Add max file size validation
2. **File Type Validation**: Verify DOCX/ZIP headers
3. **Rate Limiting**: Prevent abuse with rate limiting
4. **Authentication**: Add user login if needed
5. **Database**: Replace in-memory storage with SQLite/PostgreSQL
6. **HTTPS**: Ensure frontend and backend use HTTPS
7. **CORS**: Configure specific allowed origins

---

## 📈 Next Steps & Enhancements

### Recommended Improvements

1. **Database Persistence**
   - Replace in-memory storage with SQLite
   - Store historical reports permanently

2. **Authentication**
   - Add user login functionality
   - Store user-specific reports

3. **Advanced Features**
   - Filter reports by date range
   - Compare multiple reports
   - Export to Excel/PDF
   - Automatic data visualization

4. **Performance**
   - Add caching for large files
   - Implement background processing with Celery
   - Optimize database queries

5. **User Experience**
   - Add progress bar for large files
   - Implement batch processing
   - Add data download options

---

## 📞 Support & Updates

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs on Render
3. Check frontend console (DevTools → Console)
4. Verify your API endpoint URLs

---

## 📝 Version History

- **v1.0** (2026-06-01): Initial release with full-stack application
  - React frontend with drag-and-drop
  - Flask backend with file processing
  - Cloud deployment on Render + Vercel
  - DOCX and ZIP file support
  - Interactive dashboard with KPI cards

---

## License

Created for DRAI Organization - 2026

