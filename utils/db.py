from datetime import datetime
import yaml

# This is required to prevent yaml from using anchors for shared objects. We want to see data, not anchors!
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def db_file():
    return datetime.today().strftime('%Y-%m-%d.yaml')

def write(data, filename=db_file()):
    with open(filename, 'w') as yaml_file:
        yaml.dump(data, yaml_file, Dumper=NoAliasDumper)

def read(filename=db_file()):
    with open(filename) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data
