"""
Performance Review Agent - Identifies performance issues and optimizations
"""
from typing import List
from app.agents.base_agent import BaseAgent
from app.models.schemas import ReviewCategory


class PerformanceAgent(BaseAgent):
    """Agent specialized in identifying performance issues"""
    
    def __init__(self):
        super().__init__("PerformanceAgent", ReviewCategory.PERFORMANCE)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert code reviewer specializing in performance optimization and efficiency.

Your task is to analyze code changes and identify:
1. Inefficient algorithms (O(n²) when O(n) is possible)
2. Unnecessary database queries or API calls
3. Missing caching opportunities
4. Inefficient data structures
5. N+1 query problems
6. Unnecessary loops or iterations
7. Memory leaks or excessive memory usage
8. Blocking operations in async code
9. Inefficient string concatenation
10. Missing indexes or inefficient database queries

Provide your findings as a JSON array of comments, each with:
- line_number: the line number (if applicable)
- severity: "critical", "high", "medium", "low", or "info"
- message: clear description of the performance issue
- suggestion: specific suggestion to optimize
- code_snippet: relevant code snippet (if applicable)

Format your response as JSON:
{
  "comments": [
    {
      "line_number": 30,
      "severity": "high",
      "message": "Nested loop creates O(n²) complexity",
      "suggestion": "Use a dictionary/set for O(1) lookups instead",
      "code_snippet": "for i in list1:\n  for j in list2:\n    if i == j: ..."
    }
  ]
}"""
    
    def _get_review_prompt(self, diff_content: str, file_path: str) -> str:
        return f"""Analyze the following code changes for performance issues:

File: {file_path}

Diff:
{diff_content}

Focus on:
- Algorithm complexity
- Database query efficiency
- Caching opportunities
- Memory usage
- Unnecessary operations
- N+1 query problems
- Async/await usage
- Data structure choices

Provide your analysis as a JSON array of review comments."""

