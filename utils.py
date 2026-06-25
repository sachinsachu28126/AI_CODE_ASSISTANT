import re


def get_language_extension(language):

    mapping = {
        "Python": "python",
        "Java": "java",
        "JavaScript": "javascript",
        "C++": "cpp",
        "C#": "csharp",
        "PHP": "php",
        "Go": "go"
    }

    return mapping.get(
        language,
        "text"
    )


def calculate_quality_label(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Average"

    else:
        return "Needs Improvement"


def risk_badge(risk):

    risk = risk.lower()

    if risk == "low":
        return "🟢 Low"

    elif risk == "medium":
        return "🟠 Medium"

    else:
        return "🔴 High"


def clean_code(code):

    if not code:
        return ""

    code = code.strip()

    code = re.sub(
        r"\t",
        "    ",
        code
    )

    return code


def count_lines(code):

    if not code:
        return 0

    return len(
        code.splitlines()
    )


def estimate_complexity(code):

    loops = (
        code.count("for ")
        + code.count("while ")
    )

    conditions = (
        code.count("if ")
        + code.count("elif ")
        + code.count("switch")
    )

    total = loops + conditions

    if total <= 5:
        return "Low"

    elif total <= 15:
        return "Medium"

    else:
        return "High"


def code_statistics(code):

    lines = count_lines(code)

    chars = len(code)

    words = len(
        code.split()
    )

    complexity = estimate_complexity(
        code
    )

    return {
        "lines": lines,
        "characters": chars,
        "words": words,
        "complexity": complexity
    }


def detect_language(code):

    if "def " in code:
        return "Python"

    if "public static void main" in code:
        return "Java"

    if "console.log" in code:
        return "JavaScript"

    if "#include" in code:
        return "C++"

    return "Unknown"


def security_scan(code):

    issues = []

    patterns = {
        "eval(": "Dangerous eval() usage",
        "exec(": "Dangerous exec() usage",
        "os.system(": "Command execution detected",
        "subprocess.call(": "Subprocess execution detected",
        "password=": "Hardcoded password found",
        "passwd=": "Hardcoded password found",
        "api_key=": "Hardcoded API key found",
        "token=": "Hardcoded token found"
    }

    lower_code = code.lower()

    for pattern, issue in patterns.items():

        if pattern.lower() in lower_code:
            issues.append(issue)

    return issues


def generate_summary(stats):

    return f"""
Total Lines: {stats['lines']}
Characters: {stats['characters']}
Words: {stats['words']}
Complexity: {stats['complexity']}
"""