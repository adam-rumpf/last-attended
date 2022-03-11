# Last Attended

<a href="https://github.com/adam-rumpf/last-attended/search?l=python"><img src="https://img.shields.io/badge/language-python-blue?logo=python&logoColor=white"/></a> <a href="https://github.com/adam-rumpf/last-attended/tags"><img src="https://img.shields.io/github/v/tag/adam-rumpf/last-attended?logo=github"></a> <a href="https://github.com/adam-rumpf/last-attended/blob/main/LICENSE"><img src="https://img.shields.io/github/license/adam-rumpf/last-attended"/></a> <a href="https://github.com/adam-rumpf/last-attended/commits/main"><img src="https://img.shields.io/maintenance/yes/2022"/></a>

A small Python script to process inconveniently-formatted attendance reports.

The classroom attendance utility that I currently use exports its attendance reports as extremely long `.csv` files with one row per attendance entry, and with no ability to mark absences as excused. This makes it pretty much impossible to tell at a glance how long it's been since a student has attended class. This is a small script for extracting the useful information that I want from the database. It's fairly specific to the particular format of the attendance utility I use, so it's unlikely that very many people will find this script useful, but that's never stopped me from posting something before.

The `report()` function defined in this script accepts a path to a `.csv` file, an output file path (optional; defaults to printing to the shell), and a date (optional, in YYYY/MM/DD format; defaults to the last date in the input file). The output file includes a table of all unique student names, their overall attendance percentage (with blank entries counting as excused), and how many class days it's been since they've attended.
