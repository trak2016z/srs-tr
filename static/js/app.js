$(document).ready(function() {

    $('.captcha_reload').click(function() {
        var target = $($(this).attr('data-target'));
        var src = $(this).attr('data-url');
        target.attr('src', src+'?r='+Math.random());
        return false;
    });

});