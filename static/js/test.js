new Vue({
    el: ".scui_test",
    data: {
        result_panel: false,
        result_data: "",
        formdata: {conntype: "SSH"},
        loading: false,
    },
    methods: {
        submit_form: function(msg, event) {
            var self = this;
            this.result_panel = false;
            this.loading = true;
            $.post('/test/',
                JSON.stringify(self.$data.formdata),
                function (msg) {
                    self.$data.result_data = msg.response;
                    self.$data.result_panel = true;
                    self.$data.loading = false;
                }
            );
        },
    }
})
