# Automated GitHub Pull Request Review Agent

An intelligent, multi-agent system for automated code review of GitHub Pull Requests. This system uses multiple specialized AI agents to analyze code changes and provide comprehensive, actionable review comments.

<img width="1918" height="928" alt="Screenshot 2025-11-14 113719" src="https://github.com/user-attachments/assets/a102ba1b-172a-4a0b-b650-7522b7b4a584" />

<img width="1919" height="969" alt="Screenshot 2025-11-14 113730" src="https://github.com/user-attachments/assets/98b32fb4-c314-434e-beef-b43668da0374" />


## 🎯 Features

- **Multi-Agent Architecture**: Four specialized agents working together:
  - **Logic Agent**: Identifies logical errors, bugs, and correctness issues
  - **Readability Agent**: Analyzes code readability, maintainability, and style
  - **Performance Agent**: Detects performance bottlenecks and optimization opportunities
  - **Security Agent**: Identifies security vulnerabilities and best practices

- **Flexible Input Methods**:
  - GitHub PR URL (automatic fetching)
  - Manual diff text input
  - Direct API calls

- **Comprehensive Analysis**:
  - Structured review comments with severity levels
  - Code suggestions and improvements
  - File-level and line-level analysis
  - Summary statistics and agent reports

- **Modern Tech Stack**:
  - FastAPI for RESTful API
  - LangChain for LLM orchestration
  - Streamlit for user-friendly UI
  - Llama3 via Groq API for intelligent analysis (fast and cost-effective)

## 📋 Requirements

