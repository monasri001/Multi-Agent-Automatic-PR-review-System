# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-70b-versatile
GITHUB_TOKEN=your_token_here  # Optional
```

Get your free Groq API key from: https://console.groq.com/

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Start Server
```bash
python run_server.py
```

### 5. Open UI
In a new terminal:
```bash
streamlit run ui/streamlit_app.py
```

## 📝 Example Usage

### Via UI
1. Open Streamlit UI (http://localhost:8501)
2. Enter PR URL or paste diff
3. Click "Review PR"
4. View results!

### Via API
```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{"diff_text": "--- a/test.py\n+++ b/test.py\n@@ -1 +1,2 @@\n def test():\n     pass\n+    return None"}'
```

## 🎯 What Each Agent Does

- **Logic Agent**: Finds bugs and logical errors
- **Readability Agent**: Checks code quality and style
- **Performance Agent**: Identifies bottlenecks
- **Security Agent**: Detects vulnerabilities

## 📚 Full Documentation

See `README.md` and `IMPLEMENTATION_GUIDE.md` for detailed information.

