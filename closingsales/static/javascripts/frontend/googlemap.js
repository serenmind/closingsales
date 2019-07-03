var map;
// these are the lat lang of berlin
var lat = '52.536717343134306';
var lng = '13.415940328124975';

function initMap() {
	
	var myLatLng = {lat:  parseFloat(lat), lng: parseFloat(lng)};
	var bounds = new google.maps.LatLngBounds();

	map = new google.maps.Map(document.getElementById('main-map'), {
		center: myLatLng,
		zoom: 8
	});

	$.ajax({
		url: "/api/latest_ads/",
		dataType: 'json',
		success: function(result){
    	    result.forEach(function(ad) {
    	    	var myLatLng = {lat:  parseFloat(ad.latitude), lng: parseFloat(ad.longitude)};
    	    	var marker = new google.maps.Marker({
			      position: myLatLng,
			      map: map,
			      title: ad.title
			    });

			    bounds.extend(marker.position);
			     var contentString = '<div id="content">'+
				            '<div id="siteNotice">'+
				            '</div>'+
				            '<h4 id="firstHeading" class="firstHeading">'+ ad.title +'</h4>'+
				            '<div id="bodyContent">'+
				            '<p>' + utils.extract(ad.description) + '</p>'+
				            '</div>'+
				            '<a href="/classifieds/' +ad.id + '/"> View Details </a>' + 
            				'</div>';
            	var infowindow = new google.maps.InfoWindow({
			          content: contentString
			        });
            	marker.addListener('click', function() {
          			infowindow.open(map, marker);
        		});
    	    });
    	    map.fitBounds(bounds);
			map.panToBounds(bounds);
	    },
	    error: function(err) {
			console.log('error', err)
		}
	});


}