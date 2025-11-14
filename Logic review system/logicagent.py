import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class LogicAgent:
    def __init__(self):

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),,
            model_name="llama-3.1-8b-instant",
            temperature=0.2
        )

        self.prompt = ChatPromptTemplate.from_template("""
You are a professional code review AI focusing ONLY on LOGIC ERRORS.

Analyze the following code DIFF and identify:
- Incorrect conditions
- Wrong calculations
- Missing return statements
- Edge cases not handled
- Potential runtime errors
- Any logical mistakes introduced in the diff

### RULES
1. Return only JSON.
2. No explanation outside JSON.
3. Only report logic issues.

### OUTPUT FORMAT:
[
  {{
    "file": "<file_path>",
    "line": <line_number>,
    "issue": "<short summary>",
    "details": "<explain the logic bug>",
    "suggestion": "<how to fix it>"
  }}
]

### DIFF:
{diff}
""")

    def analyze(self, diff: str):
        messages = self.prompt.format_messages(diff=diff)
        response = self.llm.invoke(messages)
        return response.content


if __name__ == "__main__":
    agent = LogicAgent()

    sample_diff = """
--- a/app.py
+++ b/app.py
@@ -1,4 +1,7 @@
 def add(a, b):
-    return a + b
+    if a > 10:
+        return b   # logic bug: wrong return
+    return a + b + 1
"""

    print(agent.analyze(sample_diff))
