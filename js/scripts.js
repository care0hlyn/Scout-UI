
function drawDrones() {
    var i,
        fn,
        body = $('body'),
        angle = 0.0,
        drone;
    for (i = 0; i < 4; i++) {
        drone = $('#dummy-drone').clone();
        drone.attr('id', 'drone-' + (i + 1));
        body.append(drone);
        drone.show();
    }
    fn = function() {
        $('.drone').css({
            transform: 'scale(0.50) ' +
                'rotate(' + angle + 'deg)'
        });
        angle += 0.3;
        requestAnimationFrame(fn);
    };
    fn();
}

function animateGirl() {
    $('.girl-img').animate({
        "padding-left": 12
    }, {
        duration: 790,
        complete: function() {
            $('.girl-img').animate({
                "padding-left": 0
            }, {
                duration: 790,
                complete: animateGirl
            });
        }
    });
}

function animateDroneIcon() {
    $('.drone-top-img').animate({
        "padding-left": 25,
        "padding-top": 12
    }, {
        duration: 1000,
        complete: function() {
            $('.drone-top-img').animate({
                "padding-left": 0,
                "padding-top": 0
            }, {
                duration: 1000,
                complete: animateDroneIcon
            });
        }
    });
}

function animateLogo() {
    var i,
        fn,
        angle = 0.0;
    fn = function() {
        $('.loading').css({
            transform: 'translate(-50%, -50%) ' +
                'rotate(' + angle + 'deg)'
        });
        angle += 1.0;
        if (window.animating) {
            requestAnimationFrame(fn);
        }
    };
    window.animating = true;
    fn();
}

$(document).ready(function(){
    $(".loading").show();
    $(".talk-to-scout").hide();

    animateLogo();

    $(".loading").on( "click", function() {
        $(".onboarding-1").show();
        $(this).hide();
        window.animating = false;
    });

    $(".get-started-btn").on("click", function() {
        animateDroneIcon();
        animateGirl();
        $(".onboarding-2").show();
        $(".onboarding-1").hide();
    });

    $(".gmail-btn").on("click", function() {
        $(".onboarding-3").show();
        $(".onboarding-2").hide();
    });

    $(".fb-btn").on("click", function() {
        $(".onboarding-3").show();
        $(".onboarding-2").hide();
    });

    $(".pbar-2").on("click", function() {
        $(".onboarding-3").hide();
        $(".onboarding-4").show();
    });

    $(".pbar-3").on("click", function() {
        $(".onboarding-4").hide();
        $(".home").show();
        drawDrones();
    });

    $(".send-scout").on("click", function() {
        $('.confirmation').show();
    });

    $(".confirmation").on("click", function() {
        $(this).hide();
        $(".send-scout").hide();
        $(".talk-to-scout").show();
    });

});
