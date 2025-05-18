import json
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT


def create_resume(filename, resume):
    test = 32
    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )
    styles = getSampleStyleSheet()
    story = []
    right_align_normal_style = ParagraphStyle(
        name="RightAlign", parent=styles["Normal"], alignment=TA_RIGHT
    )
    right_align_title_style = ParagraphStyle(
        name="RightAlign", parent=styles["Title"], alignment=TA_RIGHT
    )

    # HEADER
    story.append(
        Paragraph(
            "<b>"
            + resume["person"]["name"]["first"]
            + " "
            + resume["person"]["name"]["last"]
            + "</b>",
            right_align_title_style,
        )
    )
    story.append(
        Paragraph(
            resume["person"]["website"] + " \u2022 " + resume["person"]["github"],
            right_align_normal_style,
        )
    )
    story.append(
        Paragraph(
            resume["person"]["location"]["city"]
            + ", "
            + resume["person"]["location"]["state"]
            + " \u2022 "
            + resume["person"]["website"],
            right_align_normal_style,
        )
    )
    story.append(Spacer(1, 12))

    # SUMMARY
    story.append(
        Paragraph("<b>" + resume["professional"]["title"] + "</b>", styles["Heading2"])
    )
    story.append(Paragraph(resume["professional"]["summary"], styles["BodyText"]))
    story.append(Spacer(1, 12))

    # PROFESSIONAL PROFILE
    story.append(Paragraph("PROFESSIONAL PROFILE", styles["Heading2"]))
    for profile in resume["professional"]["profile"]:
        story.append(
            Paragraph(
                "<b>" + profile["title"] + "</b>" + " - " + profile["summary"],
                styles["BodyText"],
            )
        )
    story.append(Spacer(1, 12))

    # COMPETENCIES and TECHNICAL SKILLS
    story.append(Paragraph("COMPETENCIES and TECHNICAL SKILLS", styles["Heading2"]))
    skills = ", ".join(item["name"] for item in resume["professional"]["skill"]["core"])
    story.append(
        Paragraph(
            "<b>Core Competencies: </b>" + skills,
            styles["BodyText"],
        )
    )

    languages = []
    for item in resume["professional"]["skill"]["progamming"]:
        name = item["name"]
        versions = ",".join(v["version"] for v in item["versions"])
        languages.append(f"{name} ({versions})")
    story.append(
        Paragraph(
            "<b>Programming Languages: </b>" + ", ".join(languages),
            styles["BodyText"],
        )
    )

    skills = ", ".join(
        skill["name"] for skill in resume["professional"]["skill"]["framework"]
    )
    story.append(
        Paragraph(
            "<b>Frameworks: </b>" + skills,
            styles["BodyText"],
        )
    )

    skills = ", ".join(
        skill["name"] for skill in resume["professional"]["skill"]["application"]
    )
    story.append(
        Paragraph(
            "<b>Applications: </b>" + skills,
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", styles["Heading2"]))
    for item in resume["professional"]["experience"]:
        full_location = item["location"]["city"] + ", " + item["location"]["state"]
        story.append(
            Paragraph(
                "<b>" + item["company"] + "</b> - " + full_location,
                styles["BodyText"],
            )
        )
        story.append(
            Paragraph(
                "<b>" + item["title"] + "</b>",
                styles["BodyText"],
            )
        )
        story.append(
            Paragraph(
                item["summary"],
                styles["BodyText"],
            )
        )
        for another in item["profile"]:
            story.append(
                Paragraph(
                    another["summary"],
                    styles["BodyText"],
                )
            )
    story.append(Spacer(1, 12))

    # Education
    story.append(Paragraph("<b>EDUCATION</b>", styles["Heading2"]))
    for item in resume["education"]:
        story.append(
            Paragraph(
                "<b>"
                + item["degree"]
                + "</b> - "
                + item["school"]["name"]
                + " - "
                + item["school"]["city"]
                + ", "
                + item["school"]["state"],
                styles["BodyText"],
            )
        )
    story.append(Spacer(1, 12))

    doc.build(story)
    print(f"Resume generated: {filename}")


def main():
    with open("resources/resume.json", "r") as file:
        data = json.load(file)
        file_name = (
            data["person"]["name"]["first"]
            + "_"
            + data["person"]["name"]["last"]
            + "_Resume"
        )
        filename = file_name + ".pdf"
        create_resume(filename, data)


if __name__ == "__main__":
    main()
