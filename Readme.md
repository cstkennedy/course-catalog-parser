# Known Bugs

  1. There is no handling of the interchangeable (and lackadaisical) use of CS
     4xx/5xx vs CS 4xx.

  2. There is no handling of _or_ vs _and_ in prereq extraction.

  3. Prereq extraction is based purely on finding numbers that fit the regular
     expression  
     `[A-Za-z]{2,} \d{3}[ACGHMNRTW]{0,1}(/\d{3}){0,1}`.

      This results in listings such as `Engl 3xx to 3xx` generating both
      `Engl 3xx` and `to 3xx`.

      This results in cases (of laziness) where the subject was omitted from a
      list (e.g., `Math 102M or 103M`) being partially processed.


# HTML Format Assumptions

It is assumed that all HTML follows the following structure

```html
<div class="courseblock">
<p class="courseblocktitle">
<strong>
<span class="coursecode">
CS 998
</span>
<span class="coursetitle">
Master's Graduate Credit
</span>
<span class="coursehours">
1 Credit
</span>
</strong>
</p>
<p class="courseblockdesc">
This course is a pass/fail course for master's students in their final semester. It may be taken to fulfill the registration requirement necessary for graduation.  All master's students are required to be registered for at least one graduate credit hour in the semester of their graduation.
<br/>
</p>
</div>
```

# JSON Output

The JSON Output will contain an entry for each course in the form:

```json
    {
        "number": "CS 150",
        "title": "Problem Solving and Programming I",
        "credits": "4",
        "description": "Laboratory work required. Introduction to computer-based problem solving and programming in C++. Topics include problem solving methodologies, program design, algorithm development, and testing. C++ language concepts include variables, data types and expressions, assignment, control-flow statements, functions, arrays, pointers, structs, and classes.",
        "prereqs": "MATH 102M or MATH 103M or equivalent.",
        "prereq_list": [
            "MATH 102M",
            "MATH 103M"
        ],
        "prereq_chain": [
            "to 450",
            "MATH 103M",
            "MATH 102M"
        ],
        "required_for": [
            "CS 170",
            "CS 250",
            "CS 252",
            "CS 270",
            "CS 333",
            "CS 334",
            "CS 381",
            "CS 431/531",
            "MATH 408/508"
        ],
        "required_for_chain": [
            "CS 170",
            "CS 250",
            "CS 252",
            "CS 270",
            "CS 312",
            "CS 330",
            "CS 333",
            "CS 334",
            "CS 350",
            "CS 355",
            "CS 361",
            "CS 381",
            "CS 382",
            "CS 390",
            "CS 410/510",
            "CS 411W/511",
            "CS 417/517",
            "CS 418/518",
            "CS 431/531",
            "CS 432/532",
            "CS 441/541",
            "CS 450/550",
            "CS 451/551",
            "CS 455/555",
            "CS 460/560",
            "CS 471",
            "CS 472",
            "CS 475/575",
            "CS 476/576",
            "CS 478/578",
            "CS 480/580",
            "CS 487",
            "CS 488/588",
            "MATH 408/508"
        ]
    },
```
