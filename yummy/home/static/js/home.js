$(document).ready(function() {
	getLocation();
});

function getLocation(){
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition();
	} else {
		x.innerHTML="Geolocation is not supported by this browser.";
	}
};

function searchQuery(position) {

	var parameters = {
    	"sort_by" : 'b',
    	"type" : 'r',
    	"longitude" : position.coords.longitude,
    	"latitude" : position..coords.latitude,
    	"distance" : 2,
        "address" : 'At Current Location'
    };

    window.location.href = getURL('/search', parameters);
}