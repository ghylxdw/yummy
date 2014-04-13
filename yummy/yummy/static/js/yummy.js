function initializeMap() {
	var mapOptions = {
    center: new google.maps.LatLng(-33.8688, 151.2195),
    zoom: 13
  	};
  	
  	var map = new google.maps.Map(document.getElementById('map-canvas'),
    mapOptions);

	var input = document.getElementById('place-input');

	var autocomplete = new google.maps.places.Autocomplete(input);

	var infowindow = new google.maps.InfoWindow();
}

google.maps.event.addDomListener(window, 'load', initializeMap);