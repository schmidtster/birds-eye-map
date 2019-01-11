This program reads through every record in the Clements Library Image Bank and filters them by whether or not they have a project name "Bird's-Eye View Project" in the metadata. The only records that have those fields (as of 7/24/2018) are Bird's-
Eye Views. Included are comments for each line that explains the purpose of the line, in case anyone who is not familiar with coding wants to understand what is happening. The regular expressions, genre set, and part of the conversion from json to geojson were written by Tyler Brockmeyer, a computer science undergraduate at MO S&T.

#!/bin/bash

import json
import requests
import codecs
from datetime import datetime, timezone
import sys
import re
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
# All of the above imports are necessary to running the program. These ensure the json import, requests (for getting data from the Image Bank API), codecs (for when windows has been funky with them in the past), datetime (using for a unique identifier), sys for codec support (again for Windows), and re (regular expression - written as variable title_regex and date_regex for standardizing the titles and dates of records). Make sure to install requests and datetime to your BASH (i.e. GitBash)

title_regex = re.compile(r"([^:/\n]*).*") # This regular expression standardizes the titles for each record. It looks for colons in the title and eliminates them and everything past that. Basically, it eliminates the subtitles
date_regex = \
    re.compile(r"((?:approximately )?(?:after )?[\d-]{4}(?:-[\d-]{4})?|between [\d-]{4} and [\d-]{4}).*") # This regular expression standardizes the dates for each record. It looks for words such as approximately, after, between, and and to keep those within the date field, but eliminates everything else, such as repetitive dates, unnecessary punctuation, etc.
genres_regex = re.compile(r"['A-Za-z-]+(?: ['A-Za-z-]+)*") # This regular expression standardizes the genre terms. It looks for all words and excludes any dates.

