from utils.task import Task
# This is the data structure that the report class will manage. It is recursive and forms a tree, where a category holds
# a category or task.

class Category:
    # Maybe consider @property for these and return the name instead of the obj???
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.categories = []

    # Check if categories are the same thing
    def __eq__(self, c):
        for task in self.tasks:
            if task not in c.tasks:
                return False

        for cat in self.categories:
            if cat not in c.categories:
                return False

        if self.name != c.name:
            return False

        return True
    
    def find(self, thing):
        if isinstance(thing, Category):
            return self.categories.index(thing)
        if isinstance(thing, Task):
            return self.tasks.index(thing)

        """
        {
            "work": [
                "aft":
                    - task
            ]
        }
        """

    @property
    def dict(self):
        things = self.categories + self.tasks
        if len(things) > 0:
            return {self.name: [i.dict for i in things]}
        else:
            return {self.name: {}}


    def add(self, thing):
        if isinstance(thing, Category):
            self.categories.append(thing)
        elif isinstance(thing, Task):
            self.tasks.append(thing)

    def delete(self, thing):
        if isinstance(thing, Category):
            return self.categories.pop(thing)
        if isinstance(thing, Task):
            return self.tasks.pop(thing)
