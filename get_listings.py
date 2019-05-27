#! /usr/bin/env python3

from pprint import PrettyPrinter
from collections import namedtuple

import sys
import re
import os
import gzip
import json
import copy

import odu_catalog.scraper as scraper
import odu_catalog.prereqextract as pe


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


def update_master_list(all_courses, full_prereq_chain,
                       prereq_to, prereq_to_chain):

    for course in all_courses:
        prereqs = list(full_prereq_chain[course["number"]])
        required_for = sorted(prereq_to[course["number"]])
        required_for_chain = sorted(list(prereq_to_chain[course["number"]]))

        course["prereq_chain"] = prereqs
        course["required_for"] = required_for
        course["required_for_chain"] = required_for_chain


if __name__ == "__main__":

    download_all_programs()

    pp = PrettyPrinter(indent=2, stream=sys.stderr)

    subject_list = ["cs", "math", "engl"]

    courses = []

    for abbrev in subject_list:
        with gzip.open(f"courses/{abbrev}.html.gz", "rt") as subject_file:
            the_page = subject_file.read()

        courses += scraper.extract_course_details(the_page)

    pe.extract_usable_prereqs(courses)

    # pp.pprint(courses)
    print("-" * 80)

    all_prereqs = pe.extract_prereqs_as_dict(courses)
    # pp.pprint(all_prereqs)

    ignored_courses = pe.walk_prereq_chains(all_prereqs)

    # print("-" * 80)
    # pp.pprint(all_prereqs)

    # print("-" * 80)
    # pp.pprint(ignored_courses)

    cs_courses = [crs for crs in courses
                  if crs["number"].upper().startswith("CS")]

    prereq_to = pe.find_required_for(courses)
    pp.pprint(prereq_to)

    pre_req_to_full_chain = copy.deepcopy(prereq_to)
    prereq_to_full_chain = pe.walk_required_for_chains(prereq_to)

    update_master_list(courses, all_prereqs, prereq_to, prereq_to_full_chain)

    with open("cs_list.json", "w") as cs_json_file:
        json.dump(cs_courses, cs_json_file, indent=4)
