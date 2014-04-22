$(document).ready(function() {
	getLocation();
});

function getLocation(){
    if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(sendAjax);
	} else {
		x.innerHTML="Geolocation is not supported by this browser.";
	}
};

function sendAjax(position) {

    var geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {

                $("#place-input").val(results[1].formatted_address);

                var parameters = {
                    "sort_by" : 'b',
                    "type" :'r',
                    "longitude" : position.coords.longitude,
                    "latitude" : position.coords.latitude,
                    "distance" : 10,
                    "address" : results[1].formatted_address
                };

                $.ajax ({
                    datatype: "json",
                    url: "/get-search",
                    data: parameters,
                    success: function(restaurant_list) {
                        $("#restaurant-list").empty();
                        if ( restaurant_list && restaurant_list.length > 0 ) {
                            for (var i=0; i<restaurant_list.length; i++) {
                                drawLi(restaurant_list[i]);
                            }
                        } else {
                            var li = $("<li class=\"row list-space top-border\">")
                            $("#restaurant-list").append(li);
                            li.append($("<h4>No results found!</h4>"));
                        }
                    },
                    async: true
                });
            }
        } else {
            alert("Geocoder failed due to: " + status);
        }
    });
}

function drawLi(restaurant) {
    var li = $("<li class=\"row list-space top-border\">")
    $("#restaurant-list").append(li);
    var div1 = $("<div class=\"col-md-3\" />");
    var div2 = $("<div class=\"col-md-5\" />");
    var div3 = $("<div class=\"col-md-3\" />");

    div1.append($("<h4>" + restaurant.fields.name + "</h4>"));
    div1.append($("<img src=\"\" width=\"160\" height=\"90\" alt=\"restaurant_picture\">"));

    div2.append($("<h4>Rating:" + restaurant.fields.avg_rating + " Reviews: " + restaurant.fields.review_number + "</h4>"));
    div2.append($("<h4>Introduction</h4>"));
    div2.append($("<p>" + restaurant.fields.introduction + "</p>"));

    div3.append($("<address><strong>" + restaurant.fields.address + "</strong></address>"));

    li.append(div1);
    li.append(div2);
    li.append(div3);
}