$(document).ready(function () {

    $('.cal-accept').click(function() {
        var href = $(this).attr('href');
        var title = $(this).attr('title');
        bootbox.confirm(title, function (result) {
            if (result) {
                $.get(href, function(data) {
                    if (data.executed) window.location.reload();
                });
            }
        });
        return false;
    });

    $('.cal-reject').click(function () {
        var href = $(this).attr('href');
        var title = $(this).attr('title') != undefined ? $(this).attr('title') : "Jesteś pewien?!";
        var dialog = bootbox.dialog({
            title: title,
            message: '<div class="row"><div class="col-sm-4">Możesz podać powód:</div><div class="col-sm-8"><input type="text" id="cal-reject-reason" name="reason" class="form-control" maxlength="255" /></div></div>',
            buttons: {
                cancel: {
                    label: 'Anuluj',
                    callback: function () { }
                },
                confirm: {
                    label: 'Potwierdź',
                    callback: function () {
                        $.post(href, {
                            reason: $('#cal-reject-reason').val(),
                            csrfmiddlewaretoken: getCookie('csrftoken')
                        }).done(function(data) {
                            if (data.executed) window.location.reload();
                        });
                    }
                }
            }
        });
        dialog.init();
        return false;
    });

});