from flask import Flask, jsonify, request
from nz_covid19_lit.constants import *
from nz_covid19_lit.controller import NZCovid19Lit


app = Flask('__main__')
nz_covid19_lit = NZCovid19Lit(url, path_to_data, seconds_before_next_update)


@app.route('/', methods=['GET', 'POST'])
def show():
    auto_refresh()
    if is_filtered(request):
        request_body_json = request.get_json()
        process_filter(request_body_json)
    return make_response(nz_covid19_lit.fetch())


@app.route('/locations/', methods=['GET', 'POST'])
def show_location_names():
    auto_refresh()
    return make_response(nz_covid19_lit.list_location_names())


@app.route('/exposure-types/', methods=['GET', 'POST'])
def show_exposure_types():
    auto_refresh()
    return make_response(nz_covid19_lit.list_exposure_types())


@app.route('/suburbs/', methods=['GET', 'POST'])
def show_suburbs():
    auto_refresh()
    return make_response(nz_covid19_lit.list_suburbs())


@app.route('/cities/', methods=['GET', 'POST'])
def show_cities():
    auto_refresh()
    return make_response(nz_covid19_lit.list_cities())


@app.route('/addresses/', methods=['GET', 'POST'])
def show_addresses():
    auto_refresh()
    return make_response(nz_covid19_lit.list_addresses())


def auto_refresh():
    if not nz_covid19_lit.is_recent():
        nz_covid19_lit.refresh_data()


def is_filtered(http_request):
    if http_request.method == 'GET':
        return False
    request_body_json = request.get_json()
    if 'isFiltered' not in request_body_json:
        return False
    return request_body_json['isFiltered']


def process_filter(request_body_json):
    nz_covid19_lit.clear_filters()
    if 'startDate' in request_body_json\
            and 'endDate' in request_body_json:
        start_date_string = request_body_json['startDate']
        end_date_string = request_body_json['endDate']
        nz_covid19_lit.filter_by_date(start_date_string, end_date_string)
    if 'locationName' in request_body_json\
            and 'locationIsExact' in request_body_json:
        location_name = request_body_json['locationName']
        location_is_exact = request_body_json['locationIsExact']
        nz_covid19_lit.filter_by_location_name(location_name, location_is_exact)
    if 'exposureType' in request_body_json\
            and 'locationIsExact' in request_body_json:
        exposure_type = request_body_json['exposureType']
        exposure_is_exact = request_body_json['exposureIsExact']
        nz_covid19_lit.filter_by_exposure_type(exposure_type, exposure_is_exact)
    if 'startLatitude' in request_body_json\
            and 'endLatitude' in request_body_json:
        start_latitude = request_body_json['startLatitude']
        end_latitude = request_body_json['endLatitude']
        nz_covid19_lit.filter_by_latitude(start_latitude, end_latitude)
    if 'startLongitude' in request_body_json\
            and 'endLongitude' in request_body_json:
        start_longitude = request_body_json['startLongitude']
        end_longitude = request_body_json['endLongitude']
        nz_covid19_lit.filter_by_longitude(start_longitude, end_longitude)
    if 'suburb' in request_body_json\
            and 'suburbIsExact' in request_body_json:
        suburb = request_body_json['suburb']
        suburb_is_exact = request_body_json['suburbIsExact']
        nz_covid19_lit.filter_by_suburb(suburb, suburb_is_exact)
    if 'city' in request_body_json\
            and 'cityIsExact' in request_body_json:
        city = request_body_json['city']
        city_is_exact = request_body_json['cityIsExact']
        nz_covid19_lit.filter_by_city(city, city_is_exact)
    if 'address' in request_body_json\
            and 'addressIsExact' in request_body_json:
        address = request_body_json['address']
        address_is_exact = request_body_json['addressIsExact']
        nz_covid19_lit.filter_by_address(address, address_is_exact)


def make_response(raw_data):
    response = jsonify(raw_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
