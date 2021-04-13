#!/usr/bin/env python

from datetime import datetime
import dateutil.parser
import requests
import xml
import utils.db
from requests.auth import HTTPBasicAuth
from utils.config import Config

import xml.etree.ElementTree as ET

config   = Config("pull")
username = config.get("username")
password = config.get("password")
hostname = config.get("hostname")
port     = config.get("port")

headers = {
        "Content-Type": "text/xml"
        }

auth=HTTPBasicAuth(username, password)

# Get list of all tasks in xml format
xml = requests.get("http://{}:{}/todos.xml".format(hostname, port), auth=auth).text

root = ET.fromstring(xml)
tasks = []

# THINGS TO DO NEXT:
# Implement contexts. This requires pulling contexts from the and using the context-id field in todos to lookup the
# proper context. 

# Grab todo objects under todo/*
for todo_e in root:
    # Get todo description
    desc = todo_e.find("description").text

    # Get todo context
    context_e = todo_e.find("context")

    if context_e is not None:
        context = context_e.text
        print(context)
    else:
        context = None

    # Get todo completion time
    completed_datestring = todo_e.find("completed-at").text
    if completed_datestring is not None:
        completed_date = dateutil.parser.parse(completed_datestring)
        completed = True
    else:
        completed_date = None
        completed = False

    # Get task due date
    due_datestring = todo_e.find("due").text
    if due_datestring is not None:
        due_date = dateutil.parser.parse(due_datestring)
    else:
        due_date = None

    # Initialize tags list for current todo
    tags = []
    
    # Grab tags for each todo under todo/*/tags/*
    for tag_e in todo_e.find("tags"):
        tags.append(tag_e.find("name").text)

    task = {
            "description": desc,
            "completed": completed,
            "completed_datetime": completed_date,
            "due_date": due_date,
            "tags": tags,
            }

    tasks.append(task)

utils.db.write(tasks)
