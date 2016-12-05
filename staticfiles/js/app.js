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

    var options = {
	    url: function(phrase) {
		    return $('#autocomplete_room').attr('data-ajax-url')+'?phrase='+phrase;
	    },
	    listLocation: "rooms",
        matchResponseProperty: "phrase",
        getValue: function(element) {
		    return element.name+' - '+element.city;
	    },
        template: {
            type: "custom",
            method: function(value, item) {
			    var v = '<a href="'+item.link+'">'+value;
                if (item.seats > 0) v += ' ('+item.seats+' miejsc)';
                v += '</a>';
                return v;
		    }
        }
    };
    $('#autocomplete_room').easyAutocomplete(options);

    $('.calendar a.cal-day').click(function() {
        var title = $(this).attr('data-title');
        var ajaxHref = $(this).attr('data-ajax-href');
        var dialog = bootbox.dialog({
            title: "Kalendarz - "+title,
            message: '<div><i class="fa fa-spin fa-spinner"></i> Trwa ładowanie...</div>',
            onEscape: function () {
                // window.location.reload();
            },
            buttons: {
                cancel: {
                    label: 'zamknij okno',
                    callback: function() {
                        // window.location.reload();
                    }
                }
            }
        });
        dialog.init(function(){
            $.get(ajaxHref, function(msg) {
                dialog.find('.bootbox-body').html(msg);
            });
        });
        return false;
    });

});