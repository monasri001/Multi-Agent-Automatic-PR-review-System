# 🚀 Complete Step-by-Step Guide to Run the PR Review Agent

This guide will walk you through running the project from scratch, step by step.

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ Internet connection (for API calls)
- ✅ A Groq API key (free at https://console.groq.com/)
- ✅ (Optional) GitHub token for fetching PRs directly

---

## Step 1: Get Your Groq API Key

1. **Visit Groq Console**: Go to https://console.groq.com/
2. **Sign Up**: Create a free account (no credit card required)
3. **Get API Key**:
   - Click on "API Keys" in the left sidebar
   - Click "Create API Key"
   - Copy the key (you'll need it in Step 3)

**Note**: The free tier is very generous and perfect for testing!

---

## Step 2: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`, type `cmd` or `powershell`, press Enter
- Or use VS Code terminal (Ctrl + `)

**Mac/Linux:**
- Open Terminal application
- Or use VS Code terminal

**Navigate to project directory:**
```bash
cd "D:\pr reviwer"
```
(Adjust the path to match your project location)

---

## Step 3: Create Virtual Environment

**Why?** Virtual environments keep project dependencies isolated.

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Success indicator**: You should see `(venv)` at the start of your terminal prompt.

**If you get an error:**
- Windows: Try `py -m venv venv` instead
- Mac/Linux: Try `python3` instead of `python`

---

## Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**This will install:**
- FastAPI (web framework)
- LangChain (LLM integration)
- Streamlit (UI)
- Requests (HTTP client)
- And other required packages

**Expected output**: You should see packages being installed. Wait for it to complete.

**If you get errors:**
- Make sure virtual environment is activated (see `(venv)` in prompt)
- Try: `pip install --upgrade pip` first
- On Windows, you might need Visual C++ Build Tools for some packages

---

## Step 5: Create Environment File

### Option A: Manual Creation

1. In your project root directory (`D:\pr reviwer`), create a new file named `.env`
2. Open it in a text editor
3. Add the following content:

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
GITHUB_TOKEN=your_github_token_here
```

4. **Replace** `your_groq_api_key_here` with the API key you got in Step 1
5. **Replace** `your_github_token_here` with your GitHub token (or leave empty if not using GitHub API)
6. Save the file

### Option B: Copy from Example (if .env.example exists)

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Then edit `.env` and add your API keys.

**Important**: The `.env` file should be in the project root, same folder as `requirements.txt`

---

## Step 6: Test Your Setup

Run the test script to verify everything is configured correctly:

```bash
python test_setup.py
```

**Expected output:**
```
==================================================
PR Review Agent - Setup Test
==================================================
Testing imports...
✓ Config imported
✓ LogicAgent imported
✓ ReadabilityAgent imported
✓ PerformanceAgent imported
✓ SecurityAgent imported
✓ GitHubService imported
✓ DiffParser imported
✓ ReviewOrchestrator imported
✓ FastAPI app imported

✅ All imports successful!

Testing configuration...
✓ GROQ_API_KEY configured
✓ LLM Model: llama-3.1-70b-versatile
✓ Max Tokens: 2000

==================================================
✅ Setup looks good! You can now run the server.
```

**If you see errors:**
- **Import errors**: Run `pip install -r requirements.txt` again
- **API key warning**: Make sure `.env` file exists and has `GROQ_API_KEY=your_key`
- **Other errors**: Check the error message and fix accordingly

---

## Step 7: Start the FastAPI Backend Server

**Keep the terminal open** (the one with venv activated) and run:

```bash
python run_server.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Success!** Your API server is now running on `http://localhost:8000`

**Keep this terminal window open!** The server needs to keep running.

**To stop the server**: Press `Ctrl + C` in the terminal

---

## Step 8: Open a New Terminal for Streamlit UI

**Important**: Keep the FastAPI server running in the first terminal!

1. **Open a new terminal/command prompt**
2. **Navigate to project directory again:**
   ```bash
   cd "D:\pr reviwer"
   ```
3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```
4. **Start Streamlit UI:**
   ```bash
   streamlit run ui/streamlit_app.py
   ```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**The UI will automatically open in your browser!** If not, manually visit: http://localhost:8501

---

## Step 9: Use the Application

### Option A: Using Streamlit UI (Recommended for Beginners)

1. **In the browser** (http://localhost:8501), you'll see the PR Review Agent interface

2. **Choose Review Mode:**
   - **GitHub PR URL**: Enter a PR URL like `https://github.com/microsoft/vscode/pull/12345`
   - **Manual Diff Input**: Paste your diff text directly

3. **Select Agents** (in the sidebar):
   - ✅ Logic Agent (finds bugs)
   - ✅ Readability Agent (code quality)
   - ✅ Performance Agent (optimization)
   - ✅ Security Agent (vulnerabilities)

4. **Click "Review PR" or "Review Diff"**

5. **Wait for analysis** (usually 30-60 seconds)

6. **View results**:
   - Summary statistics
   - Review comments by file
   - Filter by severity and category
   - Download results as JSON

### Option B: Using API Directly

**Test the API** (in a new terminal or browser):

```bash
# Health check
curl http://localhost:8000/health
```

**Or visit in browser:**
- API Docs: http://localhost:8000/docs (Interactive Swagger UI)
- Health: http://localhost:8000/health

**Review a PR via API:**
```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d "{\"pr_url\": \"https://github.com/owner/repo/pull/123\"}"
```

**Review a manual diff:**
```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d "{\"diff_text\": \"--- a/test.py\n+++ b/test.py\n@@ -1 +1,2 @@\n def test():\n     pass\n+    return None\"}"
```

---

## Step 10: Verify Everything Works

### Quick Test

1. **In Streamlit UI**, try reviewing a simple diff:
   - Select "Manual Diff Input"
   - Paste this diff:
     ```
     --- a/test.py
     +++ b/test.py
     @@ -1,2 +1,3 @@
      def hello():
          print("Hello")
     +    return None
     ```
   - Click "Review Diff"
   - You should see review comments appear!

2. **Check API**:
   - Visit http://localhost:8000/docs
   - Try the `/health` endpoint
   - Try the `/review` endpoint with a test diff

---

## 🎉 Success! You're All Set!

Your PR Review Agent is now running and ready to use!

---

## 📝 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError" or Import Errors

**Solution:**
```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "GROQ_API_KEY not set"

**Solution:**
1. Check that `.env` file exists in project root
2. Check that it contains: `GROQ_API_KEY=your_actual_key`
3. Make sure there are no spaces around the `=` sign
4. Restart the server after changing `.env`

### Issue 3: "Port 8000 already in use"

**Solution:**
```bash
# Windows - Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in run_server.py
```

### Issue 4: "Streamlit can't connect to API"

**Solution:**
1. Make sure FastAPI server is running (Step 7)
2. Check that it's running on port 8000
3. Verify in browser: http://localhost:8000/health should work
4. Check `ui/streamlit_app.py` has `API_URL = "http://localhost:8000"`

### Issue 5: "Groq API Error: 401 Unauthorized"

**Solution:**
1. Verify your API key is correct in `.env`
2. Check key is active at https://console.groq.com/
3. Make sure key starts with `gsk_` (Groq key format)

### Issue 6: "Groq API Error: 429 Too Many Requests"

**Solution:**
- You've hit rate limits
- Wait a few minutes and try again
- Free tier has generous limits, but not unlimited

### Issue 7: Virtual Environment Not Activating

**Windows:**
```bash
# If venv\Scripts\activate doesn't work, try:
venv\Scripts\activate.bat
# Or
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
# Make sure you're using source
source venv/bin/activate
```

---

## 🔄 Daily Usage Workflow

Once everything is set up, your daily workflow is:

1. **Open terminal 1:**
   ```bash
   cd "D:\pr reviwer"
   venv\Scripts\activate  # or source venv/bin/activate
   python run_server.py
   ```

2. **Open terminal 2:**
   ```bash
   cd "D:\pr reviwer"
   venv\Scripts\activate
   streamlit run ui/streamlit_app.py
   ```

3. **Use the UI** at http://localhost:8501

4. **When done**, press `Ctrl+C` in both terminals to stop servers

---

## 📚 Additional Resources

- **Full Documentation**: See `README.md`
- **Implementation Details**: See `IMPLEMENTATION_GUIDE.md`
- **Groq Setup**: See `GROQ_SETUP.md`
- **Quick Reference**: See `QUICK_START.md`

---

## 🆘 Still Having Issues?

1. **Check all steps** were followed correctly
2. **Verify** `.env` file exists and has correct API key
3. **Test** with `python test_setup.py`
4. **Check** both servers are running (FastAPI + Streamlit)
5. **Review** error messages carefully - they usually tell you what's wrong

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `GROQ_API_KEY`
- [ ] Test script passes (`python test_setup.py`)
- [ ] FastAPI server running (`python run_server.py`)
- [ ] Streamlit UI running (`streamlit run ui/streamlit_app.py`)
- [ ] Can access UI at http://localhost:8501
- [ ] Can perform a test review

**If all checkboxes are checked, you're ready to go! 🎉**

