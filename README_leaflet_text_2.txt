This map imports data from the image_bank_request_api.py program - specifically map-v2.geojson and tags.json - and displays them on a map of the United States. The intent is to present bird's-eye views of American cities found within the Clements Library Image Bank on a dynamic and interactive map. The following is the source code with explanations.

<!DOCTYPE html>
<html lang="en"> Set the html to read in English.
<head>
  <meta charset="utf-8"/> Set the character set for UTF-8 for compatibility.
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Bird's-Eye Views - William H. Clements Library</title>
  <!-- The following are references to leaflet, jQuery, and assorted plugins used to make the map. Consult the plugins' github pages for more information -->
  <!-- jQuery -->
  <script src="https://code.jquery.com/jquery-3.3.1.js"
  integrity="sha256-2Kok7MbOyxpgUVvAk/HJ2jigOSYS2auK4Pfzbm7uH60="
  crossorigin="anonymous"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js" integrity="sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI/8aZajjp4Bqd+V6D5IgvKT" crossorigin="anonymous"></script>
  <script>window.jQuery || document.write('<script src="jQuery 3.3.1/jquery-3.3.1.js">/x3C/script>')</script>
  <script>window.jQuery || document.write('<script src="jQuery 3.3.1/jquery-3.3.1.min.js">/x3C/script>')</script>

  <!-- Leaflet -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.3.3/leaflet.css" media="screen, print" rel="stylesheet" integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
  crossorigin="">
  <script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.3.3/leaflet.js' integrity="sha512-tAGcCfR4Sc5ZP5ZoVz0quoZDYX5aCtEm/eu1KhSLj2c9eFrylXZknQYmxUssFaVJKvvc0dJQixhGjG2yXWiV9Q=="
  crossorigin=""></script>
  <!-- In case of cdn breaking, uncomment this section. It will reference the local files on the server: -->
  <!-- <link href="leaflet/leaflet.css" media="screen, print" rel="stylesheet" />
  <script type='text/javascript' src='leaflet/leaflet.js'></script> -->

  <!-- MarkerCluster Plugin -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.3.0/MarkerCluster.css" integrity="sha384-lPzjPsFQL6te2x+VxmV6q1DpRxpRk0tmnl2cpwAO5y04ESyc752tnEWPKDfl1olr" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.3.0/MarkerCluster.Default.css" integrity="sha384-5kMSQJ6S4Qj5i09mtMNrWpSi8iXw230pKU76xTmrpezGnNJQzj0NzXjQLLg+jE7k" crossorigin="anonymous">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.3.0/leaflet.markercluster.js" integrity="sha384-1artbd0pdGdZ72+IcKWkY1So1xu4Hzygfd0cVLSs7f5lBZZ/FhyEZc4UyQR3DT9c" crossorigin="anonymous"></script>
  <!-- If markercluster goes down, uncomment the section below. It will reference the local files on the server: -->
  <!-- <link rel="stylesheet" type="text/css" href="Leaflet.markercluster-master/Leaflet.markercluster-master/dist/MarkerCluster.css" />
  <link rel="stylesheet" type="text/css" href="Leaflet.markercluster-master/Leaflet.markercluster-master/dist/MarkerCluster.Default.css" />
  <script src="Leaflet.markercluster-master/Leaflet.markercluster-master/dist/leaflet.markercluster.js"></script> -->

  <!-- tagFilterButton Plugin -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button@0.0.4/src/leaflet-tag-filter-button.css" integrity="sha384-qk0hbOre/j9o7RPo7Gehr1T2jE3qRUXoCmJh3ze+Tk4JwTMDA+990SJd4Tl+m75W" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button@0.0.4/src/leaflet-tag-filter-button.js" integrity="sha384-J0V5vQ3gXq22fIvuL0ugbCm6pCJ+rKpDnX5BdlofJBdqvNOWWjQeDIr16xyypYBz" crossorigin="anonymous"></script>
  <!-- In case of cdn breaking, uncomment the section below. It will reference the local files on the server: -->
  <!-- <link rel="stylesheet" href="leaflet-tag-filter-button-master/leaflet-tag-filter-button-master/src/leaflet-tag-filter-button.css" />
  <script src="leaflet-tag-filter-button-master/leaflet-tag-filter-button-master/src/leaflet-tag-filter-button.js"></script> -->

  <!-- zoomHome plugin (replaces default leaflet zoom button in top left of screen) -->
  <link rel="stylesheet" href="leaflet.zoomhome-master/leaflet.zoomhome-master/dist/leaflet.zoomhome.css"/>
  <script src="leaflet.zoomhome-master/leaflet.zoomhome-master/dist/leaflet.zoomhome.min.js"></script>

  <!-- Fullscreen Plugin-->
  <link rel="stylesheet" href="https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css" integrity="sha384-t17w2haSDwLp3KSAOHF7+VI9q2maRMLDhnIyU/JasjeWyxcN3YOcrD7T95CiJSWE" crossorigin="anonymous">
  <script src="https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js" integrity="sha384-btJhAWztz7ttA6ibFC5ppM39nkCPK6CWzRVmsaLcDn37mA3x1TzF1DbFwa6tJpTN" crossorigin="anonymous"></script>
  <!-- In case of cdn breaking, uncomment the section below. It will reference the local files on the server: -->
  <!-- <link href='Leaflet.fullscreen-gh-pages/Leaflet.fullscreen-gh-pages/dist/leaflet.fullscreen.css' rel='stylesheet' />
  <script src='Leaflet.fullscreen-gh-pages/Leaflet.fullscreen-gh-pages/dist/leaflet.fullscreen.js'></script> -->

  <!-- fontawesome (used for extra icons) -->
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" type='text/css' integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ" crossorigin="anonymous">
  <!-- In case of cdn breaking, uncomment the section below. It will reference the local files on the server: -->
  <!-- <link href="fontawesome-free-5.2.0-web/fontawesome-free-5.2.0-web/css/all.css" rel="stylesheet" /> -->

  <!-- EasyButton Plugin (compatibility for tagFilterButton) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css" integrity="sha384-iNk4bdiUuP4VWx8c4KVwk07wshEQVvAe/8xwpcNR/5anLhH9SFPHkjLSXAwGwXKC" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js" integrity="sha384-GHKGgc0qNzZZpBzGWvVZWSRFNB+LYy8aJCBtgI0IpWul99UCBQcSP85Z9RLAorB/" crossorigin="anonymous"></script>
  <!-- In case of cdn breaking, uncomment the section below. It will reference the local files on the server: -->
  <!-- <link rel="stylesheet" href="Leaflet.EasyButton-master/Leaflet.EasyButton-master/src/easy-button.css" />
  <script src="Leaflet.EasyButton-master/Leaflet.EasyButton-master/src/easy-button.js"></script> -->


