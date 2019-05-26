#! /usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple

import sys
import re
import os
import gzip

import odu_catalog.scraper as scraper


COURSE_NUM_PATTERN = r"[A-Za-z]{2,} \d{3}[AGHNRT]{0,1}(/\d{3}){0,1}"


def _extract_prereq_courses(prereq_statement):

    return [course.group(0) for course in re.finditer(COURSE_NUM_PATTERN,
                                                      prereq_statement)]


def extract_usable_prereqs(courses):

    for course in courses:
        # print(course["prereqs"])

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


def download_all_programs():

    base_catalog_url = "http://catalog.odu.edu/courses/"

    if not os.path.exists("courses"):
        os.mkdir("courses")

    if os.path.exists("courses.html"):
        with open("courses.html", "r") as courses_file:
            base_page = courses_file.read()

    else:
        base_page = scraper.download_page("http://catalog.odu.edu/courses/")

    programs = scraper.extract_program_details(base_page)

    for program in programs:
        # Trim the trailing and leading slashes
        file_path = program.path[1:-1] + ".html.gz"

        print(program.abbrev.lower(), file_path)

        program_url = base_catalog_url + program.abbrev.lower()

        if not os.path.exists(file_path):
            with gzip.open(file_path, "wt") as subject_file:
                the_page = scraper.download_page(program_url)
                subject_file.write(the_page)


if __name__ == "__main__":

    download_all_programs()

    pp = PrettyPrinter(indent=2, stream=sys.stderr)

    # Analyze CS
    with gzip.open("courses/cs.html.gz", "rt") as subject_file:
        the_page = subject_file.read()

    courses = scraper.extract_course_details(the_page)

    extract_usable_prereqs(courses)

    # pp.pprint(courses)

    for course in courses:
        find_is_required_for(course, courses)
