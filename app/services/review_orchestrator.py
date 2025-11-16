"""
Review Orchestrator - Coordinates multiple agents for comprehensive review
"""
from typing import List, Dict, Any, Optional
from app.agents.logic_agent import LogicAgent
from app.agents.readability_agent import ReadabilityAgent
from app.agents.performance_agent import PerformanceAgent
from app.agents.security_agent import SecurityAgent
from app.models.schemas import ReviewComment, ReviewSummary, ReviewResponse, ReviewCategory, Severity
from app.services.diff_parser import DiffParser
import asyncio
from concurrent.futures import ThreadPoolExecutor


class ReviewOrchestrator:
    """Orchestrates multiple review agents"""
    
    def __init__(self):
        self.agents = {
            'logic': LogicAgent(),
            'readability': ReadabilityAgent(),
            'performance': PerformanceAgent(),
            'security': SecurityAgent()
        }
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def review_pr(self, diff_text: str, pr_url: Optional[str] = None,
                  enable_agents: Optional[Dict[str, bool]] = None) -> ReviewResponse:
        """
        Perform comprehensive review using all agents
        
        Args:
            diff_text: Diff text to review
            pr_url: Optional PR URL for reference
            enable_agents: Dictionary to enable/disable specific agents
            
        Returns:
            ReviewResponse with all comments and summary
        """
        if enable_agents is None:
            enable_agents = {
                'logic': True,
                'readability': True,
                'performance': True,
                'security': True
            }
        
        # Parse diff to get file-level changes
        file_diffs = DiffParser.extract_file_diffs(diff_text)
        
        all_comments = []
        agent_reports = {}
        
        # Review each file with enabled agents
        for file_path, file_diff, changed_lines in file_diffs:
            file_comments = []
            
            # Run each enabled agent
            for agent_name, agent in self.agents.items():
                if not enable_agents.get(agent_name, True):
                    continue
                
                try:
                    comments = agent.analyze(file_diff, file_path, changed_lines)
                    file_comments.extend(comments)
                    
                    # Track agent-specific reports
                    if agent_name not in agent_reports:
                        agent_reports[agent_name] = {
                            'total_comments': 0,
                            'files_reviewed': 0
                        }
                    agent_reports[agent_name]['total_comments'] += len(comments)
                    agent_reports[agent_name]['files_reviewed'] += 1
                except Exception as e:
                    print(f"Error in {agent_name} for {file_path}: {str(e)}")
            
            all_comments.extend(file_comments)
        
        # Generate summary
        summary = self._generate_summary(all_comments)
        
        return ReviewResponse(
            pr_url=pr_url,
            comments=all_comments,
            summary=summary,
            agent_reports=agent_reports
        )
    
    def _generate_summary(self, comments: List[ReviewComment]) -> ReviewSummary:
        """Generate summary statistics from comments"""
        total = len(comments)
        critical = sum(1 for c in comments if c.severity == Severity.CRITICAL)
        high = sum(1 for c in comments if c.severity == Severity.HIGH)
        medium = sum(1 for c in comments if c.severity == Severity.MEDIUM)
        low = sum(1 for c in comments if c.severity == Severity.LOW)
        
        categories = {}
        for comment in comments:
            cat = comment.category.value
            categories[cat] = categories.get(cat, 0) + 1
        
        return ReviewSummary(
            total_comments=total,
            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,
            categories=categories
        )
    
    async def review_pr_async(self, diff_text: str, pr_url: Optional[str] = None,
                              enable_agents: Optional[Dict[str, bool]] = None) -> ReviewResponse:
        """
        Async version of review_pr for better performance
        
        Args:
            diff_text: Diff text to review
            pr_url: Optional PR URL for reference
            enable_agents: Dictionary to enable/disable specific agents
            
        Returns:
            ReviewResponse with all comments and summary
        """
        if enable_agents is None:
            enable_agents = {
                'logic': True,
                'readability': True,
                'performance': True,
                'security': True
            }
        
        # Parse diff to get file-level changes
        file_diffs = DiffParser.extract_file_diffs(diff_text)
        
        all_comments = []
        agent_reports = {}
        
        # Review each file with enabled agents (async)
        tasks = []
        for file_path, file_diff, changed_lines in file_diffs:
            for agent_name, agent in self.agents.items():
                if not enable_agents.get(agent_name, True):
                    continue
                
                task = self._analyze_file_async(agent, agent_name, file_diff, file_path, changed_lines)
                tasks.append((agent_name, task))
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # Process results
        for i, (agent_name, _) in enumerate(tasks):
            result = results[i]
            if isinstance(result, Exception):
                print(f"Error in {agent_name}: {str(result)}")
                continue
            
            comments, file_path = result
            all_comments.extend(comments)
            
            if agent_name not in agent_reports:
                agent_reports[agent_name] = {
                    'total_comments': 0,
                    'files_reviewed': 0
                }
            agent_reports[agent_name]['total_comments'] += len(comments)
            agent_reports[agent_name]['files_reviewed'] += 1
        
        # Generate summary
        summary = self._generate_summary(all_comments)
        
        return ReviewResponse(
            pr_url=pr_url,
            comments=all_comments,
            summary=summary,
            agent_reports=agent_reports
        )
    
    async def _analyze_file_async(self, agent, agent_name: str, file_diff: str, 
                                  file_path: str, changed_lines: List[int]):
        """Async wrapper for agent analysis"""
        loop = asyncio.get_event_loop()
        comments = await loop.run_in_executor(
            self.executor,
            agent.analyze,
            file_diff,
            file_path,
            changed_lines
        )
        return (comments, file_path)

