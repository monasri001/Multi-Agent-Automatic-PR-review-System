"""
Base agent class for all review agents
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models.schemas import ReviewComment, ReviewCategory
from app.config import settings
from langchain_core.messages import HumanMessage, SystemMessage
from app.services.groq_llm import GroqChatLLM
import json


class BaseAgent(ABC):
    """Base class for all review agents"""
    
    def __init__(self, agent_name: str, category: ReviewCategory):
        self.agent_name = agent_name
        self.category = category
        self.llm = GroqChatLLM(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def _get_review_prompt(self, diff_content: str, file_path: str) -> str:
        """Get the review prompt for this agent"""
        pass
    
    def analyze(self, diff_content: str, file_path: str, changed_lines: List[int]) -> List[ReviewComment]:
        """
        Analyze code changes and return review comments
        
        Args:
            diff_content: The diff content to analyze
            file_path: Path to the file being reviewed
            changed_lines: List of changed line numbers
            
        Returns:
            List of ReviewComment objects
        """
        try:
            prompt = self._get_review_prompt(diff_content, file_path)
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            review_text = response.content
            
            # Parse the LLM response into structured comments
            comments = self._parse_response(review_text, file_path, changed_lines)
            
            return comments
        except Exception as e:
            print(f"Error in {self.agent_name} analysis: {str(e)}")
            return []
    
    def _parse_response(self, response_text: str, file_path: str, changed_lines: List[int]) -> List[ReviewComment]:
        """
        Parse LLM response into structured ReviewComment objects
        
        Args:
            response_text: Raw response from LLM
            file_path: Path to the file
            changed_lines: List of changed line numbers
            
        Returns:
            List of ReviewComment objects
        """
        comments = []
        
        try:
            # Try to parse as JSON first
            if response_text.strip().startswith('{') or response_text.strip().startswith('['):
                parsed = json.loads(response_text)
                if isinstance(parsed, list):
                    for item in parsed:
                        comments.append(self._create_comment_from_dict(item, file_path))
                elif isinstance(parsed, dict) and 'comments' in parsed:
                    for item in parsed['comments']:
                        comments.append(self._create_comment_from_dict(item, file_path))
            else:
                # Fallback: parse text format
                comments = self._parse_text_response(response_text, file_path, changed_lines)
        except json.JSONDecodeError:
            # If JSON parsing fails, use text parsing
            comments = self._parse_text_response(response_text, file_path, changed_lines)
        
        return comments
    
    def _create_comment_from_dict(self, data: Dict[str, Any], file_path: str) -> ReviewComment:
        """Create a ReviewComment from a dictionary"""
        from app.models.schemas import Severity
        
        return ReviewComment(
            line_number=data.get('line_number'),
            file_path=file_path,
            category=self.category,
            severity=Severity(data.get('severity', 'medium').lower()),
            message=data.get('message', ''),
            suggestion=data.get('suggestion'),
            code_snippet=data.get('code_snippet')
        )
    
    def _parse_text_response(self, response_text: str, file_path: str, changed_lines: List[int]) -> List[ReviewComment]:
        """
        Parse text response when JSON parsing fails
        This is a fallback method
        """
        from app.models.schemas import Severity
        
        comments = []
        lines = response_text.split('\n')
        current_comment = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for severity indicators
            severity = Severity.MEDIUM
            if any(keyword in line.lower() for keyword in ['critical', 'severe', 'urgent']):
                severity = Severity.CRITICAL
            elif any(keyword in line.lower() for keyword in ['high', 'important']):
                severity = Severity.HIGH
            elif any(keyword in line.lower() for keyword in ['low', 'minor', 'suggestion']):
                severity = Severity.LOW
            elif any(keyword in line.lower() for keyword in ['info', 'note']):
                severity = Severity.INFO
            
            # Create comment if line looks like an issue
            if any(keyword in line.lower() for keyword in ['issue', 'problem', 'error', 'bug', 'concern', 'suggestion']):
                comments.append(ReviewComment(
                    line_number=changed_lines[0] if changed_lines else None,
                    file_path=file_path,
                    category=self.category,
                    severity=severity,
                    message=line,
                    suggestion=None,
                    code_snippet=None
                ))
        
        # If no structured comments found, create one general comment
        if not comments and response_text.strip():
            comments.append(ReviewComment(
                line_number=changed_lines[0] if changed_lines else None,
                file_path=file_path,
                category=self.category,
                severity=Severity.MEDIUM,
                message=response_text[:500],  # Limit message length
                suggestion=None,
                code_snippet=None
            ))
        
        return comments

