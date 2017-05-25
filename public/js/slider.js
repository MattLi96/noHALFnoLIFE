$("#timeSlider").slider();
$("#timeSlider").on("slideStop", function(slideEvt) {
    let num = slideEvt.value
    window.info.updateTime(window.info.$data.timeOptions[num])
    $("#timeSliderValLabel").text(formatDate(window.info.$data.timeOptions[num]))
});