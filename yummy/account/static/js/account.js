$(document).ready(function() {
    $('#id_address').bind('input', getLatLng());
	getLocation();
});

function getLocation(){
    if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(loadMap);
	} else {
		x.innerHTML="Geolocation is not supported by this browser.";
	}
};

function loadMap(center) {

    var center = new google.maps.LatLng(center.coords.latitude, center.coords.longitude);

    var mapOptions = {
          center: center,
          zoom: 15
        };

    var map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);

    var marker = new new google.maps.Marker({
        position: center,
        map: map
    });
}

function getLatLng() {

	var address = $('#id_address').val();

	if (address.length == 0) {
		alert('Warning: Please input the geo address');
		return false;
	}

  	$.ajax({
	    datatype: "json",
	    url: "https://maps.googleapis.com/maps/api/geocode/json",
	    data: {address: address, sensor: true},
	    success: function(geocode) {
	    	if ( geocode ) {
				var lat = geocode.results[0].geometry.location.lat;
		        var lng = geocode.results[0].geometry.location.lng;

                $('#id_longitude').val(lng);
                $('#id_latitude').val(lat);

                var center = new google.maps.LatLng(center.coords.latitude, center.coords.longitude);
                loadMap(center);

                return true;
	    	} else {
	    		alert('Fail to get geocode from google');
	    	}
	    },
	    async: false,
    });

    return false;
}

function autocomplete() {
    var input = $('#id_address').get(0);
    var autocomplete = new google.maps.places.Autocomplete(input);
}

google.maps.event.addDomListener(window, 'load', autocomplete);
