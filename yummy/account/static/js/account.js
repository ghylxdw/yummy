$(function() {
    $("div.star-rating > s").on("click", function(e) {
        var numStars = $(e.target).parentsUntil("div").length+1;
        alert(numStars + (numStars == 1 ? " star" : " stars!"));
    });
});

$(document).ready(function() {
	var stars = $("div.star-rating");
    stars.empty();
    stars.append($("<s></s>"));
});