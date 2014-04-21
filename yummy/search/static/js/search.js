function loadMap(center, restaurants, zoom) {

    var map = new google.maps.Map(document.getElementById('map-canvas'), {
      zoom: zoom,
      center: center,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    for (i = 0; i < restaurants.length; i++) {
        var location = restaurants[i].fields.location.split(" ");
        var lat = parseFloat(location[2]);
        var lng = parseFloat(location[1].substr(1));

        marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0]);
          infowindow.open(map, marker);
        }
        })(marker, i));
    }

}

function sendAjax() {

    var parameters = {
        "q" : $('#q-hid').val(),
        "sort_by" : $('input:radio[name=sortOpt]:checked').val(),
        "type" : $('#type-hid').val(),
        "longitude" : $('#lng-hid').val(),
        "latitude" : $('#lat-hid').val(),
        "distance" : $('input:radio[name=distOpt]:checked').val(),
        "address" : $('#address-hid').val()
    };

    var center = new google.maps.LatLng(parameters.latitude, parameters.longitude);
    var zoom = 16 - Math.floor(parameters.distance/5);

	$.ajax ({
		datatype: "json",
	    url: "/get-search",
	    data: parameters,
	    success: function(restaurant_list) {
            loadMap(center, restaurant_list, zoom);
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
	    async: true,
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

    div3.append($("<address>" + restaurant.fields.location + "</address>"));

    li.append(div1);
    li.append(div2);
    li.append(div3);
}

$(document).ready( function() {
    sendAjax();
});


$(function()
{
    $('#sortOpt1').click( function( event )
    {
        sendAjax();
    })

    $('#sortOpt2').click( function( event )
    {
        sendAjax();
    })

    $('#sortOpt3').click( function( event )
    {
        sendAjax();
    })

    $('#distOpt1').click( function( event )
    {
        sendAjax();
    })

    $('#distOpt2').click( function( event )
    {
        sendAjax();
    })

    $('#distOpt3').click( function( event )
    {
        sendAjax();
    })
});