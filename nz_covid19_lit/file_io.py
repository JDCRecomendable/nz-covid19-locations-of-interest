from json import dumps, loads
from json.decoder import JSONDecodeError


def load_from_file(file_location):
    data = {}
    try:
        with open(file_location, 'r') as data_file:
            data = loads(data_file.read())
    except IOError or JSONDecodeError:
        data['error'] = True
    return data


def save_to_file(file_location, data):
    try:
        with open(file_location, 'w') as data_file:
            data_file.write(dumps(data))
        return True
    except IOError or TypeError:
        return False
