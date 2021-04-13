import configparser
import os

class Config:

    def __init__(self, section):
        self.filepaths = [
            ".reporter.cfg",
            os.path.expanduser("~/.reporter.cfg")
            ]

        self.config = configparser.ConfigParser()
        self.config.read(filenames=self.filepaths)
        self.config = self.config[section]

    def get_list(self, name, delimiter=","):
        conf = self.config.get(name)
        if conf is None:
            return None
        return conf.split(delimiter)

    def get(self, name):
        return self.config.get(name)
