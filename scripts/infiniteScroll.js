/* FUNCTION DEFINITIONS */
function getDocHeight() { var D = document; return Math.max( D.body.scrollHeight, D.documentElement.scrollHeight, D.body.offsetHeight, D.documentElement.offsetHeight, D.body.clientHeight, D.documentElement.clientHeight ); }

/* GLOBAL VARIABLES */
var postCount = 0;

$(window).scroll(function() {if($(window).scrollTop() + $(window).height() >= getDocHeight() * 0.90) {
	$.post("/getPosts", { LIM: postCount }, function(response){
		$.each(response,function(i,item){
			postCount += 1;
			$('#POST').append("<div class=\"post\"><a href=\"" + item.url + "\" class=\"title\">" + item.title + "</a><span class=\"date\">Published on: " + item.date + "</span></br>" + "<div class=\"content\">" + item.content + "</div></div>");
		});
	});
}});