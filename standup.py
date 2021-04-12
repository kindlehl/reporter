#!/usr/bin/env python

import datetime
import utils.db
import utils.time
import os

if 'tags' in os.environ:
    tags_to_keep = os.environ["tags"].split(',')
else:
    tags_to_keep = None

# Read today's data pull
tasks = utils.db.read()

last_week_start, last_week_end = utils.time.last_week()
this_week_start, this_week_end = utils.time.this_week()

report = {
        "This Week": [],
        "Last Week": []
        }

last_week_projects = {"unknown_project": []}
this_week_projects = {"unknown_project": []}

for task in tasks:
    if task["completed"]:
        print(dir(task["completed_datetime"]))
        if last_week_start < task["completed_datetime"] <  last_week_end:
            # Remove useless fields
            task.pop('completed', None)
            task.pop('completed_datetime', None)
            if len(task["tags"]) == 0:
                task["tags"] = ["unknown"]
                #last_week_projects["unknown_project"].append(task)
            for tag in task["tags"]:
                if tags_to_keep and tag not in tags_to_keep:
                    continue
                if tag not in last_week_projects:
                    last_week_projects[tag] = []
                task.pop('tags', None)
                last_week_projects[tag].append(task)

    elif task["due_date"] is not None:
        if this_week_start < task["due_date"] <  this_week_end:
            # Remove useless fields
            task.pop('completed', None)
            task.pop('completed_datetime', None)

            if len(task["tags"]) == 0:
                task["tags"] = ["unknown"]
                #this_week_projects["unknown_project"].append(task)
            for tag in task["tags"]:
                if tags_to_keep and tag not in tags_to_keep:
                    continue
                if tag not in this_week_projects:
                    this_week_projects[tag] = []
                task.pop('tags', None)
                this_week_projects[tag].append(task)

    else:
        print("task not matching")

report["This Week"] = this_week_projects
report["Last Week"] = last_week_projects
            
utils.db.write(report, "report.yaml")
