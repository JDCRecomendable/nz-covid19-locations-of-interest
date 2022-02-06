from requests import get


def get_data(url):
    response = get(url)
    if response.status_code != 200:
        return {'error': True}
    else:
        response.encoding = 'UTF-8'
        return response.json()
