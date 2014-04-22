function loadMap(center) {

    var map = new google.maps.Map(document.getElementById('map-canvas'), {
        zoom: 12,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var marker = new google.maps.Marker({
        position: center,
        map: map
    });

}

$(document).ready( function() {
    var center = new google.maps.LatLng($("#lat-hid").val(), $("#lng-hid").val());
    loadMap(center);
});

function updateReviews() {
    console.log("update reviews called");

    $.ajax ({
		datatype: "json",
	    url: "/get_review",
	    data: {'restaurant_id' : $("#restID-hid").val()},
	    success: function(review_list) {
	    	$("#review-list").empty();

            if ( review_list && review_list.length > 0 ) {
                for (var i=0; i<review_list.length; i++) {
                    drawLi(review_list[i]);
                }
            } else {
                var li = $("<li class=\"row list-space top-border\">")
                $("#review-list").append(li);
                li.append($("<h4>No reviews now! Please write reviews!</h4>"));
            }
        },
	    async: true,
	});
}

function drawLi(review) {
    var li = $("<li class=\"row list-space top-border\">")
    $("#review-list").append(li);
    li.append($("<h4>" + review.reviewer + "</h4>"));
    li.append($("rating " + review.rating));
    li.append($("<p>" + review.content + "</p>"));
}

window.setInterval(updateReviews, 5000);