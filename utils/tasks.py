# Remove unwanted fields from tasks
def strip(task, *args):
    for field in args:
        task.pop(field)
    return task
