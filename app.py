import os
import streamlit as st
from code_reviewer import CodeReviewer
from pdf_generator import create_pdf_report
from utils import get_language_extension
import datetime

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="💻",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main {
    padding: 1rem;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
}
.review-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.title("💻 AI Code Review Assistant")
st.markdown(
    """
Analyze source code using Gemini AI.

### Features
- Bug Detection
- Security Analysis
- Code Quality Score
- Complexity Analysis
- Best Practices
- Performance Optimization
- Optimized Code Generation
- PDF Report Download
"""
)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Programming Language",
    [
        "Python",
        "Java",
        "JavaScript",
        "C++",
        "C#",
        "PHP",
        "Go"
    ]
)

temperature = st.sidebar.slider(
    "AI Creativity",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1
)

show_code = st.sidebar.checkbox(
    "Show Original Code",
    value=True
)

# ----------------------------
# API Key
# ----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password"
    )

# ----------------------------
# Code Input
# ----------------------------
st.subheader("Paste Source Code")

sample_code = """
def divide(a,b):
    return a/b

print(divide(10,0))
"""

code = st.text_area(
    "Source Code",
    value="",
    height=350,
    placeholder=sample_code
)

# ----------------------------
# Show Code
# ----------------------------
if show_code and code:
    st.subheader("Original Code")

    ext = get_language_extension(language)

    st.code(
        code,
        language=ext
    )

# ----------------------------
# Review Button
# ----------------------------
review_clicked = st.button(
    "🚀 Review Code"
)

# ----------------------------
# Review Process
# ----------------------------
if review_clicked:

    if not api_key:
        st.error("Please provide Gemini API Key")
        st.stop()

    if not code.strip():
        st.error("Please paste source code")
        st.stop()

    reviewer = CodeReviewer(
        api_key=api_key,
        temperature=temperature
    )

    with st.spinner("Analyzing code..."):

        try:

            result = reviewer.review_code(
                code=code,
                language=language
            )

            st.success("Analysis Completed")

            # ----------------------------
            # Tabs
            # ----------------------------
            tab1, tab2, tab3 = st.tabs(
                [
                    "📊 Review Report",
                    "⚡ Optimized Code",
                    "📄 Export"
                ]
            )

            # ----------------------------
            # Report Tab
            # ----------------------------
            with tab1:

                st.markdown(result["review"])

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Quality Score",
                        f'{result["score"]}/100'
                    )

                with col2:
                    st.metric(
                        "Complexity",
                        result["complexity"]
                    )

                with col3:
                    st.metric(
                        "Risk Level",
                        result["risk"]
                    )

            # ----------------------------
            # Optimized Code
            # ----------------------------
            with tab2:

                st.subheader("Optimized Version")

                st.code(
                    result["optimized_code"],
                    language=get_language_extension(language)
                )

                st.download_button(
                    label="⬇ Download Optimized Code",
                    data=result["optimized_code"],
                    file_name=f"optimized_code.{get_language_extension(language)}",
                    mime="text/plain"
                )

            # ----------------------------
            # Export
            # ----------------------------
            with tab3:

                report_text = f"""
AI CODE REVIEW REPORT

Date:
{datetime.datetime.now()}

Language:
{language}

Score:
{result['score']}

Complexity:
{result['complexity']}

Risk:
{result['risk']}

--------------------------------

{result['review']}
"""

                pdf_data = create_pdf_report(
                    report_text
                )

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_data,
                    file_name="AI_Code_Review_Report.pdf",
                    mime="application/pdf"
                )

                st.download_button(
                    label="📝 Download Text Report",
                    data=report_text,
                    file_name="AI_Code_Review_Report.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")

st.caption(
    "AI Code Review Assistant | Streamlit + Gemini AI"
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API Key not found.")
    st.stop()