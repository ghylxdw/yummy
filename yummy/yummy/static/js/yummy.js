function autocomplete() {
	var input = $('#place-input').get(0);
	var autocomplete = new google.maps.places.Autocomplete(input);
}

function getURL(theUrl, extraParameters) {
    var extraParametersEncoded = $.param(extraParameters);
    var seperator = theUrl.indexOf('?') == -1 ? "?" : "&";

    return(theUrl + seperator + extraParametersEncoded);
}

function onSearch() {
	var q = $('#find-input').val();
	var type = $('input:radio[name=type]:checked').val();
	var address = $('#place-input').val();
	var defaultSort = 'b';
	var defaultDist = 2;

	if (address.length == 0) {
		alert('Warning: Please input the geo address');
		return true;
	}

  	$.ajax({
	    datatype: "json",
	    url: "https://maps.googleapis.com/maps/api/geocode/json",
	    data: {address: address, sensor: true},
	    success: function(geocode) {
	    	if ( geocode ) {
				var lat = geocode.results[0].geometry.location.lat;
		        var lng = geocode.results[0].geometry.location.lng;

		        var parameters = {
		        	"q" : q,
		        	"sort_by" : defaultSort,
		        	"type" : type,
		        	"longitude" : lng,
		        	"latitude" : lat,
		        	"distance" : defaultDist,
                    "address" : address
		        };

		        window.location.replace(getURL('search', parameters));
	    	} else {
	    		alert('Fail to get geocode from google');
	    	}
	    },
	    async: false,
    });

    return false;
}

google.maps.event.addDomListener(window, 'load', autocomplete);