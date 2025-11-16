"""
Streamlit UI for PR Review Agent
"""
import streamlit as st
import requests
import json
from typing import Dict, Any

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="PR Review Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Automated GitHub Pull Request Review Agent")
st.markdown("Analyze code changes and get comprehensive review comments")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    review_mode = st.radio(
        "Review Mode",
        ["GitHub PR URL", "Manual Diff Input"],
        help="Choose how to provide code changes for review"
    )
    
    st.subheader("Agent Selection")
    enable_logic = st.checkbox("Logic Agent", value=True, help="Identifies logical errors and bugs")
    enable_readability = st.checkbox("Readability Agent", value=True, help="Identifies code readability issues")
    enable_performance = st.checkbox("Performance Agent", value=True, help="Identifies performance issues")
    enable_security = st.checkbox("Security Agent", value=True, help="Identifies security vulnerabilities")
    
    use_async = st.checkbox("Use Async Processing", value=False, help="Faster processing for large PRs")

# Main content area
if review_mode == "GitHub PR URL":
    st.subheader("📝 Enter GitHub Pull Request URL")
    pr_url = st.text_input(
        "PR URL",
        placeholder="https://github.com/owner/repo/pull/123",
        help="Enter the full URL of the GitHub Pull Request"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        review_button = st.button("🔍 Review PR", type="primary", use_container_width=True)
    
    if review_button and pr_url:
        with st.spinner("Fetching PR and performing review..."):
            try:
                endpoint = f"{API_URL}/review/async" if use_async else f"{API_URL}/review"
                
                payload = {
                    "pr_url": pr_url,
                    "enable_agents": {
                        "logic": enable_logic,
                        "readability": enable_readability,
                        "performance": enable_performance,
                        "security": enable_security
                    }
                }
                
                response = requests.post(endpoint, json=payload, timeout=300)
                response.raise_for_status()
                
                review_data = response.json()
                st.session_state['review_data'] = review_data
                st.success("Review completed!")
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        st.error(f"Details: {error_detail.get('detail', 'Unknown error')}")
                    except:
                        st.error(f"Status: {e.response.status_code}")

else:
    st.subheader("📝 Enter Diff Manually")
    
    file_path = st.text_input(
        "File Path (optional)",
        placeholder="src/main.py",
        help="Path to the file being reviewed"
    )
    
    diff_text = st.text_area(
        "Diff Text",
        height=300,
        placeholder="""--- a/src/main.py
+++ b/src/main.py
@@ -10,6 +10,7 @@ def process_user(user):
     if user is None:
         return None
+    user.name = user.name.strip()
     return user""",
        help="Paste the diff text here"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        review_button = st.button("🔍 Review Diff", type="primary", use_container_width=True)
    
    if review_button and diff_text:
        with st.spinner("Performing review..."):
            try:
                endpoint = f"{API_URL}/review/async" if use_async else f"{API_URL}/review"
                
                payload = {
                    "diff_text": diff_text,
                    "file_path": file_path if file_path else None,
                    "enable_agents": {
                        "logic": enable_logic,
                        "readability": enable_readability,
                        "performance": enable_performance,
                        "security": enable_security
                    }
                }
                
                response = requests.post(endpoint, json=payload, timeout=300)
                response.raise_for_status()
                
                review_data = response.json()
                st.session_state['review_data'] = review_data
                st.success("Review completed!")
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        st.error(f"Details: {error_detail.get('detail', 'Unknown error')}")
                    except:
                        st.error(f"Status: {e.response.status_code}")

# Display review results
if 'review_data' in st.session_state:
    review_data = st.session_state['review_data']
    
    st.divider()
    st.header("📊 Review Results")
    
    # Summary section
    summary = review_data.get('summary', {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Comments", summary.get('total_comments', 0))
    with col2:
        st.metric("🔴 Critical", summary.get('critical_issues', 0))
    with col3:
        st.metric("🟠 High", summary.get('high_issues', 0))
    with col4:
        st.metric("🟡 Medium", summary.get('medium_issues', 0))
    with col5:
        st.metric("🟢 Low", summary.get('low_issues', 0))
    
    # Agent reports
    agent_reports = review_data.get('agent_reports', {})
    if agent_reports:
        st.subheader("🤖 Agent Reports")
        agent_cols = st.columns(len(agent_reports))
        for idx, (agent_name, report) in enumerate(agent_reports.items()):
            with agent_cols[idx]:
                st.metric(
                    agent_name.replace('Agent', '').title(),
                    report.get('total_comments', 0),
                    help=f"Reviewed {report.get('files_reviewed', 0)} files"
                )
    
    # Comments section
    comments = review_data.get('comments', [])
    
    if comments:
        st.subheader("💬 Review Comments")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            severity_filter = st.multiselect(
                "Filter by Severity",
                ["critical", "high", "medium", "low", "info"],
                default=["critical", "high", "medium", "low", "info"]
            )
        with col2:
            category_filter = st.multiselect(
                "Filter by Category",
                ["logic", "readability", "performance", "security"],
                default=["logic", "readability", "performance", "security"]
            )
        
        # Filter comments
        filtered_comments = [
            c for c in comments
            if c.get('severity', '').lower() in [s.lower() for s in severity_filter]
            and c.get('category', '').lower() in [cat.lower() for cat in category_filter]
        ]
        
        # Group by file
        files_dict = {}
        for comment in filtered_comments:
            file_path = comment.get('file_path', 'Unknown')
            if file_path not in files_dict:
                files_dict[file_path] = []
            files_dict[file_path].append(comment)
        
        # Display comments grouped by file
        for file_path, file_comments in files_dict.items():
            with st.expander(f"📄 {file_path} ({len(file_comments)} comments)", expanded=True):
                for comment in file_comments:
                    severity = comment.get('severity', 'medium').upper()
                    category = comment.get('category', 'unknown').title()
                    line_num = comment.get('line_number')
                    
                    # Color coding based on severity
                    if severity == "CRITICAL":
                        st.error(f"🔴 **{severity}** - {category}")
                    elif severity == "HIGH":
                        st.warning(f"🟠 **{severity}** - {category}")
                    elif severity == "MEDIUM":
                        st.info(f"🟡 **{severity}** - {category}")
                    else:
                        st.success(f"🟢 **{severity}** - {category}")
                    
                    if line_num:
                        st.caption(f"Line {line_num}")
                    
                    st.write(comment.get('message', ''))
                    
                    if comment.get('suggestion'):
                        with st.expander("💡 Suggestion"):
                            st.code(comment.get('suggestion'), language='python')
                    
                    if comment.get('code_snippet'):
                        with st.expander("📝 Code Snippet"):
                            st.code(comment.get('code_snippet'), language='python')
                    
                    st.divider()
    else:
        st.info("✅ No issues found! Great job!")
    
    # Download results
    st.download_button(
        label="📥 Download Review Results (JSON)",
        data=json.dumps(review_data, indent=2),
        file_name="pr_review_results.json",
        mime="application/json"
    )

# Footer
st.divider()
st.caption("Powered by Multi-Agent PR Review System | Built with FastAPI, LangChain, and Streamlit")

