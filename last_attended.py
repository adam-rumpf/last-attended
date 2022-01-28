"""Short script for gathering statistics from an attendance CSV file."""

import re

#==============================================================================

def report(infile, outfile=None, date=None):
    """report(infile[, outfile][, current])
    
    Gathers statistics from a specified attendance CSV file and outputs the
    results to another file (or to the shell).
    
    Positional arguments:
        infile (str) - path to the input CSV file
    
    Keyword arguments:
        outfile (str) - path to the output TXT file (default None, which prints
            results to the shell without saving)
        date (str) - current date to use for measuring "last attended X days
            ago" reports; options include:
                "today" - the current date
                "[M]M/[D]D/[YY]YY" - a specific date
                None - the last date included in the CSV file
    
    This script assumes a few specific aspects of the input CSV file format:
        - a "Student Name" field, which is used to accumulate a list of student
            statistics
        - a "Class Date" field in "[M]M/[D]D/[YY]YY" format
        - an "Attendance" field including either "present" or "absent"
    """
    
    # Read input file
    pass

#==============================================================================

def _date_tuple(strdate):
    """_date_tuple(strdate)

    Converts a date string of the format "[M]M/[D]D/[YY]YY" into a 3-tuple
    of month, day, and year integers.

    Positional arguments:
        strdate (str) - date string of the format "[M]M/[D]D/[YY]YY"

    Returns:
        tuple ((int, int, int)) - tuple of (month, day, year) integers

    The general input date format should consist of the following, in order:
        1. 1-2 digits
        2. a delimeter from the set "/", "\", "-", "_", ".", ",", or whitespace
        3. 1-2 digits
        4. another delimeter
        5. 2 or 4 digits
    """

    # Split string and verify length
    s = re.split("[/\\-_., \t]+", strdate)
    if len(s) != 3:
        raise ValueError("input date must include 3 delimited numbers")

    # Read the input numbers
    m = int(s[0])
    d = int(s[1])
    y = int(s[2])

    # Add 2000 to a 2-digit year
    if y < 100:
        y += 2000

    return (m, d, y)
    
### Test code
report("test.csv")
