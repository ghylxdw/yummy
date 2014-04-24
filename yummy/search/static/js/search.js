function loadMap(center, restaurants, zoom) {

    var map = new google.maps.Map(document.getElementById("map-canvas"), {
        zoom: zoom,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    marker = new google.maps.Marker({
        position: center,
        map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent("You are current here!");
          infowindow.open(map, marker);
        }
    })(marker, i));

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
          infowindow.setContent(restaurants[i].fields.name);
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
    var zoom;

    switch(parameters.distance) {
        case "2":
            zoom = 12;
            break;
        case "5":
            zoom = 11;
            break;
        case "10":
            zoom = 10;
            break;
    }

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
    var div2 = $("<div class=\"col-md-4\" />");
    var div3 = $("<div class=\"col-md-5\" />");

    div1.append($("<h3><a href=\"/restaurant/" + restaurant.pk + "\">" + restaurant.fields.name +"</a></h3>"));
    div1.append($("<address><strong>" + restaurant.fields.address + "</strong></address>"));
    div1.append($("<p>" + Math.round(restaurant.fields.distance*10)/10 +" miles away</p>"));

    var divRating = $("<div style=\"width:auto; padding-top: 50px;\" />");
    divRating.append($("<img style=\"float:left;\" src=\"/static/images/rating" + Math.ceil(restaurant.fields.avg_rating) + ".png\" width=\"200px\">"));
    divRating.append($("<h4 style=\"float:right;\">" + restaurant.fields.review_number + " Reviews </h4>"));

    div2.append(divRating);
    if (restaurant.fields.recipe_id) {
        div2.append($("<p>This restaurant has " + restaurant_list.fields.recipe_name + "</p>"));
    }

    div3.append($("<h4>Introduction</h4>"));
    div3.append($("<p>" + restaurant.fields.introduction + "</p>"));

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