class Task(object):
    # This means any kwarg passed to the constructor will be accessible via '.'. So task = Task(foo='bar') means task.foo == 'bar'
    def __init__(self, **kwargs):
        # Things we want to access via . operator
        # Or things we want to access in helper methods
        self.__dict__.update(kwargs)

        # Things we want to show up in reports
        self._public = kwargs

    # Whitelist fields to show in self.dict
    def trim(self, *keep):
        purge_list = []
        for field in self._public:
            if field not in keep:
                purge_list.append(field)
        # Hide fields
        for item in purge_list:
            self._public.pop(item)

    def set(self, **kwargs):
        self._public.update(kwargs)
        self.__dict__.update(kwargs)

    # Return objects that we want to publish
    @property
    def dict(self):
        return self._public
