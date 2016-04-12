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

});

//common angularjs start
var app = angular.module('scui', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);
