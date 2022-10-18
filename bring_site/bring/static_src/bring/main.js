var slideNow = 1;
var slideCount = $('#slidewrapper').children().length / 2;
var slideInterval = 6000;
var navBtnId = 0;
var translateWidth = 0;

$(document).ready(function() {
    var switchInterval = setInterval(nextSlide, slideInterval);

    $('#viewport').hover(function() {
        clearInterval(switchInterval);
    }, function() {
        switchInterval = setInterval(nextSlide, slideInterval);
    });

    $('#next-btn').click(function() {
        nextSlide();
    });

    $('#prev-btn').click(function() {
        prevSlide();
    });

    $('.slide-nav-btn').click(function() {
        navBtnId = $(this).index();

        if (navBtnId + 1 != slideNow) {
            translateWidth = -$('#viewport').width() * (navBtnId);
            $('#slidewrapper').css({
                'transform': 'translate(' + translateWidth + 'px, 0)',
                '-webkit-transform': 'translate(' + translateWidth + 'px, 0)',
                '-ms-transform': 'translate(' + translateWidth + 'px, 0)',
            });
            slideNow = navBtnId + 1;
        }
    });
});


function nextSlide() {
    if (slideNow == slideCount || slideNow <= 0 || slideNow > slideCount) {
        $('#slidewrapper').css('transform', 'translate(0, 0)');
        slideNow = 1;
    } else {
        translateWidth = -$('#viewport').width() * (slideNow);
        $('#slidewrapper').css({
            'transform': 'translate(' + translateWidth + 'px, 0)',
            '-webkit-transform': 'translate(' + translateWidth + 'px, 0)',
            '-ms-transform': 'translate(' + translateWidth + 'px, 0)',
        });
        slideNow++;
    }
}

function prevSlide() {
    if (slideNow == 1 || slideNow <= 0 || slideNow > slideCount) {
        translateWidth = -$('#viewport').width() * (slideCount - 1);
        $('#slidewrapper').css({
            'transform': 'translate(' + translateWidth + 'px, 0)',
            '-webkit-transform': 'translate(' + translateWidth + 'px, 0)',
            '-ms-transform': 'translate(' + translateWidth + 'px, 0)',
        });
        slideNow = slideCount;
    } else {
        translateWidth = -$('#viewport').width() * (slideNow - 2);
        $('#slidewrapper').css({
            'transform': 'translate(' + translateWidth + 'px, 0)',
            '-webkit-transform': 'translate(' + translateWidth + 'px, 0)',
            '-ms-transform': 'translate(' + translateWidth + 'px, 0)',
        });
        slideNow--;
    }
}

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
                    $('.alert-danger-reg').text(response.responseJSON.error).removeClass("d-none")
                    console.log(response)
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

$(function ($) {
    $('.btn-google').click(function (e) {
        var left = (screen.width/2)-(700/2);
        var top = (screen.height/2)-(700/2);
        newWin = window.open('http://192.168.0.111:8000/login/google-oauth2/', 'social', 'menubar=no, width=700, height=700, left='+left+', top='+top+'');
        window.onmousemove = function(){
            window.location.reload();
        };
        console.log(document.getElementById('menu__btn__area'))
        var elem = document.getElementById('menu__btn__area')
//        var newWin = window.open('http://localhost:8000/login/google-oauth2/', 'social', 'menubar=no, width=600, height=600');
//        console.log('click')  onmousemove
//        console.log(window.location.href)
//        console.log(newWin.location.href)
//        console.log(newWin)
//        setTimeout(() => {console.log(newWin.location.href);}, 6000);

//        var check = function(){
//            if(condition){
//                // run when condition is met
//            }
//            else {
//                setTimeout(check, 1000); // check again in a second
//            }
//        }
//        check();
    })
})