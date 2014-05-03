$(document).ready(function() {
	$.post("/getPosts", { LIM: 0}, function(response){
		$.each(response,function(i,item){
			postCount += 1;
			$('#POST').append("<div class=\"post\"><a href=\"" + item.url + "\" class=\"title\">" + item.title + "</a><span class=\"date\">Published on: " + item.date + "</span></br>" + "<div class=\"content\">" + item.content + "</div></div>");
		});
	});
});