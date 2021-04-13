import argparse

description = """
Create reports from your task management webapp
"""

# Parse args to see if --debug was passed
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--debug', action='store_true', help="print debug messages")
args = parser.parse_args()

# So far, only one debug level
def debug(thing, level=1):
    if args.debug:
        print(thing)
