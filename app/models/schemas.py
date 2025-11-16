"""
Pydantic models for request/response schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ReviewCategory(str, Enum):
    """Categories of code review issues"""
    LOGIC = "logic"
    READABILITY = "readability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    BEST_PRACTICES = "best_practices"


class Severity(str, Enum):
    """Severity levels for review comments"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ReviewComment(BaseModel):
    """Individual review comment"""
    line_number: Optional[int] = Field(None, description="Line number in the diff")
    file_path: str = Field(..., description="Path to the file")
    category: ReviewCategory = Field(..., description="Category of the issue")
    severity: Severity = Field(..., description="Severity of the issue")
    message: str = Field(..., description="Review comment message")
    suggestion: Optional[str] = Field(None, description="Suggested fix")
    code_snippet: Optional[str] = Field(None, description="Relevant code snippet")


class ReviewSummary(BaseModel):
    """Summary of the review"""
    total_comments: int = Field(..., description="Total number of review comments")
    critical_issues: int = Field(..., description="Number of critical issues")
    high_issues: int = Field(..., description="Number of high severity issues")
    medium_issues: int = Field(..., description="Number of medium severity issues")
    low_issues: int = Field(..., description="Number of low severity issues")
    categories: Dict[str, int] = Field(..., description="Issues by category")


class ReviewResponse(BaseModel):
    """Complete review response"""
    pr_url: Optional[str] = Field(None, description="GitHub PR URL")
    comments: List[ReviewComment] = Field(..., description="List of review comments")
    summary: ReviewSummary = Field(..., description="Review summary")
    agent_reports: Dict[str, Any] = Field(default_factory=dict, description="Individual agent reports")


class PRReviewRequest(BaseModel):
    """Request model for PR review"""
    pr_url: Optional[str] = Field(None, description="GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)")
    owner: Optional[str] = Field(None, description="Repository owner")
    repo: Optional[str] = Field(None, description="Repository name")
    pr_number: Optional[int] = Field(None, description="Pull request number")
    diff_text: Optional[str] = Field(None, description="Manual diff text input")
    file_path: Optional[str] = Field(None, description="File path for manual diff")
    enable_agents: Optional[Dict[str, bool]] = Field(
        default_factory=lambda: {
            "logic": True,
            "readability": True,
            "performance": True,
            "security": True
        },
        description="Enable/disable specific agents"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "1.0.0"

