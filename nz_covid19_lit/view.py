import json
from flask import Flask
from nz_covid19_lit.constants import *
from nz_covid19_lit.controller import NZCovid19Lit


app = Flask('__main__')
nz_covid19_lit = NZCovid19Lit(url, path_to_data, seconds_before_next_update)


def auto_refresh():
    if not nz_covid19_lit.is_recent():
        nz_covid19_lit.refresh_data()


@app.route('/')
def show_all():
    auto_refresh()
    return nz_covid19_lit.fetch_all()


@app.route('/locations/')
def show_location_names():
    auto_refresh()
    return nz_covid19_lit.list_location_names()


@app.route('/exposure-types/')
def show_exposure_types():
    auto_refresh()
    return nz_covid19_lit.list_exposure_types()


@app.route('/suburbs/')
def show_suburbs():
    auto_refresh()
    return nz_covid19_lit.list_suburbs()


@app.route('/cities/')
def show_cities():
    auto_refresh()
    return nz_covid19_lit.list_cities()


@app.route('/addresses/')
def show_addresses():
    auto_refresh()
    return nz_covid19_lit.list_addresses()
