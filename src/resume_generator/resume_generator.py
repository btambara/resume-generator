from datetime import datetime
import json
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    ListFlowable,
    ListItem,
    Table,
    TableStyle,
    Spacer,
)
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib import colors


def create_resume(filename, resume):
    test = 32
    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch / 2,
    )
    styles = getSampleStyleSheet()
    story = []
    left_align_normal_style = ParagraphStyle(
        name="LeftAlign", parent=styles["Normal"], alignment=TA_LEFT
    )
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

    for index, item in enumerate(experience):
        full_location = item["location"]["city"] + ", " + item["location"]["state"]
        left_text = Paragraph(
            "<b>" + item["title"] + "</b>" + " " + full_location,
            left_align_normal_style,
        )
        right_text = Paragraph(
            to_month_name_year(item["from"], False)
            + " to "
            + to_month_name_year(item["to"], False),
            right_align_normal_style,
        )

        table = Table([[left_text, right_text]], colWidths=[None, 150])
        table.setStyle([("ALIGN", (1, 0), (1, 0), "RIGHT")])

        style = TableStyle(
            [
                # DEBUG TO SEE THE TABLE
                # (
                #     "BACKGROUND",
                #     (0, 0),
                #     (-1, -1),
                #     colors.yellow,
                # ),  # from top-left (0,0) to bottom-right (-1,-1)
                # (
                #     "GRID",
                #     (0, 0),
                #     (-1, -1),
                #     1,
                #     colors.black,
                # ),  # optional: add a grid for visibility
                # Remove padding
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )

        table.setStyle(style)
        story.append(table)

        story.append(
            Paragraph(
                item["summary"],
                styles["BodyText"],
            )
        )

        bullet_list = ListFlowable(
            [
                ListItem(Paragraph(text["summary"], styles["BodyText"]))
                for text in item["profile"]
            ],
            bulletType="bullet",
            start="-",
        )

        story.append(bullet_list)

        if index != (len(experience) - 1):
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
            return date_obj.strftime("%b %Y")


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
