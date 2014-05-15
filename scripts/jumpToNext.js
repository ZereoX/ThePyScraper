$('div.post').first();

$(document).keydown(function(evt) {
    if ( evt.keyCode == 190 || evt.keyCode == 188) {
	    evt.preventDefault();
	    var t = $(this).text(),
		that = $(this);
	}

    if ( evt.keyCode == 190 ) {
		if ($('.current').next('div.post').length > 0) {
			var $next = $('.current').next('.post');
			var top = $next.offset().top;

			$('.current').removeClass('current');     

			$(function () {
				$next.addClass('current');
				$('html, body').animate({scrollTop: $('.current').offset().top }, 'fast');
			});
		}
	}
	else if ( evt.keyCode == 188 ) {
		if ($('.current').prev('div.post').length > 0) {
			var $prev = $('.current').prev('.post');
			var top = $prev.offset().top;

			$('.current').removeClass('current');

			$(function () {
				$prev.addClass('current');
				$('html, body').animate({scrollTop: $('.current').offset().top }, 'fast');
			});
		} 
	}
});