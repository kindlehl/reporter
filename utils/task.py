class Task(object):
    # This means any kwarg passed to the constructor will be accessible via '.'. So task = Task(foo='bar') means task.foo == 'bar'
    def __init__(self, **kwargs):
        # Things we want to access via . operator
        # Or things we want to access in helper methods
        self.__dict__.update(kwargs)

        # Things we want to show up in reports
        self._public = kwargs

    def hide(self, *fields):
        try:
            for f in fields:
                self._public.pop(f)
        except:
            import pdb
            #pdb.set_trace()

    def set(self, **kwargs):
        self._public.update(kwargs)
        self.__dict__.update(kwargs)

    # Return objects that we want to publish
    @property
    def dict(self):
        return self._public

# Remove unwanted fields from tasks
def strip(task, *args):
    for field in args:
        task.hide(field)
    return task
