from datetime import datetime
import yaml

def db_file():
    return datetime.today().strftime('%Y-%m-%d.yaml')

def write(data, filename=db_file()):
    with open(filename, 'w') as yaml_file:
        yaml.dump(data, yaml_file)

def read(filename=db_file()):
    with open(filename) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data
