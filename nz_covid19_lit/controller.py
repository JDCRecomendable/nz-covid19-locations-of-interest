from datetime import date, datetime, timezone
from nz_covid19_lit.data_requestor import get_data
from nz_covid19_lit.file_io import load_from_file, save_to_file


def get_date_from_string(datetime_string):
    formatted = datetime_string.replace('T', ' ').split(' ')[0]
    return date.fromisoformat(formatted)


class NZCovid19Lit:
    def __init__(self, url_to_nz_covid19_lit, path_to_data, seconds_before_next_update):
        self._url_to_nz_covid19_lit = url_to_nz_covid19_lit
        self._path_to_data = path_to_data
        self._seconds_before_next_update = seconds_before_next_update

        self._root = load_from_file(path_to_data)

        if 'error' in self._root:
            self.refresh_data()
            self.clear_filters()
            return

        if not self.is_recent():
            self.refresh_data()
            self.clear_filters()
            return

        self._filtered = dict(self._root['data'])
        print(self._filtered)

    def is_recent(self):
        data_timestamp = datetime.fromisoformat(self._root['timestamp'])
        now = datetime.now(timezone.utc)
        if (now - data_timestamp).total_seconds() >= self._seconds_before_next_update:
            return False
        return True

    def refresh_data(self):
        latest_data = get_data(self._url_to_nz_covid19_lit)
        now = datetime.now(timezone.utc)
        data_timestamp = datetime.isoformat(now)
        self._root['timestamp'] = data_timestamp
        self._root['data'] = latest_data
        save_to_file(self._path_to_data, self._root)

    def fetch(self):
        return self._filtered

    def clear_filters(self):
        self._filtered = dict(self._root['data'])

    def filter_by_date(self, start_date_string, end_date_string):
        entries = {'items': []}
        target_start_date = get_date_from_string(start_date_string)
        target_end_date = get_date_from_string(end_date_string)
        for item in self._filtered['items']:
            item_start_date = get_date_from_string(item['startDateTime'])
            item_end_date = get_date_from_string(item['endDateTime'])
            if not(target_end_date < item_start_date or target_start_date > item_end_date):
                entries['items'].append(item)
        self._filtered = dict(entries)
        return self._filtered

    def filter_by_location_name(self, location_name, exact=False):
        return self.__filter_by_attribute('eventName', location_name, exact)

    def filter_by_exposure_type(self, exposure_type, exact=False):
        return self.__filter_by_attribute('exposureType', exposure_type, exact)

    def filter_by_latitude(self, latitude_start_string, latitude_end_string):
        return self.__filter_by_location_attribute_float('latitude', latitude_start_string, latitude_end_string)

    def filter_by_longitude(self, longitude_start_string, longitude_end_string):
        return self.__filter_by_location_attribute_float('longitude', longitude_start_string, longitude_end_string)

    def filter_by_suburb(self, suburb, exact=False):
        return self.__filter_by_location_attribute('suburb', suburb, exact)

    def filter_by_city(self, city, exact=False):
        return self.__filter_by_location_attribute('city', city, exact)

    def filter_by_address(self, address, exact=False):
        return self.__filter_by_location_attribute('address', address, exact)

    def list_location_names(self):
        entry = {'locations': self.__list_attribute('eventName')}
        return entry

    def list_exposure_types(self):
        entry = {'exposureTypes': self.__list_attribute('exposureType')}
        return entry

    def list_suburbs(self):
        entry = {'suburbs': self.__list_location_attribute('suburb')}
        return entry

    def list_cities(self):
        entry = {'cities': self.__list_location_attribute('city')}
        return entry

    def list_addresses(self):
        entry = {'addresses': self.__list_location_attribute('address')}
        return entry

    def __filter_by_attribute(self, attribute_key, attribute_value, exact):
        entries = {'items': []}
        target_attribute = attribute_value.lower()
        for item in self._filtered['items']['items']:
            item_attribute = item[attribute_key].lower()
            if exact and target_attribute == item_attribute \
                    or not exact and target_attribute in item_attribute:
                entries['items'].append(item)
        self._filtered = dict(entries)
        return self._filtered

    def __filter_by_location_attribute_float(self, location_attribute_key,
                                             location_attribute_value_start, location_attribute_value_end):
        entries = {'items': []}
        target_attribute_value_start = float(location_attribute_value_start)
        target_attribute_value_end = float(location_attribute_value_end)
        for item in self._filtered['items']['items']:
            if not item['location'][location_attribute_key]:
                continue
            item_attribute = float(item['location'][location_attribute_key])
            if target_attribute_value_start <= item_attribute <= target_attribute_value_end:
                entries['items'].append(item)
        self._filtered = dict(entries)
        return self._filtered

    def __filter_by_location_attribute(self, location_attribute_key, location_attribute_value, exact):
        entries = {'items': []}
        target_location_attribute = location_attribute_value.lower()
        for item in self._filtered['items']['items']:
            item_location_attribute = item['location'][location_attribute_key].lower()
            if exact and target_location_attribute == item_location_attribute\
                    or not exact and target_location_attribute in item_location_attribute:
                entries['items'].append(item)
        self._filtered = dict(entries)
        return self._filtered

    def __list_attribute(self, attribute_key):
        entries = set()
        for item in self._filtered['items']['items']:
            entry_formatted = item[attribute_key].strip()
            if not entry_formatted:
                continue
            entries.add(entry_formatted)
        entries_list = list(entries)
        entries_list.sort()
        return entries_list

    def __list_location_attribute(self, location_attribute_key):
        entries = set()
        for item in self._filtered['items']['items']:
            entry_formatted = item['location'][location_attribute_key].strip()
            if not entry_formatted:
                continue
            entries.add(str(entry_formatted))
        entries_list = list(entries)
        entries_list.sort()
        return entries_list
