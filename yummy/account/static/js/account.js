$(document).ready(function() {
    var lat = $("#id_latitude").val();
    var lng = $("#id_longitude").val();

    if (lat) {
        var center = new google.maps.LatLng(lat, lng);
        loadMap(center);
    } else {
        getLocation();
    }

});

function getLocation(){
    if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
            var center = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            loadMap(center);
        });
	} else {
		x.innerHTML="Geolocation is not supported by this browser.";
	}
};

function loadMap(center) {

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

                var center = new google.maps.LatLng(lat, lng);
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

function postRecipe() {
    var fd = new FormData(document.getElementById("recipe_upload"));

    $.ajax({
        url: "/account/upload-recipe",
        type: "POST",
        data: fd,
        processData: false,  // tell jQuery not to process the data
        contentType: false,   // tell jQuery not to set contentType
        success: function( response ) {

            var ids = $('#id_added_recipes').val();
            if (ids.length == 0) {
                $("#id_added_recipes").val(response.id);
            } else {
                $("#id_added_recipes").val(ids + "_" + response.id);
            }

            var tr = $("<tr id=\"recipe" + response.id + "\">");
            $("#recipe-table").append(tr);

            var td = $("<td>");
            tr.append(td);

            td.append($("<h4>" + response.name +"</h4>"));
            td.append($("<img src=\"/restaurant/recipe-image/" + response.id + "\" width=\"200px\">"));
            td.append($("<a onclick=\"deleteRecipe(" + response.id + ")\">delete</a>"));

            $("#recipe-name").val("");
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Invalid picture format or invalid recipe name!!!");
        }
    });

    return false;
}

function deleteRecipe(id) {

    $("#recipe" + id).remove();
    var csrftoken = $.cookie('csrftoken');

    $.ajax ({
        url: "/account/delete-recipe",
        type: "POST",
        data: {'id' : id, 'csrfmiddlewaretoken' : csrftoken}
    });
}

function onCancel() {
    var csrftoken = $.cookie('csrftoken');

    $.ajax ({
        url: "/account/cancel-add-edit-restaurant",
        type: "POST",
        data: {'delete_recipes' :  $("#id_added_recipes").val(), 'csrfmiddlewaretoken' : csrftoken}
    });
}

function autocomplete() {
    var input = $('#id_address').get(0);
    var autocomplete = new google.maps.places.Autocomplete(input);
}

google.maps.event.addDomListener(window, 'load', autocomplete);
