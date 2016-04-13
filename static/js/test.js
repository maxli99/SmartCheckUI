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
            this.result_panel = false;
            this.loading = true;
            this.$http({
                data: this.formdata,
                method: 'POST',
            }).then(function (response) {
                // success callback
                this.result_data = response.data;
                this.result_panel = true;
                this.loading = false;
            }, function (response) {
                this.loading = false;
            });
            return false;
        }
    }
})