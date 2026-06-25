import google.generativeai as genai
import json
import re


class CodeReviewer:

    def __init__(self, api_key, temperature=0.3):
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": temperature,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 8192
            }
        )

    def build_prompt(self, code, language):

        prompt = f"""
You are a Senior Software Architect, Security Analyst,
Performance Engineer, and Code Reviewer.

Analyze the following {language} source code.

Return your response in EXACT JSON format.

JSON Format:

{{
    "score": 85,
    "complexity": "Medium",
    "risk": "Low",
    "review": "Detailed review here",
    "optimized_code": "Optimized source code here"
}}

Tasks:

1. Explain purpose of code.

2. Detect:
   - Bugs
   - Runtime Errors
   - Logic Errors
   - Syntax Problems

3. Detect Security Vulnerabilities:
   - SQL Injection
   - Command Injection
   - Hardcoded Passwords
   - API Key Exposure
   - Unsafe File Access
   - XSS Risks

4. Performance Improvements:
   - Redundant Loops
   - Memory Issues
   - Slow Algorithms
   - Repeated Computations

5. Best Practices:
   - Naming
   - Readability
   - Maintainability
   - Documentation

6. Generate Optimized Code.

7. Give Overall Quality Score (0-100).

8. Complexity:
   Low / Medium / High

9. Risk:
   Low / Medium / High

IMPORTANT:
Return ONLY valid JSON.

Code:

{code}
"""
        return prompt

    def clean_json_response(self, text):

        text = text.strip()

        text = re.sub(r"^```json", "", text)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)

        return text.strip()

    def fallback_response(self, raw_response):

        return {
            "score": 70,
            "complexity": "Medium",
            "risk": "Medium",
            "review": raw_response,
            "optimized_code": "# Optimized code could not be extracted."
        }

    def review_code(self, code, language):

        prompt = self.build_prompt(
            code=code,
            language=language
        )

        response = self.model.generate_content(prompt)

        raw_text = response.text

        cleaned_text = self.clean_json_response(
            raw_text
        )

        try:

            result = json.loads(cleaned_text)

            result.setdefault("score", 70)
            result.setdefault("complexity", "Medium")
            result.setdefault("risk", "Medium")
            result.setdefault("review", "No review generated.")
            result.setdefault(
                "optimized_code",
                "# No optimized code generated."
            )

            return result

        except Exception:

            return self.fallback_response(
                raw_text
            )

    def get_quality_badge(self, score):

        if score >= 90:
            return "Excellent"

        if score >= 75:
            return "Good"

        if score >= 60:
            return "Average"

        return "Needs Improvement"

    def analyze_score(self, score):

        badge = self.get_quality_badge(score)

        return {
            "score": score,
            "badge": badge
        }

    def security_scan_keywords(self, code):

        findings = []

        dangerous_patterns = {
            "eval(": "Use of eval() detected",
            "exec(": "Use of exec() detected",
            "os.system(": "Command execution detected",
            "subprocess.call(": "Subprocess execution detected",
            "password=": "Hardcoded password detected",
            "api_key=": "Hardcoded API key detected",
            "token=": "Hardcoded token detected"
        }

        lower_code = code.lower()

        for key, value in dangerous_patterns.items():

            if key.lower() in lower_code:
                findings.append(value)

        return findings

    def calculate_complexity_estimate(self, code):

        loop_count = (
            code.count("for ")
            + code.count("while ")
        )

        condition_count = (
            code.count("if ")
            + code.count("elif ")
            + code.count("switch")
        )

        score = loop_count + condition_count

        if score <= 5:
            return "Low"

        if score <= 15:
            return "Medium"

        return "High"

    def quick_review(self, code):

        issues = []

        if "print(" in code:
            issues.append(
                "Debug print statements found."
            )

        if "todo" in code.lower():
            issues.append(
                "TODO comments found."
            )

        if len(code) > 3000:
            issues.append(
                "Large source file detected."
            )

        return issues