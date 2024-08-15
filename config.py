import os
from configparser import ConfigParser

def config(filename='/home/alex/PycharmProjects/pythonProjectDB/database.ini', section='postgresql'):
    # Verify the path to the database.ini file
    if not os.path.isfile(filename):
        raise Exception(f'File {filename} not found')

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db