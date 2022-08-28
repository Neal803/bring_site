
$(function ($) {
    $('#form_ajax_login').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                window.location.reload()
            },
            error: function (response) {
                if (response.status === 400) {
                    $('.alert-danger').text(response.responseJSON.error).removeClass("d-none")
                }
            }
        })
    })
})

$(function ($) {
    $('#form_ajax_registration').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                window.location.reload()
            },
            error: function (response) {
                if (response.status === 400) {
                    $('.alert-danger').text(response.responseJSON.error).removeClass("d-none")
                }
            }
        })
    })
})

$(function ($) {
    var arr = $("form[id*='favorite']")
    jQuery.each(arr, function() {
        $(this).click(function(e){
                e.preventDefault()
                $.ajax({
                    type: this.method,
                    url: this.action,
                    data: $(this).serialize(),
                    dataType: "json",
                    success : function(response){
                        window.location.reload()
                    },
                    error: function(rs, e) {
                    }
                });
        })
    })
})