var map;
var latitude = document.getElementById('id_latitude');
var longitude = document.getElementById('id_longitude');
var title = document.getElementById('id_title');

function initMap() {
  var lat = latitude.value
  var lng = longitude.value
  var myLatLng, ad_new;

  if (!lat) {
    lat = '52.536717343134306';
    lng = '13.415940328124975';
    ad_new = true;
  }
  var myLatLng = {lat:  parseFloat(lat), lng: parseFloat(lng)};
  map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 8
  });
  var marker;
  if (!ad_new) {
    marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      draggable: true,
      title: title.value
    });
  }


  google.maps.event.addListener(map, 'click', function(evt) {
    var latLang = new google.maps.LatLng(evt.latLng.lat(), evt.latLng.lng());
    if (marker) return false;
    marker = new google.maps.Marker({
      position: latLang,
      map: map,
      draggable: true,
      title: title.value
    });
    latitude.value = marker.getPosition().lat();
    longitude.value = marker.getPosition().lng();
    google.maps.event.addListener(marker, 'dragend', function(evt) {
      latitude.value = marker.getPosition().lat();
      longitude.value = marker.getPosition().lng();
    });
  });
}