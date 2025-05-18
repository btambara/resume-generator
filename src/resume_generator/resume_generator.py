import json
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_resume(filename):
    doc = SimpleDocTemplate(filename, pagesize=LETTER,
                            rightMargin=0.62, leftMargin=0.62,
                            topMargin=0.62, bottomMargin=0.62)
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph("<b>John Doe</b>", styles['Title']))
    story.append(Paragraph("Email: johndoe@example.com | Phone: (123) 456-7890 | GitHub: github.com/johndoe", styles['Normal']))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("<b>Professional Summary</b>", styles['Heading2']))
    summary = (
        "Results-driven software engineer with 5+ years of experience in developing robust code "
        "for high-volume businesses. Skilled in Python, JavaScript, and modern frameworks. "
        "Proven ability to lead teams and deliver results on time."
    )
    story.append(Paragraph(summary, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("<b>Work Experience</b>", styles['Heading2']))
    experience = (
        "<b>Senior Software Engineer</b> — TechCorp Inc. (2021–Present)<br/>"
        "• Led a team of 5 in designing scalable web applications using Django and React.<br/>"
        "• Reduced server load by 30% through backend optimizations.<br/><br/>"
        "<b>Software Engineer</b> — CodeWorks LLC (2018–2021)<br/>"
        "• Developed and maintained internal tools in Python.<br/>"
        "• Improved test coverage by 50% and reduced bug rates by 25%."
    )
    story.append(Paragraph(experience, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Education
    story.append(Paragraph("<b>Education</b>", styles['Heading2']))
    education = (
        "<b>B.Sc. in Computer Science</b><br/>"
        "University of Example — 2014–2018"
    )
    story.append(Paragraph(education, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Skills
    story.append(Paragraph("<b>Skills</b>", styles['Heading2']))
    skills = "Python, JavaScript, Django, React, Git, Docker, SQL, REST APIs"
    story.append(Paragraph(skills, styles['BodyText']))

    doc.build(story)
    print(f"Resume generated: {filename}")

def main():
    with open("resources/resume.json", "r") as file:
        data = json.load(file)
        file_name = data["person"]["name"]["first"] + "_" + data["person"]["name"]["last"] + "_Resume"
        filename = file_name + ".pdf"
        create_resume(filename)

if __name__ == "__main__":
    main()
