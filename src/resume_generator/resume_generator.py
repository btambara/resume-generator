from datetime import datetime
from pathlib import Path
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
    KeepTogether
)
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib import colors


def create_resume(filename, resume):
    title = (
        resume["person"]["name"]["first"]
        + " "
        + resume["person"]["name"]["last"]
        + "'s Resume"
    )
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=LETTER,
        rightMargin=inch / 2,
        leftMargin=inch / 2,
        topMargin=inch / 2,
        bottomMargin=inch / 2,
        title=title,
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

    # Experience
    story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", styles["Heading2"]))
    experience = resume["professional"]["experience"]

    for index, item in enumerate(experience):
        experience_flowables = []

        full_location = item["location"]["city"] + ", " + item["location"]["state"]
        company = Paragraph(
            "<b>" + item["company"] + "</b>",
            left_align_normal_style
        )
        left_text = Paragraph(
            "<b>"
            + item["title"]
            + "</b>"
            + " - "
            + full_location,
            left_align_normal_style,
        )
        right_text = Paragraph(
            to_month_name_year(item["from"], False)
            + " to "
            + to_month_name_year(item["to"], False),
            right_align_normal_style,
        )

        table = Table([[company], [left_text, right_text]], colWidths=[None, 150])
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
        experience_flowables.append(table)

        experience_flowables.append(
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
            start="\u27a4",
        )

        experience_flowables.append(bullet_list)

        # Technical Environment: 
        experience_flowables.append(Spacer(1, 8))

        technical_environment = item["technicalEnvironment"]

        technologies = []

        for items in technical_environment.values():
            for item in items:
                tech = item["name"]

                if "version" in item:
                    versions = ", ".join(str(v["release"]) for v in item["version"])
                    tech += f" ({versions})"

                technologies.append(tech)

        experience_flowables.append(
            Paragraph(
                f"<b>Technical Environment:</b> {', '.join(technologies)}",
                left_align_normal_style
            )
        )

        if index != (len(experience) - 1):
            experience_flowables.append(Spacer(1, 12))
        
        story.append(KeepTogether(experience_flowables))
        
    # Education
    education_flowables = []
    education_flowables.append(Paragraph("<b>EDUCATION</b>", styles["Heading2"]))
    for index, item in enumerate(resume["education"]):
        full_location = item["school"]["city"] + ", " + item["school"]["state"]
        left_text = Paragraph(
            "<b>"
            + item["degree"]
            + "</b>"
            + " - "
            + item["school"]["name"]
            + " - "
            + full_location,
            left_align_normal_style,
        )
        right_text = Paragraph(
            to_month_name_year(item["from"], True)
            + " to "
            + to_month_name_year(item["to"], True),
            right_align_normal_style,
        )

        table = Table([[left_text, right_text]], colWidths=[None, 150])
        table.setStyle([("ALIGN", (1, 0), (1, 0), "RIGHT")])

        # story.append(
        #     Paragraph(
        #         "<b>"
        #         + item["degree"]
        #         + "</b> - "
        #         + item["school"]["name"]
        #         + " - "
        #         + item["school"]["city"]
        #         + ", "
        #         + item["school"]["state"]
        #         + " "
        #         + to_month_name_year(item["from"], True)
        #         + " to "
        #         + to_month_name_year(item["to"], True),
        #         styles["BodyText"],
        #     )
        # )

        table.setStyle(style)
        education_flowables.append(table)

        if index != (len(resume["education"]) - 1):
            education_flowables.append(Spacer(1, 12))

    story.append(KeepTogether(education_flowables))

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
    with open("resources/brian-tambara-resume/resume.json", "r") as file:
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        data = json.load(file)
        file_name = (
            "Resume_"
            + data["person"]["name"]["first"]
            + "_"
            + data["person"]["name"]["last"]
        )
        filename = output_dir / (file_name + ".pdf")
        create_resume(filename, data)


if __name__ == "__main__":
    main()
