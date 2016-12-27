bootbox.setLocale('pl');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {

    $('.captcha_reload').click(function () {
        var target = $($(this).attr('data-target'));
        var src = $(this).attr('data-url');
        target.attr('src', src + '?r=' + Math.random());
        return false;
    });

    $('a[data-toggle="confirm"]').click(function () {
        var href = $(this).attr('href');
        var title = $(this).attr('title') != undefined ? $(this).attr('title') : "Jesteś pewien?!";
        bootbox.confirm(title, function (result) {
            if (result) window.location.href = href;
        });
        return false;
    });

    $('a[data-toggle="reject"]').click(function () {
        var href = $(this).attr('href');
        var title = $(this).attr('title') != undefined ? $(this).attr('title') : "Jesteś pewien?!";
        var dialog = bootbox.dialog({
            title: title,
            message: '<form id="reject-reason" action="' + href + '" method="post"><div class="row"><div class="col-sm-4">Możesz podać powód:</div><div class="col-sm-8"><input type="hidden" name="csrfmiddlewaretoken" value="'+getCookie('csrftoken')+'" /><input type="text" name="reason" class="form-control" maxlength="255" /></div></div></form>',
            buttons: {
                cancel: {
                    label: 'Anuluj',
                    callback: function () {
                    }
                },
                confirm: {
                    label: 'Potwierdź',
                    callback: function () {
                        $('form#reject-reason').submit();
                    }
                }
            }
        });
        dialog.init();
        return false;
    });

    /* $('.cal-show-day').click(function() {
        var ajaxHref =  $(this).attr('data-ajax-href');
        var title = $(this).attr('title');
        var dialog = bootbox.dialog({
            title: title,
            message: '<div><i class="fa fa-spin fa-spinner"></i> Trwa ładowanie...</div>',
            buttons: {
                cancel: {
                    label: 'zamknij okno'
                }
            }
        });
        dialog.init(function () {
            $.get(ajaxHref, function (msg) {
                dialog.find('.bootbox-body').html(msg);
            });
        });
        return false;
    }); */

});