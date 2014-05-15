$(document).ready(function() {
	$.post("/getPosts", { LIM: 0}, function(response){
		if ($.isEmptyObject(JSON.parse(response))) {
			$('#POST').append("<div class=\"post\"><div class=\"ENDBLOCK\">No more posts. You might have read them all.</div></div>")
		}
		else {
			$.each(JSON.parse(response),function(i,item){
				postCount += 1;
				if ( postCount == 1){
					$('#POST').append("<div class=\"post current\"><a href=\"" + item.url + "\" class=\"title\">" + item.title + "</a><span class=\"date\">Published on: " + item.date + "</span></br><div class=\"content\">" + item.content + "</div></div>");
				} else {
					$('#POST').append("<div class=\"post\"><a href=\"" + item.url + "\" class=\"title\">" + item.title + "</a><span class=\"date\">Published on: " + item.date + "</span></br><div class=\"content\">" + item.content + "</div></div>");
				}
			});
		}
	});
});