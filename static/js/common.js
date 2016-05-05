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

    // jqbootstrapvalidation
    $(function () {$("input,select,textarea").not("[type=submit]").jqBootstrapValidation(); } );

    // for pnotify
    $(document).ready(function(){
        function show_stack_topright(type) {
            var opts = {
                title: "",
                text: "",
                animation: "show",
                styling: 'bootstrap3',
                hide: true,
                delay: 5000,
            };
            switch (type) {
                case 'error':
                    opts.title = "";
                opts.text = "操作失败！";
                opts.type = "error";
                break;
                case 'success':
                    opts.title = "";
                opts.text = "操作成功！";
                opts.type = "success";
                break;
            }
            new PNotify(opts);
        }

        var success = $(".flash-success");
        if (success.length > 0) {
            show_stack_topright('success');
        }

        var failed = $(".flash-failed");
        if (failed.length > 0) {
            show_stack_topright('error');
        }
    });
});

//for vuejs
Vue.config.delimiters = ['{[', ']}'];
Vue.config.unsafeDelimiters = ['{[[', ']]}'];
Vue.config.debug = true;

new Vue({
    el: ".scui-nav",
    methods: {
        show_information: function(msg, event) {
            swal({
                title: "Smart Checker UI",
                text: "网元日志收集工具<br />版权所有：诺基亚",
                html: true,
                imageUrl: "/img/logo.png",
                imageSize: "300x50",
                confirmButtonColor: '#DD6B55',
                confirmButtonText: '关闭',
                closeOnConfirm: true
            });
        }
    }
})


