# ⚡ Quick Run Guide - Copy & Paste Commands

## 🎯 Fastest Way to Get Started

### Step 1: Get Groq API Key
Visit: https://console.groq.com/ → Create API Key

### Step 2: Setup (One Time)

```bash
# Navigate to project
cd "D:\pr reviwer"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Create .env File

Create file `.env` in project root with:
```env
GROQ_API_KEY=your_key_here
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
```

### Step 4: Test Setup
```bash
python test_setup.py
```

### Step 5: Run Application

**Terminal 1 (Backend):**
```bash
python run_server.py
```

**Terminal 2 (UI):**
```bash
streamlit run ui/streamlit_app.py
```

### Step 6: Open Browser
Visit: http://localhost:8501

---

## 🚨 Troubleshooting

**Import errors?**
```bash
pip install -r requirements.txt
```

**Port in use?**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**API key error?**
- Check `.env` file exists
- Verify key is correct
- Restart server

---

## 📖 Full Guide
See `RUN_GUIDE.md` for detailed instructions.