- Python 3.8+
- Groq API key (get one from https://console.groq.com/)
- GitHub token (optional, for fetching PRs directly)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd "pr reviwer"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-70b-versatile
LLM_TEMPERATURE=0.3
GITHUB_TOKEN=your_github_token_here  # Optional
```

**Available Groq Llama3 Models:**
- `llama-3.1-70b-versatile` (recommended, best quality)
- `llama-3.1-8b-instant` (faster, good quality)
- `llama-3-70b-8192`
- `llama-3-8b-8192`
- `mixtral-8x7b-32768`

### 3. Run the Application

#### Option A: Run FastAPI Backend

```bash
# From project root
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

#### Option B: Run Streamlit UI

```bash
# In a new terminal (with venv activated)
streamlit run ui/streamlit_app.py
```

The UI will open in your browser at `http://localhost:8501`

### 4. Test the API

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 📖 Usage

### Using Streamlit UI

1. Start the FastAPI backend (if not already running)
2. Start the Streamlit UI
3. Choose review mode:
   - **GitHub PR URL**: Enter a PR URL like `https://github.com/owner/repo/pull/123`
   - **Manual Diff Input**: Paste your diff text directly
4. Select which agents to enable
5. Click "Review PR" or "Review Diff"
6. View results with filtering options

### Using API Directly

#### Review via PR URL

```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{
    "pr_url": "https://github.com/owner/repo/pull/123",
    "enable_agents": {
      "logic": true,
      "readability": true,
      "performance": true,
      "security": true
    }
  }'
```

#### Review via Manual Diff

```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{
    "diff_text": "--- a/file.py\n+++ b/file.py\n@@ -1,3 +1,4 @@\n def test():\n     pass\n+    return None",
    "file_path": "file.py"
  }'
```

#### Async Review (Faster for Large PRs)

```bash
curl -X POST "http://localhost:8000/review/async" \
  -H "Content-Type: application/json" \
  -d '{
    "pr_url": "https://github.com/owner/repo/pull/123"
  }'
```

## 🏗️ Project Structure

```
pr-reviewer/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Base agent class
│   │   ├── logic_agent.py      # Logic review agent
│   │   ├── readability_agent.py # Readability review agent
│   │   ├── performance_agent.py  # Performance review agent
│   │   └── security_agent.py     # Security review agent
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github_service.py    # GitHub API integration
│   │   ├── diff_parser.py       # Diff parsing utilities
│   │   └── review_orchestrator.py # Multi-agent orchestration
│   └── models/
│       ├── __init__.py
│       └── schemas.py           # Pydantic models
├── ui/
│   └── streamlit_app.py         # Streamlit UI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `GITHUB_TOKEN`: GitHub personal access token (optional, for PR fetching)
- `LLM_MODEL`: LLM model to use (default: `gpt-4`)
- `LLM_TEMPERATURE`: Temperature for LLM (default: `0.3`)
- `MAX_TOKENS`: Maximum tokens per agent response (default: `2000`)

### Agent Configuration

You can enable/disable specific agents per request:

```json
{
  "enable_agents": {
    "logic": true,
    "readability": true,
    "performance": false,
    "security": true
  }
}
```

## 📊 Response Format

The API returns structured review data:

```json
{
  "pr_url": "https://github.com/owner/repo/pull/123",
  "comments": [
    {
      "line_number": 42,
      "file_path": "src/main.py",
      "category": "security",
      "severity": "critical",
      "message": "SQL injection vulnerability detected",
      "suggestion": "Use parameterized queries",
      "code_snippet": "query = f'SELECT * FROM users WHERE id = {user_id}'"
    }
  ],
  "summary": {
    "total_comments": 15,
    "critical_issues": 2,
    "high_issues": 5,
    "medium_issues": 6,
    "low_issues": 2,
    "categories": {
      "security": 2,
      "logic": 5,
      "readability": 6,
      "performance": 2
    }
  },
  "agent_reports": {
    "security": {
      "total_comments": 2,
      "files_reviewed": 1
    }
  }
}
```

## 🧪 Testing

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

### Test with Sample Diff

```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{
    "diff_text": "--- a/test.py\n+++ b/test.py\n@@ -1,2 +1,3 @@\n def hello():\n     print(\"Hello\")\n+    return None"
  }'
```

## 🔍 How It Works

1. **Input Processing**: System accepts PR URL or manual diff text
2. **Diff Parsing**: Extracts file-level changes and line numbers
3. **Multi-Agent Analysis**: Each enabled agent analyzes the code:
   - Logic Agent checks for bugs and logical errors
   - Readability Agent evaluates code quality
   - Performance Agent identifies bottlenecks
   - Security Agent scans for vulnerabilities
4. **Orchestration**: Review orchestrator coordinates agents and aggregates results
5. **Response Generation**: Structured comments with severity, suggestions, and code snippets

## 🛠️ Extending the System

### Adding a New Agent

1. Create a new agent class in `app/agents/`:

```python
from app.agents.base_agent import BaseAgent
from app.models.schemas import ReviewCategory

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("CustomAgent", ReviewCategory.BEST_PRACTICES)
    
    def _get_system_prompt(self) -> str:
        return "Your system prompt here..."
    
    def _get_review_prompt(self, diff_content: str, file_path: str) -> str:
        return f"Your review prompt here..."
```

2. Register it in `review_orchestrator.py`:

```python
from app.agents.custom_agent import CustomAgent

self.agents = {
    ...
    'custom': CustomAgent()
}
```

## 📝 Notes

- The system uses **Llama3 via Groq API** for fast and cost-effective code reviews.
- Groq provides extremely fast inference speeds (often 10x faster than traditional APIs).
- Get your free Groq API key from https://console.groq.com/
- For large PRs, use the async endpoint (`/review/async`) for better performance.
- GitHub token is optional but recommended for accessing private repositories.
- Review quality depends on the model used (`llama-3.1-70b-versatile` recommended for best results).

## 🤝 Contributing

This is a modular system designed for easy extension. Feel free to:
- Add new specialized agents
- Improve diff parsing
- Enhance UI features
- Add support for other LLM providers

## 📄 License

This project is provided as-is for educational and development purposes.

## 🐛 Troubleshooting

### API Key Issues
- Ensure `OPENAI_API_KEY` is set in `.env`
- Check that your API key has sufficient credits

### GitHub API Issues
- Verify `GITHUB_TOKEN` is valid
- Check repository access permissions

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Port Already in Use
- Change port in `app/main.py` or use `--port` flag with uvicorn

## 📚 API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

