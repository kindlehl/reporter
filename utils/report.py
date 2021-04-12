import utils.db

# This class will hold all the settings and provide methods for writing reports
class Report():
    def __init__(self, **kwargs):
        self.name = 'report'
        self.categories = []
        # Access args via '.'
        self.__dict__.update(kwargs)
        self._update()

    def add(self, c):
        self.categories.append(c)
        self._update()

    def delete(self, c):
        self.categories.pop(c)

    def find(self, s):
        return None

    def _update(self):
        # Update top-level dict keys to write to report file
        self._dict = {}
        for c in self.categories:
            self._dict.update(c.dict)

    def write(self):
        utils.db.write(self._dict, "%s.yaml" % self.name)
