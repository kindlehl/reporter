#!/usr/bin/env python

import utils.db
import utils.time

from utils.category import Category
from utils.report import Report
from utils.task import Task
from utils.config import Config
from utils.debug import debug

config = Config("standup")
tags_to_keep = config.get_list("tags")
default_tag = config.get("default_tag")
task_attrib_whitelist = config.get_list("attribute_whitelist")

# Debugging statements for ConfigParser
debug(tags_to_keep)
debug(default_tag)
debug(task_attrib_whitelist)

# Read today's data pull
tasks_yaml = utils.db.read()

tasks = [Task(**item) for item in tasks_yaml]

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

        # Add tags to category if they don't exist yet
        if not category.find(tag) and (tags_to_keep is None or tag in tags_to_keep):
            category.add(Category(tag))

        # Get the tag (subcat) from main category
        subcat = category.find(tag)

        if subcat is not None:
            subcat.add(task)
            return True

        return False

# Get comparable times
last_week_start, last_week_end = utils.time.last_week()
this_week_start, this_week_end = utils.time.this_week()

for task in tasks:
    # Add a default tag
    if len(task.tags) == 0:
        debug("NO TAG")
        task.set(tags=[default_tag])

    #print(task.dict)
    if task.completed:
        debug(dir(task.completed_datetime))
        if last_week_start < task.completed_datetime <  last_week_end:
            add_task(task, lw, *task_attrib_whitelist)

    elif task.due_date is not None:
        if this_week_start < task.due_date <  this_week_end:
            add_task(task, tw, *task_attrib_whitelist)
    else:
        debug("task not matching")

report = Report()
report.add(lw)
report.add(tw)
report.write()