<style type="text/css"> The following are specific css stylings I made to adjust the map and filter buttons.
/* sets the map size to fit the screen it is in (found from lyzidiamond.com/posts/osgeo-august-meeting)*/
  body { padding: 0; margin: 0;}
  html, body, #bev_map {height: 100%;} Sets the map to fill 100% of any frame it is given.

  .easy-button-button {
  display: block !important;} Is required to make the leaflet tag filter button to operate.

  .tag-filter-tags-container {
  margin-left: 40px;} Offsets the tag filter button list by 40px. The initial setting was the list of options overran the button itself.

  .custom .leaflet-popup-tip,
  .custom .leaflet-popup-content-wrapper {
  font-size: 17px;
  } Increases the font size of the text of the popups themselves.

  .leaflet-bar span.filter-info-box {
      white-space: pre-wrap;
  } Pre-wraps the text in the tag filter button list.

  .leaflet-bar .tag-filter-tags-container ul {
      border: 1px solid #000;
      width: 230px; margin: 0 auto;
      max-height: 250px;
  } Adjusts the width, height, and border size and color of the tag filter button list.

  .leaflet-bar .tag-filter-tags-container ul li a {
      font-size: 15px;
      font-family: "Helvetica Neue", Arial, Helvetica, sans-serif;
      color: #000000;
      display: inline;
  } Adjusts the text of the tag filter button list.

  .leaflet-bar .tag-filter-tags-container ul.header {
      border-top: 1px solid #000;
      border-bottom: 1px solid #000;
  } Adjusts the header ('clear') height, border, etc.

  .leaflet-bar .tag-filter-tags-container .checkbox {
      font-size: 15px;
      color: #000;
  } Adjusts the text size and color of the tag filter button list.

  .leaflet-bar .tag-filter-tags-container ul li {
      padding-left: 10px;
      border-bottom: 1px solid #000;
  } Adjusts the padding of the text and tag separator line color in the tag filter button list.

