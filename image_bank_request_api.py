#!/bin/bash

import json
import requests
import codecs
from datetime import datetime, timezone
import sys
import re

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

title_regex = re.compile(r"([^:/\n]*).*")
date_regex = re.compile(r"((?:(?:approximately|after|between) )*\d{4}(?:(?:-| and )\d{4})?).*")
genres_regex = re.compile(r"['A-Za-z-]+(?: ['A-Za-z-&]+)*")


class ImageRecord(object):

    def __init__(self, input_dictionary):

        date_ranges = {"1700-1799": range(1700, 1800), "1800-1819": range(1800, 1820), "1820-1839": range(1820, 1840),
                       "1840-1859": range(1840, 1860), "1860-1879": range(1860, 1880), "1880-1900": range(1880, 1901),
                       "1901-2000": range(1901, 2000)}

        self.title = ''
        self.date = ''
        self.creator = ''
        self.longitude = ''
        self.latitude = ''
        self.genres = set()
        self.image_bank_url = ''
        self.thumbnail_base_url = ''
        self.date_range = ''

        for individual_record in input_dictionary['metadata']:

            if individual_record['field'] == 'wcl1ic_it':
                title = individual_record['value']
                match = title_regex.match(title)
                if match:
                    self.title = match.group(1).strip()
                else:
                    self.title = title
                    print("Error: title_regex non-match [{}]".format(title))

            elif individual_record['field'] == 'wcl1ic_da':
                date = individual_record['value']
                match = date_regex.match(date)
                if match:
                    self.date = match.group(1)
                else:
                    self.date = date
                    print("Error: date_regex non-match [{}]".format(date), individual_record)
                # Begin date range
                re_date_list = re.findall(r'([\d]{4})', date)
                ranges_per_record = []
                if len(re_date_list) > 0:
                    for every_date in re_date_list:
                        for key, value in date_ranges.items():
                            for each_year in value:
                                if int(every_date) == each_year:
                                    if key not in ranges_per_record:
                                        ranges_per_record.append(key)
                    self.date_range = tuple(ranges_per_record)
                else:
                    self.date_range = date
                    print("Error: date_range_regex non-match [{}]".format(date))

            elif individual_record['field'] == 'wcl1ic_cr':
                self.creator = individual_record['value']

            elif individual_record['field'] == 'wcl1ic_long':
                self.longitude = individual_record['value']

            elif individual_record['field'] == 'wcl1ic_lat':
                self.latitude = individual_record['value']

            elif individual_record['field'] == 'wcl1ic_g':
                if isinstance(individual_record['value'], list):
                    for genre in individual_record['value']:
                        match = genres_regex.match(genre)
                        if match:
                            self.genres.add(match.group(0))
                        else:
                            self.genres = genre
                            print("Error: date_regex non-match [{}]".format(genre))
                elif isinstance(individual_record['value'], str):
                    match = genres_regex.match(individual_record['value'])
                    if match:
                        self.genres.add(match.group(0))
                    else:
                        self.genres = individual_record['value']
                        print("Error: date_regex non-match [{}]".format(individual_record['value']))
                else:
                    self.genres = individual_record['value']
                    print("Error: date_regex non-match [{}]".format(individual_record['value']))

        if "@id" in input_dictionary['images'][0]['resource']:
            self.image_bank_url = input_dictionary['images'][0]['resource']['@id']

        if "@id" in input_dictionary['images'][0]['resource']['service']:
            self.thumbnail_base_url = input_dictionary['images'][0]['resource']['service']['@id']

    def get_thumbnail_url(self):
        thumbnail_str_att = "/full/!250,250/0/default.jpg"
        base_url = self.thumbnail_base_url
        complete_thumbnail_url = base_url + thumbnail_str_att
        return complete_thumbnail_url

    def to_geojson(self):
        longitude, latitude = map(float, (self.longitude, self.latitude))
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [longitude, latitude],
            },
            'properties': {
                'Title': self.title,
                'Date': self.date,
                'Creator': self.creator,
                'Image_Bank_URL': self.image_bank_url,
                'Thumbnail_URL': self.get_thumbnail_url(),
                'Genres': list(self.genres),
                'Date_Range': self.date_range
            }
        }
        return feature


collections_dictionary = {}

print("Gathering records...", end='', flush=True)

image_bank_search_query = "https://quod.lib.umich.edu/cgi/i/image/api/search/wcl1ic?offset=500"
while True:
    unique_id = datetime.now(timezone.utc).astimezone().isoformat()
    collections_request = requests.get(image_bank_search_query)
    collections_request_text = collections_request.text
    collections_request_dict = json.loads(collections_request_text)
    collections_dictionary[unique_id] = collections_request_dict
    if "next" in collections_dictionary[unique_id]:
        image_bank_search_query = collections_dictionary[unique_id]['next']
    else:
        break

print("Done.")
print("Writing GeoJson file...", end='', flush=True)

lat_long_records = []
genres = set()
creators = set()
for each_request in collections_dictionary.values():
    for item_record in each_request['sequences'][0]['canvases']:
        for each_md_dict in item_record['metadata']:
            if each_md_dict['field'] == 'wcl1ic_pn':
                if each_md_dict['value'] == "Bird's-Eye View Project":
                    record = ImageRecord(item_record)
                    if record.creator not in creators:
                        creators.add(record.creator)
                    for each_genre in record.genres:
                        if each_genre not in genres:
                            genres.add(each_genre)
                    lat_long_records.append(record)

genres_sort = sorted(genres)
creators_sort = sorted(creators)

save_path = ""
with open("map-v2.geojson", "w") as GEOJSON_FILE:
    records = {'features': [r.to_geojson() for r in lat_long_records],
               'type': 'FeatureCollection'
               }
    json.dump(records, GEOJSON_FILE, indent=2)

print("Done")
print("Writing tags file...", end='', flush=True)

with open("tags.json", "w") as f:
    json.dump({
        "genres": list(genres_sort),
        "creators": list(creators_sort),
        "date_ranges": ["1700-1799", "1800-1819", "1820-1839", "1840-1859", "1860-1879", "1880-1900", "1901-2000"]
    }, f)

print("Done")
