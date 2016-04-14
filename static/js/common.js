$(function () {
    // For IE
    if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
        var msViewportStyle = document.createElement("style");
        msViewportStyle.appendChild(
            document.createTextNode(
                "@-ms-viewport{width:auto!important}"
        ));
        document.getElementsByTagName("head")[0].
            appendChild(msViewportStyle);
    }

    // For scrollUp
    $.scrollUp({
        animation: 'fade',
        scrollDistance: 100,
        scrollImg: true
    });
});

//for vuejs
Vue.config.delimiters = ['{[', ']}'];
Vue.config.unsafeDelimiters = ['{[[', ']]}'];
Vue.config.debug = true;