</style>

</head>

<body>

    <div id="bev_map"></div> Defines the map as "bev_map"


    <script src="enableMCG.js"></script> This references the following code that enables a MarkerCluster group.

    <script src="map.js"></script> This references the following code that builds the map and populates the data.

    This is not inlcuded, but a part of enableMCG.js and map.js files.
    <script>
    The following was concocted by ghybs from StackOverflow. It makes the tag filter button filter the marker clusters. I will not go line by line here, as it deals directly with the source code for the tag filter button. For more information on this, see: https://stackoverflow.com/questions/51770138/leaflet-tag-filter-button-and-markercluster-layersupport-plugins-integration-t
    ////////////////////////////////////////////////
    // Quick and dirty implementation of enableMCG
    ////////////////////////////////////////////////
    L.Control.TagFilterButton.include({
      // Goal: read from MCG instead of from _map
      enableMCG: function(mcgInstance) {
        this.registerCustomSource({
          name: 'mcg',
          source: {
            mcg: mcgInstance,
            hide: function(layerSource) {
              var releatedLayers = [];

              for (
                var r = 0; r < this._releatedFilterButtons.length; r++
              ) {
                releatedLayers = releatedLayers.concat(
                  this._releatedFilterButtons[r].getInvisibles()
                );
              }

              var toBeRemovedFromInvisibles = [],
                i,
                toAdd = [];

              for (var i = 0; i < this._invisibles.length; i++) {
                if (releatedLayers.indexOf(this._invisibles[i]) == -1) {
                  for (
                    var j = 0; j < this._invisibles[i].options.tags.length; j++
                  ) {
                    if (
                      this._selectedTags.length == 0 ||
                      this._selectedTags.indexOf(
                        this._invisibles[i].options.tags[j]
                      ) !== -1
                    ) {
                      //this._map.addLayer(this._invisibles[i]);
                      toAdd.push(this._invisibles[i]);
                      toBeRemovedFromInvisibles.push(i);
                      break;
                    }
                  }
                }
              }

              // Batch add into MCG
              layerSource.mcg.addLayers(toAdd);

              while (toBeRemovedFromInvisibles.length > 0) {
                this._invisibles.splice(
                  toBeRemovedFromInvisibles.pop(),
                  1
                );
              }

              var removedMarkers = [];
              var totalCount = 0;

              if (this._selectedTags.length > 0) {
                //this._map.eachLayer(
                layerSource.mcg.eachLayer(
                  function(layer) {
                    if (
                      layer &&
                      layer.options &&
                      layer.options.tags
                    ) {
                      totalCount++;
                      if (releatedLayers.indexOf(layer) == -1) {
                        var found = false;
                        for (
                          var i = 0; i < layer.options.tags.length; i++
                        ) {
                          found =
                            this._selectedTags.indexOf(
                              layer.options.tags[i]
                            ) !== -1;
                          if (found) {
                            break;
                          }
                        }
                        if (!found) {
                          removedMarkers.push(layer);
                        }
                      }
                    }
                  }.bind(this)
                );

                for (i = 0; i < removedMarkers.length; i++) {
                  //this._map.removeLayer(removedMarkers[i]);
                  this._invisibles.push(removedMarkers[i]);
                }

                // Batch remove from MCG
                layerSource.mcg.removeLayers(removedMarkers);
              }

              return totalCount - removedMarkers.length;
            },
          },
        });

        this.layerSources.currentSource = this.layerSources.sources[
          'mcg'
        ];
      },
    });

    ////////////////////////////////////////////////
    // Fix for TagFilterButton
    ////////////////////////////////////////////////
    L.Control.TagFilterButton.include({
      _prepareLayerSources: function() {
        this.layerSources = new Object();
        this.layerSources['sources'] = new Object();

        this.registerCustomSource({
          name: 'default',
          source: {
            hide: function() {
              var releatedLayers = [];

              for (var r = 0; r < this._releatedFilterButtons.length; r++) {
                releatedLayers = releatedLayers.concat(
                  this._releatedFilterButtons[r].getInvisibles()
                );
              }

              var toBeRemovedFromInvisibles = [],
                i;

              // "Fix": add var
              for (var i = 0; i < this._invisibles.length; i++) {
                if (releatedLayers.indexOf(this._invisibles[i]) == -1) {
                  // "Fix": add var
                  for (var j = 0; j < this._invisibles[i].options.tags.length; j++) {
                    if (
                      this._selectedTags.length == 0 ||
                      this._selectedTags.indexOf(
                        this._invisibles[i].options.tags[j]
                      ) !== -1
                    ) {
                      this._map.addLayer(this._invisibles[i]);
                      toBeRemovedFromInvisibles.push(i);
                      break;
                    }
                  }
                }
              }

              while (toBeRemovedFromInvisibles.length > 0) {
                this._invisibles.splice(toBeRemovedFromInvisibles.pop(), 1);
              }

              var removedMarkers = [];
              var totalCount = 0;

              if (this._selectedTags.length > 0) {
                this._map.eachLayer(
                  function(layer) {
                    if (layer && layer.options && layer.options.tags) {
                      totalCount++;
                      if (releatedLayers.indexOf(layer) == -1) {
                        var found = false;
                        for (var i = 0; i < layer.options.tags.length; i++) {
                          found =
                            this._selectedTags.indexOf(layer.options.tags[i]) !==
                            -1;
                          if (found) {
                            break;
                          }
                        }
                        if (!found) {
                          removedMarkers.push(layer);
                        }
                      }
                    }
                  }.bind(this)
                );

                for (i = 0; i < removedMarkers.length; i++) {
                  this._map.removeLayer(removedMarkers[i]);
                  this._invisibles.push(removedMarkers[i]);
                }
              }

              return totalCount - removedMarkers.length;
            },
          },
        });
        this.layerSources.currentSource = this.layerSources.sources['default'];
      },
    });
    Here begins building the map, markers, popup, and tag filter buttons.
    // initialize the map by assigning it a variable, map. zoomControl set to false because of zoomHome plugin replacement. scrollWheelZoom set to false in order to allow scroll wheel to work with tag filter button lists. fullscreenControlOptions sets the fullscreen button at the top left of the map. setView sets the center of the map and 4 is the initial zoom level.
    var map = L.map('bev_map', {zoomControl: false, scrollWheelZoom: false, fullscreenControl: true, fullscreenControlOptions: {
    position: 'topleft'}}).setView([38.00000, -97.00000], 4);

    Adds the zoomHome plugin to the map.
    var zoomHome = L.Control.zoomHome();
    zoomHome.addTo(map);

    // scrollWheelZoom defaults to true, but when false, prevents a user from using the scroll wheel to zoom in. .setView centers the map on a certain point. I have it here centered in Kansas. The 4 is the initial zoom value when loading the page. Increase it and the map will load closer to earth.

    // define a tile layer for the map, basically what sort of skin you want the map to have. Also set the min and max zoom feature here.
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', {attribution: 'Tiles &copy; Esri', maxZoom: 13, minZoom: 4}).addTo(map);

    Set a variable for custom options. This includes any changes we made to the popup style marked above via .custom. minWidth was set to 250 to ensure longer thumbnails could fit within the popup. className is set to the value custom (any changes made in our <style> portion marked with .custom)
    var customOptions = {
      'minWidth': '250',
      'className': 'custom'
    }

    // This part adds the points to the map and adds them as a marker cluster group variable, which we use later to filter via the tag filter buttons. $.getJSON is a jQuery method that extracts data from a file found within a directory to be used within the current program. It should be noted that for var marker, we add latlng and tags. These tags are found in the geoJSON for each marker and are used to filter markers via tag filter button.
    var clusters = L.markerClusterGroup({maxClusterRadius:75}).addTo(map); Set variable clusters = to markerClusterGroup with a max cluster radius of 75. Can adjust bigger or smaller. Default is 100? .addTo(map) adds it to the map.
    $.getJSON("map-v2.geojson",function(data){ Get the json data from map-v2.geojson and run function(data) to prepare for data extract.
      var bev = L.geoJson(data,{ Set var bev (birdseyeview) = to L.geoJSON - a function of leaflet to tell it to receive geoJSON data - (data,{ extract the data from map-v2.geojson
        pointToLayer: function(feature,latlng){ Add a layer with access to latlng coordinates and features (properties) of each marker.
          var marker = L.marker(latlng, { tags: feature.properties.Genres.concat(feature.properties.Creator)}); Assign var marker to L.marker - a leaflet function that creates a marker - (latlng - generates the marker, { tags: etc... - assign each marker tags based on Genres and Creator properties found within geoJSON data.
          marker.bindPopup('<p align=center>' + '<strong>Title: </strong>' + feature.properties.Title + '<br/><a href="' + feature.properties.Image_Bank_URL + '" target="_blank"><img src="' + feature.properties.Thumbnail_URL + '"/></a><br/>' + '<strong>Date: </strong>' + feature.properties.Date + '<br/>' + '<strong>Creator: </strong>' + feature.properties.Creator, customOptions); For every popup, align everything center, and extract Title, Image Bank URL, Thumbnail URL, Date, and Creator from the geoJSON file for each individual marker. The thumbnail url will have an embedded image bank url to be clickable by the user.
          return marker; Return the marker.
        }
      });
      bev.addTo(clusters); Add variable bev to clusters (this part adds every marker found within our geoJSON file to the marker cluster groups, which we can then display on the map).
    });

    // Here is the code block for the Tag Filter Button. I start by accessing a tags file that has the data that I use for filter options. This uses the same method as above with $.getJSON to get data from the tags.json. This part is only used to generate the list of options to filter by in the tag filter button.
    $.getJSON('tags.json', function(data) {
    var genres = L.control.tagFilterButton({ Set var genres = to control.tagFilterButton - this initializes the tag filter button for genres.
      data: data.genres, Set the list of filters as whatever data is found within the genres key in our tags.json file.
      filterOnEveryClick: true, Once a user clicks on the filter, it will immediately filter for that selection.
      icon: '<i class="fas fa-tags"></i>', This sets a unique icon for the button. Unique icon was from fontawesome free version.
    }).addTo(map); Add the button to the map.
    genres.enableMCG(clusters); This is a unique function that was made by ghybs (see above after <style>) that enables the markerclustergroup we assigned to our variable clusters to be filtered by the tag filter button.
    var creators = L.control.tagFilterButton({ Set var creators = to control.tagFilterButton - this initializes the tag filter button for creators.
      data: data.creators, Set the list of filters as whatever data is found within the creators key in our tags.json file.
      filterOnEveryClick: true, Once a user clicks on the filter, it will immediately filter for that selection.
      icon: '<i class="fas fa-user-edit"></i>', This sets a unique icon for the button. Unique icon was from fontawesome free version.
    }).addTo(map); Add the button to the map.
    creators.enableMCG(clusters); This is a unique function that was made by ghybs (see above after <style>) that enables the markerclustergroup we assigned to our variable clusters to be filtered by the tag filter button.
    The following makes the tag filter button work. Got from tag filter button github.
    var date_ranges = L.control.tagFilterButton({ Set var date_ranges = to control.tagFilterButton - this initializes the tag filter button
      data: data.date_ranges, Set the list of filters as whatever date is found within the date_ranges key in our tags.json file.
      filterOnEveryClick: true, Once a user clicks on the filter, it will immediately filter for that selection.
      icon: '<i class="fas fa-clock"></i>' This sets a unique icon for the button. Unique icon was from fontawesome free version.
    }).addTo(map); Add the button to the map.
    date_ranges.enableMCG(clusters); This is a unique function that was made by ghybs (see above after <style>) that enables the markerclustergroup we assigned to our variable clusters to be filtered by the tag filter button.
    jQuery('.easy-button-button').click(function() { The following enables the EasyButton functionality, required by the tag filter button.
		target = jQuery('.easy-button-button').not(this);
		target.parent().find('.tag-filter-tags-container').css({
			'display' : 'none',
		});
	});
  });
    The following is a solution made by ghybs to move the map to fit the entire popup on screen. This solution is not fullproof, as there are some markers, if they are too close to the top of the map, that will not force the map to adjust all the way to fit the popup within the screen. Solution was made here: https://stackoverflow.com/questions/51732698/leaflet-popup-update-resizing-solution-recreating-a-popup-everytime-unable
    document.querySelector(".leaflet-popup-pane").addEventListener("load", function(event) {
      var tagName = event.target.tagName,
        popup = map._popup;
      console.log("got load event from " + tagName);
      // Also check if flag is already set.
      if (tagName === "IMG" && popup && !popup._updated) {
        popup._updated = true; // Set flag to prevent looping.
        popup.update();
      }
    }, true);

    </script>
</body>
</html>
