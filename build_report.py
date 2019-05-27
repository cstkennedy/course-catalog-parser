#! /usr/bin/env python3

from pprint import PrettyPrinter

import sys
import re
import os
import gzip
import json
import copy
import contextlib

COURSE_TEMPLATE = """
# {number} - {title}

**Credits:** {credits}

{description}


## Prerequisites

{prereqs}

"""


def as_md_list(crs_list):

    for crs in crs_list:
        yield f"  * {crs}"


def generate_report(course_list, fp):
    with contextlib.redirect_stdout(fp):
        for course in course_list:
            print(COURSE_TEMPLATE.format(**course))

            if course["prereqs"]:
                print("### Immediate Prereqs")
                print()
                print("\n".join(as_md_list(course["prereq_list"])))
                print()

                print("### Indirect Prereqs")
                print()
                print("\n".join(as_md_list(course["prereq_chain"])))
                print()

                if len(course["required_for"]) > 0:
                    print("## (Directly) Required By")
                    print()
                    print("\n".join(as_md_list(course["required_for"])))
                    print()

                    print("## (Indirectly) Required By")
                    print()
                    print("\n".join(as_md_list(course["required_for_chain"])))
                    print()


if __name__ == "__main__":

    with open("cs_list.json", "r") as cs_json_file:
        cs_list = json.load(cs_json_file)

    with open("course_list.md", "w") as report_file:
        generate_report(cs_list, report_file)
