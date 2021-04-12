import utils.db

# This class will hold all the settings and provide methods for writing reports
class Report():
    def __init__(self, **kwargs):
        self.name = 'report'
        self.categories = []
        # Access args via '.'
        self.__dict__.update(kwargs)

    def add(self, c):
        self.categories.append(c)

    def delete(self, c):
        self.categories.pop(c)

    def update(self):
        # Update top-level dict keys to write to report file
        self._dict = {d.name: d.dict for d in self.categories}
        return self._dict

    def write(self):
        db.write(self._dict, "%s.yaml" % self.name)
