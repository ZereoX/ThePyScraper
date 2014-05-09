$(document).bind('keydown', function (evt){
    if ( evt.keycode = 190 ) {
        post = $(this).parent();

        // if I am the last .post in my group...
        while (    document != post[0] // not reached root
        && post.find('~.post, ~:has(.post)').length == 0)
        post = post.parent(); // search siblings of parent instead

        nextdiv = post.nextAll('.post, :has(.post)').first();

        // no next .post found, go back to first post
        if (nextdiv.length==0) nextdiv = $(document).find('.post:first');

        $(document).scrollTop(nextdiv.offset().top);
        // $(this).parent().next() // this is the next div post.
        return false;
    }
});
