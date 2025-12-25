# MaleCare Clinical Trials Chatbot

AI-powered chatbot that helps cancer patients find relevant clinical trials.

---

## 🚀 For Darryl: WordPress Deployment & Usage

### Adding the Chatbot to WordPress

Add the chatbot to your WordPress site:

1. **Go to WordPress**:
   - Open your WordPress page editor
   - Switch to "Text" or "HTML" mode

2. **Add This Code** where you want the chatbot:
   ```html
   <iframe 
     src="https://malecarechatbot.vercel.app" 
     width="100%" 
     height="800px" 
     frameborder="0"
     title="Clinical Trials Chatbot">
   </iframe>
   ```

3. **Adjust Size** (optional):
   - Change `height="800px"` to make it taller/shorter
   - Change `width="100%"` to a specific width like `"800px"`

### Accessing Usage Statistics (in development)

After deploying these updates (see deployment steps below):
- Visit https://malecarechatbot.vercel.app/admin to:
- View usage dashboard
- Download CSV reports
- Export data to Google Sheets
- Also check https://vercel.com/docs/pricing/manage-and-optimize-usage for directions
- If the above doesn't work, please check the USAGE_STATISTICS_GUIDE.md

---

## 💻 Getting Started: Clone, Test, and Deploy

### Step 1: Clone the Repository

1. **Install VS Code**:
   - Download from https://code.visualstudio.com/
   - Install on your computer

2. **Clone This Repository**:
   - Open VS Code
   - Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
   - Type "Git: Clone" and press Enter
   - Paste: `https://github.com/Moonwalkert3ch/malecare_chatbot.git`
   - Choose where to save it on your computer
   - Click "Open" when prompted

### Step 2: Test Locally

1. **Open Terminal in VS Code**:
   - Click "Terminal" menu → "New Terminal"

2. **Start the Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
   - Wait for "Application startup complete"

3. **Open Second Terminal**:
   - Click the `+` button in terminal panel

4. **Start the Frontend**:
   ```bash
   cd clinicaltrials-chatbot
   npm install
   npm run dev
   ```
   - Wait for "Ready" message

5. **Test in Browser**:
   - Open http://localhost:3000
   - Test the chatbot
   - Check admin dashboard at http://localhost:3000/admin

6. **Make Changes**:
   - Edit files in VS Code
   - Save (they auto-refresh in browser)
   - Test to ensure everything works

### Step 3: Deploy to Vercel

1. **Create Vercel Account**:
   - Go to https://vercel.com/
   - Sign up with GitHub

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose `malecare_chatbot`
   - Click "Import"

3. **Configure**:
   - **Framework Preset**: Next.js
   - **Root Directory**: `clinicaltrials-chatbot`
   - Click "Deploy"

4. **Your URL**:
   - The chatbot is live at https://malecarechatbot.vercel.app
   - Use this URL in the WordPress iframe above

**Note**: The backend (FastAPI) needs separate deployment. See Backend Deployment section below.

---

## 🔧 Backend Deployment Options

The FastAPI backend can be deployed alongside your Vercel frontend:

### Option 1: Vercel (Recommended - keeps everything together)
- Deploy backend as Vercel Serverless Functions
- Same platform as frontend
- See `clinicaltrials-chatbot/DEPLOYMENT.md` for details

### Option 2: Render.com (Alternative)
- Free tier available
- Easy Python deployments
- Connect your GitHub repo

### Option 3: Railway.app (Alternative)
- Simple setup
- Auto-deploys from GitHub
- Good for small projects

**Important**: After backend is deployed, update the frontend's API URL in `clinicaltrials-chatbot/lib/api.ts` to point to your backend URL.

---

## ✨ New Features

### Restart Chat Button
Users can restart their conversation at any time with a single click.

### Usage Statistics Tracking
- Automatically tracks user demographics (age, gender, location)
- Records cancer types and stages searched
- Counts messages sent and trials found
- Simple CSV export for Google Sheets
- Admin dashboard at `/admin`

### What's Tracked?
- User age, gender, and location
- Cancer type and stage
- Number of messages sent
- Number of trials found
- Session duration

**For Admin:** Visit `/admin` page, click "Download CSV", upload to Google Sheets. Simple!

---

## 📖 Documentation

- **[USAGE_STATISTICS_GUIDE.md](./USAGE_STATISTICS_GUIDE.md)** - How to use the admin dashboard
- **[DATABASE_IMPLEMENTATION_GUIDE.md](./DATABASE_IMPLEMENTATION_GUIDE.md)** - For webmasters: switching to database storage
- **[clinicaltrials-chatbot/DEPLOYMENT.md](./clinicaltrials-chatbot/DEPLOYMENT.md)** - Detailed deployment instructions

---

## 🏗️ Project Structure

```
MaleCare_ChatBot/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   │   ├── chat.py        # Chat functionality
│   │   │   ├── admin.py       # Admin dashboard endpoints
│   │   │   └── health.py      # Health check
│   │   └── services/
│   │       ├── usage_tracker.py    # NEW: Usage statistics
│   │       └── clinicaltrials_api.py
│   └── usage_stats.json       # Usage data storage
├── clinicaltrials-chatbot/    # Next.js frontend
│   └── app/
│       ├── page.tsx           # Main chatbot page
│       └── admin/
│           └── page.tsx       # NEW: Admin dashboard
└── models/                    # ML models
```

---

## 💻 Technology Stack

**Backend:**
- FastAPI (Python)
- ClinicalTrials.gov API v2
- BioClinicalBERT NLP models

**Frontend:**
- Next.js 16
- React
- TypeScript
- Tailwind CSS

---

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Backend runs at: http://localhost:8000

### Frontend Setup
```bash
cd clinicaltrials-chatbot
npm install
npm run dev
```
Frontend runs at: http://localhost:3000

### Admin Dashboard
Visit: http://localhost:3000/admin

---

## 📊 Usage Data Storage

**Current:** JSON file (`backend/usage_stats.json`)
- Simple, works great for testing
- Data persists when server restarts
- Download CSV backups regularly

**For Production:** See [DATABASE_IMPLEMENTATION_GUIDE.md](./DATABASE_IMPLEMENTATION_GUIDE.md)
- Options: PostgreSQL, MySQL, MongoDB
- Your webmaster can choose based on needs
- Easy migration path provided

---

## 🧪 Testing

### Test the Chatbot
1. Start both servers (backend and frontend)
2. Visit http://localhost:3000
3. Fill out the questionnaire
4. Send messages
5. Click "Restart Chat" button to reset

### Test Admin Dashboard
1. Visit http://localhost:3000/admin
2. View usage statistics
3. Click "Download CSV for Google Sheets"
4. Upload CSV to Google Sheets to analyze data

---



