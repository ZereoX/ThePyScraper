/* FUNCTION DEFINITIONS */
function getDocHeight() { var D = document; return Math.max( D.body.scrollHeight, D.documentElement.scrollHeight, D.body.offsetHeight, D.documentElement.offsetHeight, D.body.clientHeight, D.documentElement.clientHeight ); }

/* GLOBAL VARIABLES */
var postCount = 0;
var timer;
var isHaveContent = 0

$(window).scroll(function(){
	if ( timer ) clearTimeout(timer);

	timer = setTimeout(function(){
		if($(window).scrollTop() + $(window).height() >= getDocHeight() * 0.90 && isHaveContent != 1) {
			$.post("/getPosts", { LIM: postCount }, function(response){
				if ($.isEmptyObject(JSON.parse(response))) {
					$('#POST').append("<div class=\"post\"><div class=\"ENDBLOCK\">No more posts. You might have read them all.</div></div>")
					isHaveContent = 1;
				}
				else {
					$.each(JSON.parse(response),function(i,item){
						postCount += 1;
						$('#POST').append("<div class=\"post\"><a href=\"" + item.url + "\" class=\"title\">" + item.title + "</a><span class=\"date\">Published on: " + item.date + "</span></br><div class=\"content\">" + item.content + "</div></div>");
					});
				}
			});
		}
	}, 500);
});