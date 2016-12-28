$(document).ready(function () {
    $('#frr').submit(function () {
        var form = $(this);
        var message = $(form).find('.message');
        var rest = $(form).find('.rest');
        var ajaxHref = $(form).attr('data-ajax-href');
        var my_listHref = $(form).attr('data-my-list-href');
        message.html('<div class="text-xs-center alert alert-info"><i class="fa fa-spin fa-spinner"></i> Trwa ładowanie...</div>');
        $.post(ajaxHref, {
            from_hour: $('[name="from_hour"]', form).val(),
            from_minute: $('[name="from_minute"]', form).val(),
            to_hour: $('[name="to_hour"]', form).val(),
            to_minute: $('[name="to_minute"]', form).val(),
            event_name: $('[name="event_name"]', form).val(),
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]', form).val()
        }).done(function (data) {
            if (data.status == -1) {
                message.fadeOut().html('');
                var error_str = '';
                for (var e in data.errors) {
                    if (e > 0) error_str += '<br />';
                    error_str += data.errors[e];
                }
                message.html('<div class="alert alert-danger">' + error_str + '</div>').fadeIn();
            } else if (data.status == 0) {
                message.fadeOut().html('<div class="alert alert-success">Rezerwacja została przyjęta. Oczekuje ona obecnie na zatwierdzenie przez opiekuna sali.</div>' +
                    '<div class="alert alert-info">Status swoich rezerwacji możesz sprawdzić w zakładce:<br /><a href="' + my_listHref + '" class="btn btn-primary btn-sm mt-1"><i class="fa fa-list"></i> moje rezerwacje</a>').fadeIn();
                rest.hide();
            } else if (data.status == 1) {
                $('body').attr('reload', '1');
                message.fadeOut().html('<div class="alert alert-success">Rezerwacja została przyjęta oraz automatycznie zaakceptowana.</div>' +
                    '<div class="alert alert-info">Status swoich rezerwacji możesz sprawdzić w zakładce:<br /><a href="' + my_listHref + '" class="btn btn-primary btn-sm mt-1"><i class="fa fa-list"></i> moje rezerwacje</a>').fadeIn();
                rest.hide();
            }
        });
        return false;
    });
});