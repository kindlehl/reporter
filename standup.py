#!/usr/bin/env python

import datetime
import utils.db
import utils.time

# Read today's data pull
tasks = utils.db.read()

last_week_start, last_week_end = utils.time.last_week()
this_week_start, this_week_end = utils.time.this_week()

report = {
        "This Week": [],
        "Last Week": []
        }

for task in tasks:
    if task["completed"]:
        print(dir(task["completed_datetime"]))
        if last_week_start < task["completed_datetime"] <  last_week_end:
            report["Last Week"].append(task)

    if task["due_date"] is not None:
        if this_week_start < task["due_date"] <  this_week_end:
            report["This Week"].append(task)

    else:
        print("task not matching")
            
utils.db.write(report, "report.yaml")
