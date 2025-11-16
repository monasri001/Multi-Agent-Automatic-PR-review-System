# 🔧 Troubleshooting Guide - "Connection Refused" Error

## Problem: Connection Refused Error

**Error Message:**
```
HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded
Failed to establish a new connection: [WinError 10061] 
No connection could be made because the target machine actively refused it
```

**This means:** The backend server is NOT running!

---

## ✅ Step-by-Step Solution

### Step 1: Check if Server Can Start

First, let's verify the server can start without errors:

```bash
# Make sure you're in the project directory
cd "D:\pr reviwer"

# Activate virtual environment
venv\Scripts\activate

# Try to start the server
python run_server.py
```

**What to look for:**

✅ **SUCCESS** - You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

❌ **ERROR** - If you see errors, note them down. Common issues:
- Import errors → Run `pip install -r requirements.txt`
- Missing .env file → Create `.env` with `GROQ_API_KEY`
- Port already in use → See Step 4 below

### Step 2: Keep Server Running

**IMPORTANT:** Once the server starts successfully:
- **DO NOT close the terminal**
- **DO NOT press Ctrl+C**
- **Keep it running!**

The server must stay running for Streamlit to connect to it.

### Step 3: Verify Server is Running

**In a NEW terminal** (keep the first one running!):

```bash
# Check if server is accessible
python check_server.py
```

Or test manually:
```bash
# Test health endpoint
curl http://localhost:8000/health
```

Or open in browser: http://localhost:8000/health

You should see: `{"status":"healthy","version":"1.0.0"}`

### Step 4: Start Streamlit (Only After Server is Running!)

**In a THIRD terminal** (or second if you closed the check one):

```bash
cd "D:\pr reviwer"
venv\Scripts\activate
streamlit run ui/streamlit_app.py
```

Now Streamlit should connect successfully!

---

## 🔍 Common Issues & Fixes

### Issue 1: Port 8000 Already in Use

**Error:** `Address already in use` or `Port 8000 is already in use`

**Solution:**

```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with the number from above)
taskkill /PID <PID> /F

# Or change the port in run_server.py
# Change port=8000 to port=8001
```

### Issue 2: Import Errors When Starting Server

**Error:** `ModuleNotFoundError` or `ImportError`

**Solution:**

```bash
# Make sure venv is activated
venv\Scripts\activate

# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue 3: Missing .env File

**Error:** Server starts but can't connect to Groq API

**Solution:**

1. Create `.env` file in project root
2. Add:
```env
GROQ_API_KEY=your_actual_groq_api_key
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
```

### Issue 4: Server Starts Then Immediately Crashes

**Check the error message in the terminal.** Common causes:

- **Missing GROQ_API_KEY**: Add it to `.env`
- **Invalid API key**: Verify key at https://console.groq.com/
- **Network issues**: Check internet connection

### Issue 5: "Can't reach this page" in Browser

**If you tried:** `http://0.0.0.0:8000`

**Use instead:** `http://localhost:8000` or `http://127.0.0.1:8000`

`0.0.0.0` is a server binding address, not a browser address!

---

## 📋 Complete Startup Checklist

Follow this checklist in order:

- [ ] **Terminal 1**: Navigate to project directory
- [ ] **Terminal 1**: Activate virtual environment (`venv\Scripts\activate`)
- [ ] **Terminal 1**: Run `python run_server.py`
- [ ] **Terminal 1**: See "Uvicorn running" message
- [ ] **Terminal 1**: Keep terminal open (don't close!)
- [ ] **Browser**: Test http://localhost:8000/health (should work)
- [ ] **Terminal 2**: Open NEW terminal
- [ ] **Terminal 2**: Navigate to project directory
- [ ] **Terminal 2**: Activate virtual environment
- [ ] **Terminal 2**: Run `streamlit run ui/streamlit_app.py`
- [ ] **Browser**: Streamlit opens at http://localhost:8501
- [ ] **Success!**: Both servers running, UI should work

---

## 🎯 Quick Test Procedure

1. **Terminal 1:**
   ```bash
   cd "D:\pr reviwer"
   venv\Scripts\activate
   python run_server.py
   ```
   Wait for: `INFO: Uvicorn running...`

2. **Browser:**
   Visit: http://localhost:8000/health
   Should see: `{"status":"healthy","version":"1.0.0"}`

3. **Terminal 2:**
   ```bash
   cd "D:\pr reviwer"
   venv\Scripts\activate
   streamlit run ui/streamlit_app.py
   ```

4. **Browser:**
   Streamlit opens automatically at http://localhost:8501

---

## 🆘 Still Not Working?

1. **Check both terminals are open and running**
2. **Verify server is actually running** (use `check_server.py`)
3. **Check for error messages** in Terminal 1 (where server runs)
4. **Verify .env file exists** and has correct API key
5. **Try restarting** both terminals

---

## 💡 Pro Tip

Create a batch file to start both servers:

**Create `start_all.bat`:**
```batch
@echo off
start cmd /k "cd /d D:\pr reviwer && venv\Scripts\activate && python run_server.py"
timeout /t 3
start cmd /k "cd /d D:\pr reviwer && venv\Scripts\activate && streamlit run ui/streamlit_app.py"
```

Then just double-click `start_all.bat` to start everything!

