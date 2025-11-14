import streamlit as st
import json
from logicagent import LogicAgent   # Make sure logicagent.py is in the project root

st.set_page_config(
    page_title="Logic Review Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
#   SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Configuration")
st.sidebar.subheader("Agent Selection")

enable_logic = st.sidebar.checkbox("Logic Agent", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("Built using **LangChain + Streamlit** ❤️")


# ----------------------------
#   MAIN TITLE
# ----------------------------
st.markdown("""
<h1 style='text-align: center; color: #84b6f4;'>🧠 Automated Logic Review Agent</h1>
<p style='text-align: center; color: #999;'>Analyze code diffs and detect logical issues instantly.</p>
""", unsafe_allow_html=True)

st.markdown("---")


# ----------------------------
#   DIFF INPUT SECTION
# ----------------------------
st.subheader("📝 Enter Diff Manually")

diff_input = st.text_area(
    "Paste Unified Diff Below",
    height=300,
    placeholder="Example:\n--- a/app.py\n+++ b/app.py\n@@ -1,4 +1,7 @@\n def add(a, b):\n-    return a + b\n+    if a > 10:\n+        return b\n+    return a + b + 1"
)

run_button = st.button("🔍 Review Diff", type="primary")


# ----------------------------
#   PROCESS INPUT
# ----------------------------
results = []
if run_button:
    if not diff_input.strip():
        st.error("❌ Please paste a valid diff text!")
    else:
        with st.spinner("Analyzing code with Logic Agent..."):
            agent = LogicAgent()
            response = agent.analyze(diff_input)

            try:
                results = json.loads(response)
            except:
                st.error("⚠️ LLM returned invalid JSON. Showing raw output.")
                st.code(response, language="json")
                results = []

        st.markdown("---")
        st.subheader("📊 Review Results")

        if not results:
            st.success("🎉 No issues found! Great job!")
        else:
            # ----------------------------
            # Metrics Summary
            # ----------------------------
            severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

            for item in results:
                sev = item.get("severity", "low").lower()
                if sev in severity_counts:
                    severity_counts[sev] += 1

            total = sum(severity_counts.values())

            cols = st.columns(5)
            cols[0].metric("📝 Total Issues", total)
            cols[1].metric("🔥 Critical", severity_counts["critical"])
            cols[2].metric("⚠ High", severity_counts["high"])
            cols[3].metric("🟡 Medium", severity_counts["medium"])
            cols[4].metric("🟢 Low", severity_counts["low"])

            st.markdown("---")
            st.subheader("🧠 Logic Agent Report")

            # Display issues in UI
            for issue in results:
                with st.container():
                    st.markdown(f"""
                    ### 🧩 File: `{issue.get('file', 'unknown')}`  
                    **Line:** {issue.get('line', 0)}  
                    **Issue:** {issue.get('issue', '').strip()}  
                    **Details:** {issue.get('details', '').strip()}  
                    **Suggestion:** {issue.get('suggestion', '').strip()}
                    """)

                    st.markdown("---")


# ----------------------------
#   FOOTER
# ----------------------------
st.markdown("""
<br><br>
<p style='text-align: center; font-size: 14px; color: #777;'>
Powered by <b>Logic Review Agent</b> — LangChain + Streamlit
</p>
""", unsafe_allow_html=True)
