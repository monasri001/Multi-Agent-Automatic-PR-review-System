"""
Readability Review Agent - Identifies code readability and maintainability issues
"""
from typing import List
from app.agents.base_agent import BaseAgent
from app.models.schemas import ReviewCategory


class ReadabilityAgent(BaseAgent):
    """Agent specialized in code readability and maintainability"""
    
    def __init__(self):
        super().__init__("ReadabilityAgent", ReviewCategory.READABILITY)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert code reviewer specializing in code readability, maintainability, and style.

Your task is to analyze code changes and identify:
1. Poor variable and function naming
2. Long functions or methods that should be split
3. Complex nested conditionals
4. Missing or unclear comments
5. Code duplication
6. Inconsistent code style
7. Magic numbers and hardcoded values
8. Unclear code structure
9. Missing docstrings
10. Overly complex expressions

Provide your findings as a JSON array of comments, each with:
- line_number: the line number (if applicable)
- severity: "critical", "high", "medium", "low", or "info"
- message: clear description of the issue
- suggestion: specific suggestion to improve readability
- code_snippet: relevant code snippet (if applicable)

Format your response as JSON:
{
  "comments": [
    {
      "line_number": 15,
      "severity": "medium",
      "message": "Variable name 'x' is not descriptive",
      "suggestion": "Rename to 'user_count' or similar descriptive name",
      "code_snippet": "x = len(users)"
    }
  ]
}"""
    
    def _get_review_prompt(self, diff_content: str, file_path: str) -> str:
        return f"""Analyze the following code changes for readability and maintainability issues:

File: {file_path}

Diff:
{diff_content}

Focus on:
- Variable and function naming
- Code structure and organization
- Comments and documentation
- Code complexity
- Style consistency
- Magic numbers
- Code duplication

Provide your analysis as a JSON array of review comments."""

