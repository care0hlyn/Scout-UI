$(document).ready(function(){
	$(".onboarding-1").hide();
    $(".onboarding-2").hide();
    $(".onboarding-3").hide();
    $(".onboarding-4").hide();
    $(".confirmation").hide();
    $(".home").hide();
    $(".loading").show();

    $(".loading").on( "click", function() {
        $(".onboarding-1").show();
        $(this).hide();
    });

    $(".get-started-btn").on("click", function() {
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
    });

    $(".send-scout").on("click", function() {
        $(".confirmation").show();
    });

});
