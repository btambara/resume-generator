from datetime import datetime
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
        topMargin=inch/2,
        bottomMargin=inch/2,
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
            resume["person"]["location"]["city"]
            + ", "
            + resume["person"]["location"]["state"]
            + " \u2022 "
            + resume["person"]["email"],
            right_align_normal_style,
        )
    )

    story.append(
        Paragraph(
            resume["person"]["website"] + " \u2022 " + resume["person"]["github"],
            right_align_normal_style,
        )
    )

    # SUMMARY
    story.append(
        Paragraph("<b>" + resume["professional"]["title"] + "</b>", styles["Heading2"])
    )
    story.append(Paragraph(resume["professional"]["summary"], styles["BodyText"]))

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

    # Experience
    story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", styles["Heading2"]))
    experience = resume["professional"]["experience"]

    for item in experience:
        full_location = item["location"]["city"] + ", " + item["location"]["state"]

        story.append(
            Paragraph(
                "<b>" + item["company"] + "</b> - " + full_location,
                styles["BodyText"],
            )
        )
        story.append(
            Paragraph(
                "<b>"
                + item["title"]
                + "</b>"
                + " "
                + to_month_name_year(item["from"], False)
                + " to "
                + to_month_name_year(item["to"], False),
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
                + item["school"]["state"]
                + " "
                + to_month_name_year(item["from"], True)
                + " to "
                + to_month_name_year(item["to"], True),
                styles["BodyText"],
            )
        )

    doc.build(story)
    print(f"Resume generated: {filename}")


def to_month_name_year(yyyymmdd, just_year):
    if yyyymmdd == "PRESENT":
        return "Present"

    if len(yyyymmdd) == 8:
        date_obj = datetime.strptime(yyyymmdd, "%Y%m%d")
        if just_year:
            return date_obj.strftime("%Y")
        else:
            return date_obj.strftime("%B, %Y")


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
