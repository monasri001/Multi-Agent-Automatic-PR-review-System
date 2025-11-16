# Step-by-Step Implementation Guide

This guide will walk you through setting up and running the PR Review Agent project from scratch.

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- A Groq API key (get one from https://console.groq.com/ - free tier available)
- A GitHub personal access token (optional, for fetching PRs directly)
- Git installed (optional)

## Step 1: Project Setup

### 1.1 Navigate to Project Directory

```bash
cd "pr reviwer"
```

### 1.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### 1.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (web framework)
- LangChain and Groq (LLM integration for Llama3)
- Streamlit (UI)
- Requests (HTTP client)
- Pydantic (data validation)

## Step 2: Configuration

### 2.1 Create Environment File

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2.2 Edit .env File

Open `.env` in a text editor and add your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
GITHUB_TOKEN=ghp_your_github_token_here
```

**Important Notes:**
- Get your Groq API key from https://console.groq.com/ (free tier available)
- Replace `your_groq_api_key_here` with your real Groq API key
- Replace `ghp_your_github_token_here` with your GitHub token (or leave empty if not using GitHub API)
- Available models: `llama-3.1-70b-versatile` (best), `llama-3.1-8b-instant` (faster), `llama-3-70b-8192`, `llama-3-8b-8192`

### 2.3 Get GitHub Token (Optional)

If you want to fetch PRs directly from GitHub:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (for private repos) or `public_repo` (for public repos only)
4. Copy the token and paste it in `.env`

## Step 3: Verify Project Structure

Ensure your project structure looks like this:

```
pr-reviewer/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── logic_agent.py
│   │   ├── readability_agent.py
│   │   ├── performance_agent.py
│   │   └── security_agent.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github_service.py
│   │   ├── diff_parser.py
│   │   └── review_orchestrator.py
│   └── models/
│       ├── __init__.py
│       └── schemas.py
├── ui/
│   └── streamlit_app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Step 4: Test the Backend API

### 4.1 Start the FastAPI Server

Open a terminal (with venv activated) and run:

```bash
python -m app.main
```

Or:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4.2 Test Health Endpoint

Open a new terminal and test:

```bash
# Windows PowerShell
curl http://localhost:8000/health

# Or use browser
# Visit: http://localhost:8000/health
```

You should see:
```json
{"status":"healthy","version":"1.0.0"}
```

### 4.3 Test Review Endpoint with Sample Diff

```bash
# Windows PowerShell
curl -X POST "http://localhost:8000/review" -H "Content-Type: application/json" -d '{\"diff_text\": \"--- a/test.py\n+++ b/test.py\n@@ -1,2 +1,3 @@\n def hello():\n     print(\\\"Hello\\\")\n+    return None\"}'
```

Or use a tool like Postman or the Swagger UI at `http://localhost:8000/docs`

## Step 5: Run the Streamlit UI

### 5.1 Start Streamlit (in a new terminal)

Make sure your FastAPI server is still running, then:

```bash
# Activate venv in new terminal
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

streamlit run ui/streamlit_app.py
```

Streamlit will open automatically in your browser at `http://localhost:8501`

### 5.2 Use the UI

1. **For GitHub PR Review:**
   - Select "GitHub PR URL" mode
   - Enter a PR URL (e.g., `https://github.com/microsoft/vscode/pull/12345`)
   - Select which agents to enable
   - Click "Review PR"

2. **For Manual Diff Review:**
   - Select "Manual Diff Input" mode
   - Optionally enter file path
   - Paste your diff text
   - Click "Review Diff"

3. **View Results:**
   - See summary metrics
   - Browse comments by file
   - Filter by severity and category
   - Download results as JSON

## Step 6: Test with Real GitHub PR

### 6.1 Find a Public PR

Choose a public repository PR, for example:
- `https://github.com/microsoft/vscode/pull/12345`
- `https://github.com/facebook/react/pull/12345`

### 6.2 Review via UI

1. Open Streamlit UI
2. Select "GitHub PR URL"
3. Paste the PR URL
4. Enable all agents
5. Click "Review PR"
6. Wait for analysis (may take 30-60 seconds)

### 6.3 Review via API

```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d "{\"pr_url\": \"https://github.com/owner/repo/pull/123\"}"
```

## Step 7: Understanding the Output

### Review Response Structure

```json
{
  "pr_url": "...",
  "comments": [
    {
      "line_number": 42,
      "file_path": "src/main.py",
      "category": "security",
      "severity": "critical",
      "message": "Issue description",
      "suggestion": "How to fix it",
      "code_snippet": "Relevant code"
    }
  ],
  "summary": {
    "total_comments": 10,
    "critical_issues": 2,
    "high_issues": 3,
    ...
  },
  "agent_reports": {
    "security": {"total_comments": 2, "files_reviewed": 1},
    ...
  }
}
```

### Severity Levels

- **Critical**: Must fix immediately (security vulnerabilities, critical bugs)
- **High**: Should fix soon (major logic errors, performance issues)
- **Medium**: Should consider fixing (readability, best practices)
- **Low**: Nice to have (minor improvements)
- **Info**: Informational comments

## Step 8: Customization

### 8.1 Change LLM Model

Edit `.env`:
```env
LLM_MODEL=llama-3.1-8b-instant  # Faster but lower quality
# or
LLM_MODEL=llama-3.1-70b-versatile  # Best quality (default)
# or
LLM_MODEL=llama-3-70b-8192  # Alternative 70B model
```

### 8.2 Adjust Agent Behavior

Edit agent prompts in:
- `app/agents/logic_agent.py`
- `app/agents/readability_agent.py`
- `app/agents/performance_agent.py`
- `app/agents/security_agent.py`

### 8.3 Modify API Port

Edit `app/main.py`:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
```

## Step 9: Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Ensure venv is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Groq API Error"

**Solutions:**
- Check `.env` file has correct `GROQ_API_KEY`
- Verify API key is valid at https://console.groq.com/
- Check you have API credits (free tier available)
- Try using `llama-3.1-8b-instant` if `llama-3.1-70b-versatile` is unavailable

### Issue: "GitHub API Error"

**Solutions:**
- Check `.env` has `GITHUB_TOKEN` (if using GitHub API)
- Verify token has correct permissions
- For public repos, token is optional
- Check rate limits (GitHub allows 60 requests/hour without token)

### Issue: "Port Already in Use"

**Solution:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
# Kill process (replace PID):
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Issue: "Streamlit Can't Connect to API"

**Solution:**
- Ensure FastAPI server is running on port 8000
- Check `ui/streamlit_app.py` has correct `API_URL`
- Try accessing API directly: `http://localhost:8000/health`

## Step 10: Production Deployment (Optional)

### 10.1 Environment Variables

Set environment variables on your hosting platform:
- Heroku: Use Config Vars
- AWS: Use Parameter Store or Secrets Manager
- Docker: Use environment file

### 10.2 Run with Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 10.3 Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Next Steps

1. **Experiment with Different PRs**: Test with various codebases
2. **Fine-tune Agents**: Adjust prompts for your specific needs
3. **Add Custom Agents**: Create domain-specific review agents
4. **Integrate with CI/CD**: Add webhook support for automatic reviews
5. **Add Caching**: Cache reviews for unchanged code
6. **Support More Languages**: Extend agents for other programming languages

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all environment variables are set correctly
3. Check API logs for detailed error messages
4. Ensure all dependencies are installed

## Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `.env` file configured with API keys
- [ ] FastAPI server starts without errors
- [ ] Health endpoint returns success
- [ ] Streamlit UI opens and connects to API
- [ ] Can review a sample diff
- [ ] Can review a GitHub PR (if token configured)
- [ ] Review results display correctly

Congratulations! Your PR Review Agent is now set up and ready to use! 🎉

