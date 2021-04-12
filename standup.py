#!/usr/bin/env python

import datetime
import utils.db
import utils.time
import utils.task

from utils.category import Category
from utils.report import Report
from utils.task import Task

import pdb

import os

# handle this via cli args PLS
if 'tags' in os.environ:
    tags_to_keep = os.environ["tags"].split(',')
else:
    tags_to_keep = None

# Read today's data pull
tasks_yaml = utils.db.read()

tasks = [Task(**item) for item in tasks_yaml]

# Get comparable times
last_week_start, last_week_end = utils.time.last_week()
this_week_start, this_week_end = utils.time.this_week()

lw = Category('Last Week')
tw = Category('This Week')

lw.add(Category("Unknown"))
tw.add(Category("Unknown"))

# Add task to category
def add_task(task, category, *cleanup):
    # Remove useless fields
    if len(task.tags) == 0:
        task.set(tags=["Unknown"])
    for tag in task.tags:
        if tags_to_keep and tag not in tags_to_keep:
            return False

        # Get 'tag' category
        tag_cat = category.find(tag)
        if tag_cat is None:
            # Or create it if it doesn't exist
            category.add(Category(tag))
            tag_cat = category.find(tag)

        task.hide(*cleanup)
        tag_cat.add(task)
    return True

trim = ['completed', 'completed_datetime', 'tags']
#trim = []

for task in tasks:
    #print(task.dict)
    if task.completed:
        # Implement debugging
        #print(dir(task["completed_datetime"]))
        if last_week_start < task.completed_datetime <  last_week_end:
            add_task(task, lw, *trim)

    elif task.due_date is not None:
        if this_week_start < task.due_date <  this_week_end:
            add_task(task, tw, *trim)
    #else:
        # Implement debugging
        #print("task not matching")

report = Report()
report.add(lw)
report.add(tw)
report.write()
