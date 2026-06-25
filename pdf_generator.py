from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors

from io import BytesIO


def create_pdf_report(report_text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    content.append(
        Paragraph(
            "AI Code Review Report",
            title_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    sections = report_text.split("\n")

    for line in sections:

        line = line.strip()

        if not line:
            continue

        if (
            "BUG" in line.upper()
            or "SECURITY" in line.upper()
            or "PERFORMANCE" in line.upper()
            or "BEST PRACTICES" in line.upper()
            or "OPTIMIZED" in line.upper()
            or "QUALITY" in line.upper()
        ):

            content.append(
                Paragraph(
                    line,
                    heading_style
                )
            )

        else:

            content.append(
                Paragraph(
                    line,
                    body_style
                )
            )

        content.append(
            Spacer(1, 5)
        )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


def create_detailed_pdf(
    language,
    score,
    complexity,
    risk,
    review,
    optimized_code
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Advanced AI Code Review Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    summary = f"""
    <b>Language:</b> {language}<br/>
    <b>Quality Score:</b> {score}/100<br/>
    <b>Complexity:</b> {complexity}<br/>
    <b>Risk Level:</b> {risk}
    """

    content.append(
        Paragraph(
            summary,
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            "Review Findings",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            review.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    content.append(
        PageBreak()
    )

    content.append(
        Paragraph(
            "Optimized Code",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            optimized_code.replace("\n", "<br/>"),
            styles["Code"] if "Code" in styles else styles["BodyText"]
        )
    )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf