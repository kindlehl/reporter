#!/usr/bin/env python

import datetime
import utils.db
import utils.time
import utils.tasks
import os

if 'tags' in os.environ:
    tags_to_keep = os.environ["tags"].split(',')
else:
    tags_to_keep = None

# Read today's data pull
tasks_yaml = utils.db.read()

tasks = [utils.tasks.Task(**item) for item in tasks_yaml]

last_week_start, last_week_end = utils.time.last_week()
this_week_start, this_week_end = utils.time.this_week()

report = {
        "This Week": [],
        "Last Week": []
        }

last_week_projects = {"unknown_project": []}
this_week_projects = {"unknown_project": []}

# Add task to project.
def add_task(task, project, *cleanup):
    # Remove useless fields
    if len(task.tags) == 0:
        task.tags = ["unknown"]
    for tag in task.tags:
        if tags_to_keep and tag not in tags_to_keep:
            return False
        if tag not in project:
            project[tag] = []
        utils.tasks.strip(task, *cleanup)
        project[tag].append(task.dict)
    return True

trim = ['completed', 'completed_datetime', 'tags']

# check if task is in a specific time slot
# clean it up
# toss it in
for task in tasks:
    if task.completed:
        # Implement debugging
        #print(dir(task["completed_datetime"]))
        if last_week_start < task.completed_datetime <  last_week_end:
            add_task(task, last_week_projects, *trim)

    elif task.due_date is not None:
        if this_week_start < task.due_date <  this_week_end:
            add_task(task, this_week_projects, *trim)
    #else:
        # Implement debugging
        #print("task not matching")

report["This Week"] = this_week_projects
report["Last Week"] = last_week_projects
            
# Only write task._yaml 
utils.db.write(report, "report.yaml")