# This takes the data from the API and makes each record a class instance.
class ImageRecord(object):

    def __init__(self, input_dictionary):

        date_ranges = {"1700-1799": range(1700, 1800), "1800-1819": range(1800, 1820), "1820-1839": range(1820, 1840),
                       "1840-1859": range(1840, 1860), "1860-1879": range(1860, 1880), "1880-1900": range(1880, 1901),
                       "1901-2000": range(1901, 2000)} # This class variable is consistent for every individual instance(record). It is meant to set date ranges for each record. See below under Begin date range.

        self.title = ''
        self.date = ''
        self.creator = ''
        self.longitude = ''
        self.latitude = ''
        self.genres = set()
        self.image_bank_url = ''
        self.thumbnail_base_url = ''
        self.date_range = '' # All of the above sets our class instances

        for individual_record in input_dictionary['metadata']: # Iterates through each metadata dictionary for each record

            if individual_record['field'] == 'wcl1ic_it': # If there is a dictionary with a field who's value is wcl1ic_it
                title = individual_record['value'] # Take the value of the value key (aka the actual title)
                match = title_regex.match(title) # Perform our regex match on it with the .match method
                if match: # If regex ran successfully
                    self.title = match.group(1).strip() # Assign self.title the regex'd title and strip any extra spaces from the title at the end
                else: # If regex wasn't compatible
                    self.title = title # Assign the title as is in the metadata field
                    print("Error: title_regex non-match [{}]".format(title)) # Print an error saying this title didn't match regex's parameters

            elif individual_record['field'] == 'wcl1ic_da': # If there is a dictionary with a field who's value is wcl1ic_da
                date = individual_record['value'] # Assign the value of the value key (aka the actual date)
                match = date_regex.match(date) # Perform our regex match to check for compatibility
                if match: # If date compatible
                    self.date = match.group(1) # Run our regex on the date and assign it to self.date
                else: # If regex wasn't compatible
                    self.date = date # Assign the date as is in the metadata field
                    print("Error: date_regex non-match [{}]".format(date)) # Print an error saying this date didn't match regex's parameters
                # Begin date range * This will check to make sure all date ranges that are applicable to each date are selected. So if there is a date with more than 1 date range (ex. between 1858 and 1865), this will add 2 date ranges ("1840-1859", "1860-1879") to self.date_range.
                re_date_list = re.findall(r'([\d]{4})', date) # This runs a small regex function over the date, extracting all dates and excluding everything else. We use the findall method that returns a list of all dates.
                ranges_per_record = [] # Create an empty list where we will store all our date ranges that we find.
                if len(re_date_list) > 0: # if there are more than 0 items in our re_date_list (i.e. re_date_list = ['1880', '1900']).
                    for every_date in re_date_list: # We begin iterating through each individual date found in re_date_list, saving each one as every_date.
                        for key, value in date_ranges.items(): # We go through every key,value pair in our date_ranges dictionary as above.
                            for each_year in value: # Because the value of every key in date_ranges is a range of numbers, this for loop will iterate through each number in that range, saving it as each_year.
                                if int(every_date) == each_year: # If the integer of every_date (because it is saved as a string in re_date_list, so we have to convert it to an integer) matches each_year (which is already an integer).
                                    if key not in ranges_per_record: # If the key associated with that value (i.e. "1700-1799", etc.) is not already in our ranges_per_record list.
                                        ranges_per_record.append(key) # Append the key (i.e. "1700-1799", etc.) to our ranges_per_record list.
                    self.date_range = tuple(ranges_per_record) # Convert the list to a tuple and assign it to our class attribute self.date_range.
                else: # If re_date_list is empty (meaning the regex did not successfully run).
                    self.date_range = date # Assign just the date to attribute self.date_range
                    print("Error: date_range_regex non-match [{}]".format(date)) # Print an error saying the regex did not match and the date.

            elif individual_record['field'] == 'wcl1ic_cr': # If there is a dictionary with a field who's value is wcl1ic_cr
                self.creator = individual_record['value'] # Take the value of the value key (aka the actual creator) and assign it to self.creator

            elif individual_record['field'] == 'wcl1ic_long': # If there is a dictionary with a field who's value is wcl1ic_long
                self.longitude = individual_record['value'] # Take the value of the value key (aka the actual longitude) and assign it to self.longitude

            elif individual_record['field'] == 'wcl1ic_lat': # If there is a dictionary with a field who's value is wcl1ic_lat
                self.latitude = individual_record['value'] # Take the value of the value key (aka the actual latitude) and assign it to self.latitude

            elif individual_record['field'] == 'wcl1ic_g': # If there is a dictionary with a field who's value is wcl1ic_g
                if isinstance(individual_record['value'], list): # If the value of the genres field is a list of genres
                    for genre in individual_record['value']: # Assign the value of the value key (aka the actual genre)
                        match = genres_regex.match(genre) # Perform our regex to match on it with the .match method
                        if match: # If regex ran successfully
                            self.genres.add(match.group(0)) # Assign self.genres the regex'd genre.
                        else: # If regex didn't run successfully
                            self.genres = genre # Assign the genre as it is in the metadata field
                            print("Error: date_regex non-match [{}]".format(genre)) # Print an error saying this title didn't match regex's parameters
                elif isinstance(individual_record['value'], str): # If the value of the genres field is a string (there is only 1 genre)
                    match = genres_regex.match(individual_record['value']) # Perform our regex to match on it with the .match method
                    if match: # If regex ran successfully
                        self.genres.add(match.group(0)) # Assign self.genres the regex'd genre.
                    else: # If regex didn't run successfully
                        self.genres = individual_record['value'] # Assign the genre as it is in the metadata field
                        print("Error: date_regex non-match [{}]".format(individual_record['value'])) # Print an error saying this title didn't match regex's parameters
                else: # If the value of genre is empty or anything but a list or string
                    self.genres = individual_record['value'] # Assign the genre as it is in the metadata field
                    print("Error: date_regex non-match [{}]".format(individual_record['value'])) # Print an error saying this title didn't match regex's parameters

        if "@id" in input_dictionary['images'][0]['resource']: # If there is a key "@id" within ['images'][0]['resources']
            self.image_bank_url = input_dictionary['images'][0]['resource']['@id'] # Assign it's value to self.image_bank_url

        if "@id" in input_dictionary['images'][0]['resource']['service']: # If there is a key "@id" within ['images'][0]['resources']['service']
            self.thumbnail_base_url = input_dictionary['images'][0]['resource']['service']['@id'] # Assign it's value to self.thumbnail_base_url

    def get_thumbnail_url(self): # This method will take the base url we got from the record and convert it to a string url that can be displayed as a thumbnail
        thumbnail_str_att = "/full/!250,250/0/default.jpg" # This is the iiif ending string that will take a url and turn it into a usable thumbnail
        base_url = self.thumbnail_base_url # Assign the thumbnail_base_url value to the variable base_url
        complete_thumbnail_url = base_url + thumbnail_str_att # Combine the base url and thumbnail string to form the complete url
        return complete_thumbnail_url # return the completed url

    def to_geojson(self): # This method will take the data for each record and convert it to a geojson format
        longitude, latitude = map(float, (self.longitude, self.latitude)) # Convert the long and lat #s into floats (they default to strings, which cannot be read by geojson) and assign the values of both to variables Longitude and Latitude
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
        } # This is the structure of geojson. Just plug in the instances where needed
        return feature # Return feature, a dictionary structured in geojson


collections_dictionary = {} # collections_dictionary will hold all the information about every record in the Image Bank

