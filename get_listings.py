#! /usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple

import sys
import re
import os

import odu_catalog.scraper as scraper


COURSE_NUM_PATTERN = r"[A-Za-z]{2,} \d{3}[AGHNRT]{0,1}(/\d{3}){0,1}"


def _extract_prereq_courses(prereq_statement):

    return [course.group(0) for course in re.finditer(COURSE_NUM_PATTERN,
                                                      prereq_statement)]


def extract_usable_prereqs(courses):

    for course in courses:
        print(course["prereqs"])

        if not course["prereqs"]:
            course["prereq_list"] = []
        else:
            course["prereq_list"] = _extract_prereq_courses(course["prereqs"])


def find_is_required_for(course, all_courses):

    print(f"{course['number']}:", end="")

    for other_course in all_courses:

        if course["number"] in other_course["prereq_list"]:
            print(other_course["number"], "", end="")

    print()


if __name__ == "__main__":

    # base_page = download_page("http://catalog.odu.edu/courses/");
    # extract_program_details(base_page)
    base_catalog_url = "http://catalog.odu.edu/courses/cs/"

    if os.path.exists("courses-cs.html"):
        with open("courses-cs.html", "r") as subject_file:
            the_page = subject_file.read()

    else:

        with open("courses-cs.html", "w") as subject_file:
            the_page = scraper.download_page(base_catalog_url)

            subject_file.write(the_page)

    pp = PrettyPrinter(indent=2, stream=sys.stderr)
    courses = scraper.extract_course_details(the_page)

    extract_usable_prereqs(courses)

    pp.pprint(courses)

    for course in courses:
        find_is_required_for(course, courses)
