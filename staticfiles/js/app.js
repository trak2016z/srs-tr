bootbox.setLocale('pl');

$(document).ready(function() {

    $('.captcha_reload').click(function() {
        var target = $($(this).attr('data-target'));
        var src = $(this).attr('data-url');
        target.attr('src', src+'?r='+Math.random());
        return false;
    });

    $('a[data-toggle="confirm"]').click(function() {
        var href = $(this).attr('href');
        var title = $(this).attr('title') != undefined ? $(this).attr('title') : "Jesteś pewien?!";
        bootbox.confirm(title, function(result) {
            if (result) window.location.href = href;
        });
        return false;
    });

});