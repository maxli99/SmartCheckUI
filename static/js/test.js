new Vue({
    el: ".scui-test",
    data: {
        result_panel: false,
        result_data: "",
        formdata: {conntype: "SSH"},
        loading: false,
    },
    methods: {
        submit_form: function(msg, event) {
            if ($("input,select,textarea").not("[type=submit]").jqBootstrapValidation("hasErrors")) {
                return;
            }
            var self = this.$data;
            this.result_panel = false;
            this.loading = true;
            $.post(SCRIPT_ROOT,
                JSON.stringify(self.formdata),
                function (msg) {
                    self.result_data = msg.response;
                    self.result_panel = true;
                    self.loading = false;
                }
            );
        },
    }
});
