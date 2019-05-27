import re

from urllib.request import urlopen
from collections import namedtuple

from bs4 import BeautifulSoup

Subject = namedtuple("Subject", ["abbrev", "full", "path"])

BLANK_LINES = ["<br>", "<br />", "<br/>", "\n", ""]


def download_page(url_to_check):
    # http://catalog.odu.edu/courses/

    # https://stackoverflow.com/questions/4485113/how-do-i-download-a-website-using-python-3
    html = urlopen(url_to_check).read().decode("utf-8")

    return html


def extract_program_details(page_html):

    soup = BeautifulSoup(page_html, "html.parser")

    # print(soup.prettify())

    dash_regex = re.compile("-|–")

    programs = []

    for program_block in soup.select(".sitemap li a"):
        split_idx = dash_regex.search(program_block.string).start()

        abbrev = program_block.string[:split_idx].strip()
        name = program_block.string[split_idx + 1:].strip()

        href = program_block["href"]

        programs.append(Subject(abbrev=abbrev,
                                full=name,
                                path=href))

    return programs


def extract_course_details(page_html):

    soup = BeautifulSoup(page_html, "html.parser")
    # print(soup.prettify())

    courses = []

    for course_block in soup.select(".courseblock"):
        # print(course_block.prettify())

        course = {
            "number": course_block.select(".coursecode")[0].string,
            "title": course_block.select(".coursetitle")[0].string,
            "credits": course_block.select(".coursehours")[0].string,
            "description": course_block.select(".courseblockdesc")[0].contents
        }

        course = sanitize_course_details(**course)

        # Retrict to CS 4xx an lower (undergrad)
        if int(course["number"].split()[1][0]) < 5:
            courses.append(course)

    return courses


def split_description(raw_description):

    description = raw_description.replace("\xa0", " ").split("Prerequisites:")

    if len(description) == 1:
        description = description[0].split("Prerequisite:")

    if len(description) > 1:
        description, prereqs = description

        prereqs = re.sub(r"\s*<[/]*a[^>]*>\s*", r" ", prereqs)
        prereqs = prereqs.replace("\xa0", " ").strip()

    else:
        description = description[0]
        prereqs = None

    description = re.sub(r"<[/]*a[^>]*>\s*", r" ", description)

    return description, prereqs


def sanitize_course_details(number, title, credits, description):

    course = {"number": number.replace("\xa0", " "),
              "title": str(title),
              "credits": credits.split("C")[0][:-1]}

    # Description processing is a little more fun

    description = [str(line).strip() for line in description]
    description = " ".join([line for line in description
                            if line not in BLANK_LINES])

    description, prereqs = split_description(description)

    course["description"] = re.sub(r"\s{2,}", " ", description.strip())
    course["prereqs"] = prereqs

    return course
