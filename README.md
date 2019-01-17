### Live site:

http://clements.umich.edu/exhibits/online/birdseye/birdseye.php

### Description

This program takes the Clements Library Image Bank API, extracts information about all the images that have the project 
name "Bird's-Eye View Project", generates a .geoJSON file, initializes a Leaflet map, and plots points with information 
for each bird's-eye view captured. The project contains a python file that handles the data extraction from the API. An 
HTML file structures the map for display. Two JavaScript files ingest the information from the geoJSON file and 
enables the MarkerCluster plugin to be compatible with the Leaflet Tag Filter Button.

This project uses Python 3.7, Leaflet 1.3.3, and jQuery 3.3.1, as well as the following plugins:

MarkerCluster 1.3.0 - https://github.com/Leaflet/Leaflet.markercluster;
Leaflet Tag Filter Button 0.0.4 - https://github.com/maydemirx/leaflet-tag-filter-button;
ZoomHome - https://github.com/torfsen/leaflet.zoomhome;
Leaflet Fullscreen 1.0.1 - https://github.com/Leaflet/Leaflet.fullscreen;
Fontawesome 5.2.0 - https://fontawesome.com/;
Leaflet Easybutton - https://github.com/CliffCloud/Leaflet.EasyButton.


### Structure

##### image_bank_request_api.py
Requirements: Python3, json, requests, codecs, datetime, timezone, sys, re. See requirements.txt for full list.

Description: The file makes a request to the Clements Library Image Bank API to get all the images in the repository and 
filters each one if it has the project name "Bird's-Eye View Project". Each record is then passed through the class 
ImageRecord, where it has the get_thumbnail method that generates thumbnail urls for each record and the to_geojson 
method that structures each record in the geojson format. It then writes each class instance to a geojson file and
takes all the genres, creators, and date-ranges collected from the class instances and writes that information into the 
tags.json file.

Instructions: Open a terminal and using python3, run the program. It will generate two files: map-v2.geojson and 
tags.json. map-v2.geojson is the information for Leaflet to display each bird's-eye view. tags.json is used for the 
Tag filter buttons plugin.

##### leaflet_text_2.html
Requirements: None

Description: Displays the leaflet map. It contains plugins with local references commented out in case the cdns go down 
or stop working, for whatever reason. CSS styles are outlined primarily to fit the map with 100% height (fill whatever 
contains it) and stylings for the Leaflet Tag Filter buttons. References to enableMCG.js and map.js scripts are 
enabled under the div "bev_map".

Instructions: Make sure enableMCG.js, map.js, map-v2.geojson and tags.json are all in the same directory as the html 
file.

##### map.js
Requirements: None

Description: This file initializes the leaflet map, as well as 3 tag filter buttons for genre, creator, and date and
the various plugins (zoomhome, fullscreen, markercluster). It also provides a solution to make popups move the map to 
fit the entire popup (see https://stackoverflow.com/questions/51732698/leaflet-popup-update-resizing-solution-recreating-a-popup-everytime-unable 
for more details).

Instructions: Make sure enableMCG.js, leaflet_text_2.html, map-v2.geojson and tags.json are all in the same directory 
as the html file.

##### enableMCG.js
Requirements: None

Description: This enables the Leaflet Tag Filter button to take a MarkerClusterGroup layer and filter that layer
instead of the default layer. See 
https://stackoverflow.com/questions/51770138/leaflet-tag-filter-button-and-markercluster-layersupport-plugins-integration-t 
for more details.

Instructions: Make sure map.js, leaflet_text_2.html, map-v2.geojson and tags.json are all in the same directory 
as the html file.

##### map-v2.geojson
Requirements: None

Description: This file is structured to be compatible with Leaflet's acceptable file formats. This file is generated 
through the image_bank_request_api.py file. It requires a specific structure, which you can read more about here:
http://geojson.org/

Instructions: Make sure enableMCG.js, map.js, leaflet_text_2.html, and tags.json are all in the same directory as the 
html file.

##### tags.json
Requirements: None

Description: A simple json file containing a dictionary with keys for genres, creators, and date-ranges, whose values
are lists. Used for Leaflet Tag Filter Button.

Instructions: Make sure enableMCG.js, map.js, leaflet_text_2.html, and map-v2.geojson are all in the same directory as the 
html file.

### Appendix

Two README’s, one for image_bank_request_api.py and one for leaflet_text_2.html, detail what each line of the file does through comments. It should be noted that both enableMCG.js and map.js were a part of leaflet_text_2.html but were 
moved into separate files to make it easier to read.


