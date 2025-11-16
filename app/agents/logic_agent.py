"""
Logic Review Agent - Identifies logical errors and bugs
"""
from typing import List
from app.agents.base_agent import BaseAgent
from app.models.schemas import ReviewCategory


class LogicAgent(BaseAgent):
    """Agent specialized in identifying logical errors and bugs"""
    
    def __init__(self):
        super().__init__("LogicAgent", ReviewCategory.LOGIC)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert code reviewer specializing in identifying logical errors, bugs, and correctness issues in code.

Your task is to analyze code changes and identify:
1. Logic errors and bugs
2. Incorrect algorithm implementations
3. Edge cases that are not handled
4. Incorrect conditionals or loops
5. Type mismatches and incorrect data handling
6. Missing null/None checks
7. Incorrect variable assignments
8. Off-by-one errors
9. Incorrect function return values
10. Race conditions and concurrency issues

Provide your findings as a JSON array of comments, each with:
- line_number: the line number (if applicable)
- severity: "critical", "high", "medium", "low", or "info"
- message: clear description of the issue
- suggestion: specific suggestion to fix the issue
- code_snippet: relevant code snippet (if applicable)

Format your response as JSON:
{
  "comments": [
    {
      "line_number": 42,
      "severity": "high",
      "message": "Missing null check before accessing user object",
      "suggestion": "Add null check: if user is not None: ...",
      "code_snippet": "user.name"
    }
  ]
}"""
    
    def _get_review_prompt(self, diff_content: str, file_path: str) -> str:
        return f"""Analyze the following code changes for logical errors and bugs:

File: {file_path}

Diff:
{diff_content}

Focus on:
- Logic errors and bugs
- Edge cases not handled
- Incorrect conditionals
- Missing null/None checks
- Type mismatches
- Algorithm correctness
- Concurrency issues

Provide your analysis as a JSON array of review comments."""

