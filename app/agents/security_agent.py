"""
Security Review Agent - Identifies security vulnerabilities
"""
from typing import List
from app.agents.base_agent import BaseAgent
from app.models.schemas import ReviewCategory


class SecurityAgent(BaseAgent):
    """Agent specialized in identifying security vulnerabilities"""
    
    def __init__(self):
        super().__init__("SecurityAgent", ReviewCategory.SECURITY)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert security code reviewer specializing in identifying security vulnerabilities.

Your task is to analyze code changes and identify:
1. SQL injection vulnerabilities
2. Cross-site scripting (XSS) vulnerabilities
3. Authentication and authorization issues
4. Sensitive data exposure
5. Insecure direct object references
6. Missing input validation
7. Hardcoded secrets or credentials
8. Insecure random number generation
9. Path traversal vulnerabilities
10. Insecure deserialization
11. Missing CSRF protection
12. Insecure cryptographic storage
13. Race conditions in security checks
14. Insecure API endpoints

Provide your findings as a JSON array of comments, each with:
- line_number: the line number (if applicable)
- severity: "critical", "high", "medium", "low", or "info"
- message: clear description of the security issue
- suggestion: specific suggestion to fix the vulnerability
- code_snippet: relevant code snippet (if applicable)

Format your response as JSON:
{
  "comments": [
    {
      "line_number": 25,
      "severity": "critical",
      "message": "SQL injection vulnerability: user input directly concatenated into query",
      "suggestion": "Use parameterized queries or ORM methods",
      "code_snippet": "query = f\"SELECT * FROM users WHERE id = {user_id}\""
    }
  ]
}"""
    
    def _get_review_prompt(self, diff_content: str, file_path: str) -> str:
        return f"""Analyze the following code changes for security vulnerabilities:

File: {file_path}

Diff:
{diff_content}

Focus on:
- SQL injection
- XSS vulnerabilities
- Authentication/authorization
- Input validation
- Secret management
- Cryptographic issues
- Path traversal
- CSRF protection
- Insecure deserialization
- API security

Provide your analysis as a JSON array of review comments. Be thorough and prioritize critical security issues."""

