# Reporter
## How to process task data from Tracks

I had a few afternoons of free time and wrote a report generator for my task/time-management software I run on my
laptop.

`pull.py` is used to pull xml data from the Tracks REST API, filter out the nitty from the gritty, and dumps it as YAML into a local file named  `yyyy-mm-dd.yaml`.

`standup.py` is used to pull data that I can reference for weekly standup meetings. It grabs only tasks from last week
and next week, and sorts them based on their tags (usually project names). You can configure which tags get included or
excluded, and which fields from the tasks get included or excluded. It dumps its contents into yyyy-mm-dd-report.yaml

### How to get started

#### Running tracks

You need to be running [tracks](https://github.com/TracksApp/tracks). I am running from docker-compose on `bbed5b9100005b15d77df639fcd462b0b23aaeb2`. The project in general is kinda dead so I wouldn't recommend running it on an internet-exposed link.

#### Configure Reporter

Make sure you have a `.reporter.cfg` in the working directory. Example file with all options below:

~~~ini
[pull]
username = admin
password = password
hostname = localhost
port = 3000
[standup]
tags = internal,clientx,clienty,open_source # Tags to put into report
attribute_whitelist = description,due_date # Task (Tracks actions) fields to keep in report.
default_tag = NO_TAG
~~~

#### Pull data

If you run `./pull.py`, you should end up with a file in the working directory named `yyyy-mm-dd.yaml`. This is what
`./standup.py` will use to generate the report.

This is what the typical output will look like:

~~~yaml
- completed: true
  completed_datetime: 2021-04-07 08:28:32-05:00
  description: Read chapter 10
  due_date: 2021-04-07 00:00:00-05:00
  tags:
  - education
- completed: false
  completed_datetime: null
  description: File taxes
  due_date: 2021-04-15 18:00:00-05:00
  tags:
  - taxes
- completed: false
  completed_datetime: null
  description: Login to intuit
  due_date: null
  tags:
  - taxes
- completed: false
  completed_datetime: null
  description: Pester coworker to review PR
  due_date: 2021-04-16 00:00:00-05:00
  tags:
  - clientx
- completed: false
  completed_datetime: null
  description: Keep an eye out on Redis Servers
  due_date: 2021-04-14 00:00:00-05:00
  tags: []
- completed: true
  completed_datetime: 2021-04-08 11:55:09-05:00
  description: Read ansible style guide
  due_date: 2021-04-08 00:00:00-05:00
  tags:
  - ansible
~~~

#### Build report

Using the example config and the data you just generated via `pull.py`, `standup.py` is going to generate 
this for you:

~~~yaml
Last Week:
- education:
  - description: Read chapter 10
    due_date: 2021-04-07 00:00:00-05:00
- ansible:
  - description: Read ansible style guide
    due_date: 2021-04-08 00:00:00-05:00
This Week:
- taxes:
  - description: File taxes
    due_date: 2021-04-15 18:00:00-05:00
- clientx:
  - description: Pester coworker to review PR
    due_date: 2021-04-16 00:00:00-05:00
~~~

I like to use this data to quickly refer to what I've done recently, and what I'm going to do soon.
