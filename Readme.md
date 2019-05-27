# Known Bugs

  1. There is no handling of the interchangeable (and lackadaisical) use of CS
     4xx/5xx vs CS 4xx.

  2. There is no handling of _or_ vs _and_ in prereq extraction.

  3. Prereq extraction is based purely on finding numbers that fit the regular
     expression `[A-Za-z]{2,} \d{3}[ACGHMNRTW]{0,1}(/\d{3}){0,1}`.

    - This results in listings such as `Engl 3xx to 3xx` generating both `Engl
      3xx` and `to 3xx`.

    - This results in cases (of laziness) where the subject was omitted from a
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
