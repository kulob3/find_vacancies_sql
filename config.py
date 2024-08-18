import os
from configparser import ConfigParser


def config(filename = os.path.abspath('database.ini'), section='postgresql'):
    """Функция для чтения файла конфигурации и возврата словаря с параметрами"""
    if not os.path.isfile(filename):
        raise Exception(f'File {filename} not found')
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db



