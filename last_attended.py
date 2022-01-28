"""Short script for gathering statistics from an attendance CSV file."""

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
    
### Test code
report("test.csv")
