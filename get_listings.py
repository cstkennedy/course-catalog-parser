#! /usr/bin/env python3

from urllib.request import urlopen
from pprint import PrettyPrinter
import sys
import re
import os
from collections import namedtuple

from bs4 import BeautifulSoup

Subject = namedtuple("Subject", ["abbrev", "full", "path"])


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

        course = {"number": course_block.select(".coursecode")[0].string,
                  "title": course_block.select(".coursetitle")[0].string,
                  "credits": course_block.select(".coursehours")[0].string,
                  "description": course_block.select(".courseblockdesc")[0].contents}

        course = sanitize_course_details(**course)

        # Retrict to CS 4xx an lower (undergrad)
        if int(course["number"].split()[1][0]) < 5:
            courses.append(course)

    return courses


def sanitize_course_details(number, title, credits, description):

    course = {"number": number.replace("\xa0", " "),
              "title": title,
              "credits": credits.split("C")[0][:-1]}

    # Description processing is a little more fun
    BLANK_LINES = ["<br>", "<br />", "<br/>", "\n", ""]

    description = [str(line).strip() for line in description]
    description = " ".join([line for line in description if line not in BLANK_LINES])

    # print(description)

    description = description.replace("\xa0", " ").split("Prerequisites:")

    if len(description) == 1:
        description = description[0].split("Prerequisite:")

    if len(description) > 1:
        description, prereqs = description

        prereqs = re.sub(r"<[/]*a[^>]*>", r" ", prereqs)
        prereqs = prereqs.replace("\xa0", " ").strip()

        # for pq_course in re.finditer(r"[A-Za-z]{2,} \d{3}(/\d{3}){0,1}", prereqs):
        #   print("\"{}\"->\"{}\"".format(number,pq_course.group(0)))

    else:
        description = description[0]
        prereqs = None

    description = re.sub(r"<[/]*a[^>]*>", r" ", description)

    # print(prereqs)

    course["description"] = description
    course["prereqs"] = prereqs

    return course


if __name__ == "__main__":

    # base_page = download_page("http://catalog.odu.edu/courses/");
    # extract_program_details(base_page)

    if os.path.exists("courses-cs.html"):
        with open("courses-cs.html", "r") as subject_file:
            the_page = subject_file.read()

            # print(the_page)
    else:
        with open("courses-cs.html", "w") as subject_file:
            the_page = download_page("http://catalog.odu.edu/courses/cs/")

            subject_file.write(the_page)

    pp = PrettyPrinter(indent=2, stream=sys.stderr)
    courses = extract_course_details(the_page)

    pp.pprint(courses)

    print(courses[0])
