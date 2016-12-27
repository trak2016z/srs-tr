$(document).ready(function () {

    var options = {
        url: function (phrase) {
            return $('#autocomplete_room').attr('data-ajax-url') + '?phrase=' + phrase;
        },
        listLocation: "rooms",
        matchResponseProperty: "phrase",
        getValue: function (element) {
            return element.name + ' - ' + element.city;
        },
        template: {
            type: "custom",
            method: function (value, item) {
                var v = '<a href="' + item.link + '">' + value;
                if (item.seats > 0) v += ' (' + item.seats + ' miejsc)';
                v += '</a>';
                return v;
            }
        }
    };
    $('#autocomplete_room').easyAutocomplete(options);

    $('.calendarium a.cal-day').click(function () {
        var title = $(this).attr('data-title');
        var ajaxHref = $(this).attr('data-ajax-href');
        var dialog = bootbox.dialog({
            size: "large",
            title: "Kalendarz - " + title,
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
    });


});