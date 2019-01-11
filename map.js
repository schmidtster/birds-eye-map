// initialize the map by assigning it a variable, map.
var map = L.map('bev_map', {zoomControl: false, scrollWheelZoom: false, fullscreenControl: true, fullscreenControlOptions: {
position: 'topleft'}}).setView([38.00000, -97.00000], 4);

var zoomHome = L.Control.zoomHome();
zoomHome.addTo(map);

// scrollWheelZoom defaults to true, but when false, prevents a user from using the scroll wheel to zoom in. .setView centers the map on a certain point. I have it here centered in Kansas. The 4 is the initial zoom value when loading the page. Increase it and the map will load closer to earth.

// define a tile layer for the map, basically what sort of skin you want the map to have. Also set the min and max zoom feature here.
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', {attribution: 'Tiles &copy; Esri', maxZoom: 13, minZoom: 4}).addTo(map);

var customOptions = {
  'minWidth': '250',
  'className': 'custom'
}

// This part adds the points to the map and adds them as a marker cluster group.
var clusters = L.markerClusterGroup({maxClusterRadius:70}).addTo(map);
$.getJSON("map-v2.geojson",function(data){
  var bev = L.geoJson(data,{
    pointToLayer: function(feature,latlng){
      var marker = L.marker(latlng, { tags: feature.properties.Genres.concat(feature.properties.Creator, feature.properties.Date_Range)});
      marker.bindPopup('<p align=center>' + '<strong>Title: </strong>' + feature.properties.Title + '<br/><a href="' + feature.properties.Image_Bank_URL + '" target="_blank"><img src="' + feature.properties.Thumbnail_URL + '"/></a><br/>' + '<strong>Date: </strong>' + feature.properties.Date + '<br/>' + '<strong>Creator: </strong>' + feature.properties.Creator, customOptions);
      return marker;
    }
  });
  bev.addTo(clusters);
});

// Here is the code block for the Tag Filter Button. I start by accessing a tags file that has the data that I use for filter options.
$.getJSON('tags.json', function(data) {
var genres = L.control.tagFilterButton({
  data: data.genres,
  filterOnEveryClick: true,
  icon: '<i class="fas fa-tags"></i>',
}).addTo(map);
genres.enableMCG(clusters);
var creators = L.control.tagFilterButton({
  data: data.creators,
  filterOnEveryClick: true,
  icon: '<i class="fas fa-user-edit"></i>',
}).addTo(map);
creators.enableMCG(clusters);
var date_ranges = L.control.tagFilterButton({
  data: data.date_ranges,
  filterOnEveryClick: true,
  icon: '<i class="fas fa-clock"></i>'
}).addTo(map);
date_ranges.enableMCG(clusters);
jQuery('.easy-button-button').click(function() {
    target = jQuery('.easy-button-button').not(this);
    target.parent().find('.tag-filter-tags-container').css({
        'display' : 'none',
    });
});
});

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