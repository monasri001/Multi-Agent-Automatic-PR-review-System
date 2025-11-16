"""
GitHub Service - Interacts with GitHub API to fetch PR information
"""
import requests
from typing import Optional, Dict, Any, List
from app.config import settings
from app.services.diff_parser import DiffParser


class GitHubService:
    """Service for interacting with GitHub API"""
    
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.base_url = settings.GITHUB_API_URL
        self.headers = {
            "Accept": "application/vnd.github.v3.diff",
            "Authorization": f"token {self.token}" if self.token else None
        }
        # Remove None values from headers
        self.headers = {k: v for k, v in self.headers.items() if v is not None}
    
    def parse_pr_url(self, pr_url: str) -> Dict[str, str]:
        """
        Parse GitHub PR URL to extract owner, repo, and PR number
        
        Args:
            pr_url: GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)
            
        Returns:
            Dictionary with owner, repo, and pr_number
        """
        # Handle different URL formats
        patterns = [
            r'github\.com/([^/]+)/([^/]+)/pull/(\d+)',
            r'github\.com/([^/]+)/([^/]+)/pull/(\d+)',
        ]
        
        import re
        for pattern in patterns:
            match = re.search(pattern, pr_url)
            if match:
                return {
                    'owner': match.group(1),
                    'repo': match.group(2),
                    'pr_number': int(match.group(3))
                }
        
        raise ValueError(f"Invalid PR URL format: {pr_url}")
    
    def get_pr_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """
        Fetch PR diff from GitHub API
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            Diff text as string
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        
        headers = {
            "Accept": "application/vnd.github.v3.diff",
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch PR diff: {str(e)}")
    
    def get_pr_info(self, owner: str, repo: str, pr_number: int) -> Dict[str, Any]:
        """
        Get PR information (title, description, etc.)
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            PR information dictionary
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch PR info: {str(e)}")
    
    def get_pr_files(self, owner: str, repo: str, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get list of files changed in PR
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            List of file information dictionaries
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch PR files: {str(e)}")
    
    def fetch_pr_for_review(self, pr_url: Optional[str] = None, 
                           owner: Optional[str] = None,
                           repo: Optional[str] = None,
                           pr_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch PR data for review
        
        Args:
            pr_url: GitHub PR URL (alternative to owner/repo/pr_number)
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            Dictionary with diff_text and metadata
        """
        # Parse PR URL if provided
        if pr_url:
            parsed = self.parse_pr_url(pr_url)
            owner = parsed['owner']
            repo = parsed['repo']
            pr_number = parsed['pr_number']
        
        if not all([owner, repo, pr_number]):
            raise ValueError("Must provide either pr_url or all of owner, repo, pr_number")
        
        # Fetch diff
        diff_text = self.get_pr_diff(owner, repo, pr_number)
        
        # Fetch PR info
        pr_info = self.get_pr_info(owner, repo, pr_number)
        
        return {
            'diff_text': diff_text,
            'pr_url': pr_info.get('html_url'),
            'title': pr_info.get('title'),
            'description': pr_info.get('body'),
            'owner': owner,
            'repo': repo,
            'pr_number': pr_number
        }

