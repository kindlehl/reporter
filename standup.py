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


###### BEGIN SETTINGS THAT SHOULD BE CONFIGURABLE

# handle this via cli args PLS
if 'tags' in os.environ:
    tags_to_keep = os.environ["tags"].split(',')
else:
    tags_to_keep = []

default_tag = 'Unknown'
task_attrib_whitelist = ['description', 'due_date']

###### END

# Read today's data pull
tasks_yaml = utils.db.read()

tasks = [Task(**item) for item in tasks_yaml]

if len(tags_to_keep) == 0:
    for task in tasks:
        for tag in task.tags:
            if tag not in tags_to_keep:
                tags_to_keep.append(tag)

lw = Category('Last Week')
tw = Category('This Week')

# Add task to category
# Create sub-catagories for all tags
def add_task(task, category, *whitelist):
    # __dict__ member, should deep copy (I think)
    task_tags = task.tags

    # Clean the task
    task.trim(*whitelist)
    for tag in task_tags:

        if not category.find(tag) and tag in tags_to_keep:
            category.add(Category(tag))

        subcat = category.find(tag)

        if tag in tags_to_keep:
            subcat.add(task)
            return True

        return False

# Get comparable times
last_week_start, last_week_end = utils.time.last_week()
this_week_start, this_week_end = utils.time.this_week()

for task in tasks:
    # Add a default tag
    if len(task.tags) == 0:
        print("NO TAG")
        task.set(tags=[default_tag])

    #print(task.dict)
    if task.completed:
        # Implement debugging
        #print(dir(task["completed_datetime"]))
        if last_week_start < task.completed_datetime <  last_week_end:
            add_task(task, lw, *task_attrib_whitelist)

    elif task.due_date is not None:
        if this_week_start < task.due_date <  this_week_end:
            add_task(task, tw, *task_attrib_whitelist)
    #else:
        # Implement debugging
        #print("task not matching")

report = Report()
report.add(lw)
report.add(tw)
report.write()
