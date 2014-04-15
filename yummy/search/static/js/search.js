function loadMap(center, locations) {

    var map = new google.maps.Map(document.getElementById('map-canvas'), {
      zoom: 10,
      center: center,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    for (i = 0; i < locations.length; i++) {  
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
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
    };

    console.log(parameters.sort_by + parameters.distance);

// var data = [
//     {'name':{'first':'Leonard','last':'Marx'},'nickname':'Chico','born':'March 21, 1887','actor': true,'solo_endeavours':[{'title':'Papa Romani'}]},
//     {'name':{'first':'Adolph','last':'Marx'},'nickname':'Harpo','born':'November 23, 1888','actor':true,'solo_endeavours':[{'title':'Too Many Kisses','rating':'favourite'},{'title':'Stage Door Canteen'}]},
//     {'name':{'first':'Julius Henry','last':'Marx'},'nickname':'Groucho','born': 'October 2, 1890','actor':true,'solo_endeavours':[{'title':'Copacabana'},{'title':'Mr. Music','rating':'favourite'},{'title':'Double Dynamite'}]},
//     {'name':{'first':'Milton','last':'Marx'},'nickname':'Gummo','born':'October 23, 1892'},
//     {'name':{'first':'Herbert','last':'Marx'},'nickname':'Zeppo','born':'February 25, 1901','actor':true,'solo_endeavours':[{'title':'A Kiss in the Dark'}]}
// ];

//     Tempo.prepare('rest-list').render(data);
    
    var center = new google.maps.LatLng(-33.92, 151.25);

    var locations = [
      ['Bondi Beach', -33.890542, 151.274856, 4],
      ['Coogee Beach', -33.923036, 151.259052, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]
    ];
    
    loadMap(center, locations);

	$.ajax ({
		datatype: "json",
	    url: "/get-search",
	    data: parameters,
	    success: function(restaurant_list) {
            if ( restaurant_list && restaurant_list.length > 0 ) {
                Tempo.prepare('rest-list').render(restaurant_list);
                // loadMap(center, restaurant_list);
            } else {
                alert('No restaurant found!');
            }
	    },
	    async: true,
	});
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