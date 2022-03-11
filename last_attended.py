"""Short script for gathering statistics from an attendance CSV file."""

import csv
import datetime
import re

#==============================================================================

def report(infile, outfile=None, date=None):
    """report(infile[, outfile][, date])
    
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
                "[YY]YY/[M]M/[D]D" - a specific date
                None - the last date included in the CSV file
    
    This script assumes a few specific aspects of the input CSV file format:
        - a "Student Name" field, which is used to accumulate a list of student
            statistics
        - a "Class Date" field in "[M]M/[D]D/[YY]YY" format
        - an "Attendance" field including either "present" or "absent"
    """

    # Initialize reference date tuple
    rdate = (0, 0, 0)

    # Initialize column indices
    namecol = -1 # student name
    datecol = -1 # date
    attcol = -1 # attendance status

    # Initialize a set of unique dates, for calculating total class days
    udates = set()

    # Initialize student dictionary, indexed by student names.
    # Values are lists containing the following in order:
    #   days attended
    #   last attendance tuple
    sdic = {}
    
    # Read input file
    with open(infile, 'r') as f:
        read = csv.reader(f)

        # Loop through rows
        for row in read:
            
            # Look for important columns if not already set
            if namecol < 0:
                namecol = row.index("Student Name")
                datecol = row.index("Class Date")
                attcol = row.index("Attendance")
                continue

            # Gather info from the column
            n = row[namecol] # row's student name
            d = _date_tuple(row[datecol]) # row's date tuple
            a = _attendance_code(row[attcol]) # row's attendance code

            # Add date to unique date list and update latest date
            udates.add(d)
            if _later_date(d, rdate):
                rdate = d

            # Create row entry for new students
            if n not in sdic:
                sdic[n] = [0, (0, 0, 0)]

            # Update row entry for logged students
            if a > 0:
                sdic[n][0] += 1
                if _later_date(d, sdic[n][1]):
                    sdic[n][1] = d

    # Choose reference date (defaults to last recorded date)
    if date == "today":
        dt = datetime.date.today()
        rdate = (int(dt.year), int(dt.month), int(dt.day))
    elif isinstance(date, str):
        rdate = _date_tuple(date)

    # Initialize output string
    ostring = "Grade Report\n\nName\tRate\tDays Since Attended\n"

    # Generate statistics for each student
    for n in sdic:
        r = sdic[n][0]/len(udates) # attendance rate
        g = _date_difference(rdate, sdic[n][1]) # days since last attended
        ostring += f'{n}\t{r:.1%}\t{g}\n'

    # Write to file or print to screen
    if outfile == None:
        print(ostring)
    else:
        with open(outfile, mode='w') as f:
            f.write(ostring)
        print("Grade report successfully written to '" + outfile + "'.")

#==============================================================================

def _date_tuple(strdate):
    """_date_tuple(strdate)

    Converts a date string of the format "[YY]YY/[M]M/[D]D" into a 3-tuple
    of month, day, and year integers.

    Positional arguments:
        strdate (str) - date string of the format "[YY]YY/[M]M/[D]D"

    Returns:
        tuple ((int, int, int)) - tuple of (year, month, day) integers

    The general input date format should consist of the following, in order:
        1. 1-2 digits
        2. a delimeter from the set "/", "\\", "-", "_", ".", ",", or whitespace
        3. 1-2 digits
        4. another delimeter
        5. 2 or 4 digits
    """

    # Split string and verify length
    s = re.split("[/\\-_., \t]+", strdate)
    if len(s) != 3:
        raise ValueError("input date must include 3 delimited numbers")

    # Read the input numbers
    y = int(s[0])
    m = int(s[1])
    d = int(s[2])

    # Add 2000 to a 2-digit year
    if y < 100:
        y += 2000

    return (y, m, d)

#==============================================================================

def _attendance_code(stratt):
    """_attendance_code(stratt)

    Converts an attendance string to a standardized numerical code.

    Positional arguments:
        stratt (str) - attendance string, either "present" or "absent"

    Returns:
        int - attendance code from the following list
            -1 - unrecognized
            0 - absent
            1 - present
    """

    if stratt.lower() == "present":
        return 1
    elif stratt.lower() == "absent":
        return 0
    else:
        return -1

#==============================================================================
def _year_days(year):
    """_year_days(year)

    Returns the number of days in a given year.

    Positional arguments:
        year (int) - a year

    Returns:
        int - number of days in the specified year

    This is computed according to the Gregorian calendar, under which a leap
    year occurs every 4 years, unless the year is divisible by 100 and not 400.
    """

    if (year % 4 != 0) or (year % 100 == 0 and year % 400 == 0):
        return 365
    else:
        return 366

#==============================================================================
def _month_days(month, year=None):
    """_month_days(month[, year])

    Returns the number of days in a given month.

    Positional arguments:
        month (int) - a month, with January = 1 and December = 12

    Keyword arguments:
        year (int) - a year (default None, which ignores leap years)

    Returns:
        int - number of days in the specified month of the specified year, or
            -1 if given an invalid month
    """

    # Categorize depending on month
    if month in {4, 6, 9, 11}:
        return 30
    elif month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    elif month == 2:
        if year == None:
            return 28
        else:
            return 28 + (_year_days(year) - 365)
    else:
        return -1

#==============================================================================
def _increment_date(date):
    """_increment_date(date)

    Increments a given date by one day.

    Positional arguments:
        date (tuple) - date tuple

    Returns:
        tuple - date tuple one day later than the given date
    """

    # Add 1 to the day
    d = (date[0], date[1], date[2] + 1)

    # Carry over the month if needed
    if d[2] > _month_days(d[1], year=d[0]):
        d = (d[0], d[1] + 1, 1)
        
        # Carry over the year if needed
        if d[1] > 12:
            d = (d[0] + 1, 1, 1)

    return d

#==============================================================================
def _date_difference(date1, date2):
    """_date_difference(date1, date2)

    Computes date1 minus date2, as a number of days.

    Positional arguments:
        date1 (tuple) - first date tuple
        date2 (tuple) - second date tuple

    Returns:
        int - number of days that need to be added to date2 to get to date1
    """

    # Determine the sign of the result
    negate = False
    d1 = date1
    d2 = date2
    if not _later_date(date1, date2):
        negate = True
        d2 = date1
        d1 = date2

    # Count days from earlier date to later date
    days = 0
    while _later_date(d1, d2):
        days += 1
        d2 = _increment_date(d2)

    # Return number of days counted, negated properly
    if negate:
        return -days
    else:
        return days

#==============================================================================

def _later_date(date1, date2):
    """_later_date(date1, date2)

    Compares two (month, day, year) tuples to see which is later.

    Positional arguments:
        date1 (tuple) - first date tuple
        date2 (tuple) - second date tuple

    Returns:
        bool - True if the first date is later than the second, False otherwise
    """

    # Compare years
    if date1[0] > date2[0]:
        return True
    elif date1[0] < date2[0]:
        return False
    else:
        # Compare months
        if date1[1] > date2[1]:
            return True
        elif date1[1] < date2[1]:
            return False
        else:
            # Compare days
            if date1[2] > date2[2]:
                return True
            else:
                return False
