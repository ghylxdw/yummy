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

//
//function updateReviews() {
//    console.log("update reviews called");
//
//    $.ajax ({
//		datatype: "json",
//	    url: "/restaurant/get-reviews",
//	    data: {'restaurant_id' : $("#restID-hid").val()},
//	    success: function(review_list) {
//	    	$("#review-table").empty();
//            if ( review_list && review_list.length > 0 ) {
//                for (var i=0; i<review_list.length; i++) {
//                    drawTr(review_list[i]);
//                }
//            } else {
//                var tr = $("<tr class=\"bot-border\">");
//                var td = $("<td style=\"color: red;\">");
//                $("#review-table").append(tr);
//                tr.append(td);
//                td.append($("<h4>No reviews now! Please write reviews!</h4>"));
//            }
//        },
//	    async: true,
//	});
//}
//
//function drawTr(review) {
//    var tr = $("<tr class=\"bot-border\">");
//
//    $("#review-table").append(tr);
//
//    var td1 = $("<td class=\"col-lg-3\">");
//    var td2 = $("<td class=\"col-lg-3\">");
//    var td3 = $("<td class=\"col-lg-3\">");
//
//    td1.append($("<h4>" + review.fields.name + "</h4>"));
//    td1.append($("<p>" + convertDateTime(review.fields.create_time).toString() + "</p>"));
//
//    td2.append($("<img src=\"/static/images/rating" + review.fields.rating + ".png\" height=\"42px\" width=\"200px\">"));
//
//    td3.append($("<h4>Comment</h4>"));
//    td3.append($("<p><strong>" + review.fields.content + "</strong></p>"));
//
//    tr.append(td1);
//    tr.append(td2);
//    tr.append(td3);
//}
//
//function convertDateTime(dateTime){
//    var arr = dateTime.split("T");
//    var date = arr[0];
//    var yyyy = date[0];
//    var mm = date[1]-1;
//    var dd = date[2];
//
//    var time = dateTime[1].split(":");
//    var h = time[0];
//    var m = time[1];
//    var s = parseInt(time[2]); //get rid of that 00.0;
//
//    return new Date(yyyy,mm,dd,h,m,s);
//}
//
//window.setInterval(updateReviews, 5000);