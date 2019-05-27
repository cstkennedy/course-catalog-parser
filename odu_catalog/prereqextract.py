import re


COURSE_NUM_PATTERN = r"[A-Za-z]{2,} \d{3}[ACGHMNRTW]{0,1}(/\d{3}){0,1}"


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


def list_contains_a(subject: str, course_list):

    for course in course_list:
        if course.lower().startswith(subject):
            return True

    return False


def find_is_required_for(course, all_courses):

    prereq_to_list = []

    for other_course in all_courses:
        if course["number"] in other_course["prereq_list"]:
            prereq_to_list.append(other_course["number"])

    if len(prereq_to_list) > 0 and list_contains_a("cs", prereq_to_list):
        print(f"{course['number']}: ", end="")
        print(", ".join(prereq_to_list))


def extract_prereqs_as_dict(all_courses):
    """
    Map course number to immediate prereqs.

    :param all_courses: list with all course metadata

    :returns: sorted dictionary keyed on course number
    """

    return {crs["number"]: set(crs["prereq_list"]) for crs
            in sorted(all_courses, key=lambda crs: crs["number"])}


def walk_prereq_chains(all_prereqs):
    """
    Walk the full prereq chain for each course. If a prereq course is not in
    the dictionary, skip it.

    This can happen if the focus is on CS and CEE was not analyzed (ECE
    requires a CEE course).
    """

    ignored_courses = []

    for course in all_prereqs:
        for prereq in all_prereqs[course]:
            try:
                all_prereqs[course] = all_prereqs[course].union(all_prereqs[prereq])

            except KeyError as e:
                ignored_courses.append(prereq)

    return ignored_courses