print("Gathering records...", end='', flush=True) # Adds a little dialog when the program runs, saying it is working
# The following grabs the data
image_bank_search_query = "https://quod.lib.umich.edu/cgi/i/image/api/search/wcl1ic?offset=500" # This sets our initial search query parameter. We will overwrite it later on in our while loop.
while True # Initializes our while loop. The following will keep running until we use break to stop the loop.
    unique_id = datetime.now(timezone.utc).astimezone().isoformat() # This creates a unique id for each request. The id is simply the time the request was made in the iso format (it includes time down to the second)
    collections_request = requests.get(image_bank_search_query) # This makes the request to the image bank
    collections_request_text = collections_request.text # This converts the request to text, to be readable via json
    collections_request_dict = json.loads(collections_request_text) # This loads the string of the text into the variable
    collections_dictionary[unique_id] = collections_request_dict # This inputs the data into the collections_dictionary with unique id of current date and time (in ISO format)
    if "next" in collections_dictionary[unique_id]: # This looks for the "next" key in the recently added data. The Image Bank API is limited to a search query of 500 records per query. The "next" key means there are more records that can be queried.
        image_bank_search_query = collections_dictionary[unique_id]['next'] # This resets the variable image_bank_search_query with the value of "next". It defaults to the next 500 records, i.e. offset=1000, offset=1500, etc.
    else:
        break # If there is no "next" key in the most recent data query, that means there are no more records to be queried. This breaks the while loop (Aka, it prevents an infinite loop of requests).

print("Done.") # This finishes the little dialog we added at the top, signifying that the program got the data.
print("Writing GeoJson file...", end='', flush=True) # Adds a little dialog when the program runs, saying it is working

lat_long_records = [] # This list will hold all the records with latitude and longitude metadata
genres = set() # This set will hold all genres that are listed in the metadata for each record with lat and long
creators = set() # This set will hold all the creators that are listed in the metadata for each record with lat and long
# This looks through the data, looking for the existence of project name = "Bird's-Eye View Project" in the metadata for each record in the image bank.
for each_request in collections_dictionary.values(): # This goes through each request we made from the Image Bank
    for item_record in collections_dictionary[unique_id]['sequences'][0]['canvases']: # This goes through each individual record we pulled from the Image Bank
        for each_md_dict in item_record['metadata']: # This checks each metadata dictionary for each record
        	if each_md_dict['field'] == 'wcl1ic_pn': # If the project name (pn) field exists
                if each_md_dict['value'] == 'Bird's-Eye View Project': # If the value of project name field is Bird's-Eye View Project
                    record = ImageRecord(item_record) # Then make a class instance of that entire record
                    if record.creator not in creators: # If the creator of the record is not in our creators set above
                        creators.add(record.creator) # Add the creator to our creator set
                    for each_genre in record.genres: # Now, for each genre term in the list of genres found in the metadata
                        if each_genre not in genres: # and if those terms are not already in our genres set
                            genres.add(each_genre) # add those genre terms to our global genres set
                    lat_long_records.append(record) # add the records with lat and long into our list

genres_sort = sorted(genres) # This sorts the genres set alphabetically
creators_sort = sorted(creators) # This sorts the creators set alphabetically

with open("map-v2.geojson", "w") as GEOJSON_FILE: # This creates a file and allows us to write to that file ('as GEOJSON_FILE' simply assigns the opened file to the variable named GEOJSON_FILE)
    records = {'features': [r.to_geojson() for r in lat_long_records],
        'type': 'FeatureCollection'
    } # this converts our json to geojson by first creating a 'features' key (req by geojson), then the value of that is a list of each record that is converted from json in our lat_long_records to geojson via our class method to_geojson(). Then it adds the key-value pair 'type': 'FeatureCollection' at the end of the conversion, as is required by geojson
    json.dump(records, GEOJSON_FILE, indent=2) # We dump the converted geojson into our GEOJSON_FILE, meaning we write the data to the file, and we use optional parameter indent to make it look readable

print("Done") # This finishes the dialog we added above.
print("Writing tags file...", end='', flush=True) # Another dialog statement

with open("tags.json", "w") as f: # Here, we are creating and opening a file, tags.json. This is used to generate our tags we will use with our tag filter button in the leaflet html file
    json.dump({ # Dump the json formatted data
        "genres": list(genres_sort), # Create a key named genres and assign the value of our genres global sorted set (which we turn into a list to make it readable). Will be used for our tag filter button.
        "creators": list(creators_sort), # Create a key named creators and assign the value of our creators global sorted set (which we turn into a list to make it readable). Will be used for our tag filter button.
        "date_ranges": ["1700-1799", "1800-1819", "1820-1839", "1840-1859", "1860-1879", "1880-1900", "1901-2000"] # Create a key named date_ranges and assign it a list of date ranges that will be used in our tag filter button.
    }, f) # f is our variable, which is acting as our file, so we are dumping the data to f

print("Done") # Print a dialog saying writing the tags.json file is done
