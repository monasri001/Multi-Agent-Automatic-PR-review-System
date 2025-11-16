"""
Diff Parser - Parses GitHub diffs and extracts changed lines
"""
from typing import List, Dict, Tuple
import re


class DiffParser:
    """Parser for GitHub diff format"""
    
    @staticmethod
    def parse_diff(diff_text: str) -> Dict[str, Dict]:
        """
        Parse a diff string into structured format
        
        Args:
            diff_text: Raw diff text
            
        Returns:
            Dictionary mapping file paths to their diff information
        """
        files = {}
        current_file = None
        current_lines = []
        
        lines = diff_text.split('\n')
        
        for line in lines:
            # Detect file header
            if line.startswith('diff --git'):
                if current_file:
                    files[current_file] = DiffParser._process_file_diff(current_lines)
                current_file = None
                current_lines = []
            elif line.startswith('---') or line.startswith('+++'):
                # Extract file path
                if line.startswith('+++'):
                    # Extract file path from +++ b/path/to/file
                    match = re.search(r'\+\+\+ b/(.+)', line)
                    if match:
                        current_file = match.group(1)
            elif current_file:
                current_lines.append(line)
        
        # Process last file
        if current_file:
            files[current_file] = DiffParser._process_file_diff(current_lines)
        
        return files
    
    @staticmethod
    def _process_file_diff(diff_lines: List[str]) -> Dict:
        """
        Process diff lines for a single file
        
        Args:
            diff_lines: List of diff lines for the file
            
        Returns:
            Dictionary with file diff information
        """
        changed_lines = []
        added_lines = []
        removed_lines = []
        current_line_num = None
        hunk_start = None
        
        for line in diff_lines:
            # Detect hunk header: @@ -start,count +start,count @@
            hunk_match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            if hunk_match:
                hunk_start = int(hunk_match.group(3))  # New file line number
                current_line_num = hunk_start - 1  # Will be incremented
                continue
            
            if current_line_num is None:
                continue
            
            # Track line changes
            if line.startswith('+') and not line.startswith('+++'):
                current_line_num += 1
                added_lines.append(current_line_num)
                changed_lines.append(current_line_num)
            elif line.startswith('-') and not line.startswith('---'):
                removed_lines.append(current_line_num)
                changed_lines.append(current_line_num)
            elif line.startswith(' '):
                current_line_num += 1
        
        return {
            'changed_lines': sorted(set(changed_lines)),
            'added_lines': sorted(set(added_lines)),
            'removed_lines': sorted(set(removed_lines)),
            'diff_content': '\n'.join(diff_lines)
        }
    
    @staticmethod
    def extract_file_diffs(diff_text: str) -> List[Tuple[str, str, List[int]]]:
        """
        Extract individual file diffs from a full diff
        
        Args:
            diff_text: Full diff text
            
        Returns:
            List of tuples: (file_path, diff_content, changed_lines)
        """
        parsed = DiffParser.parse_diff(diff_text)
        result = []
        
        for file_path, file_info in parsed.items():
            result.append((
                file_path,
                file_info['diff_content'],
                file_info['changed_lines']
            ))
        
        return result
    
    @staticmethod
    def get_changed_files(diff_text: str) -> List[str]:
        """
        Get list of changed files from diff
        
        Args:
            diff_text: Full diff text
            
        Returns:
            List of file paths
        """
        parsed = DiffParser.parse_diff(diff_text)
        return list(parsed.keys())

