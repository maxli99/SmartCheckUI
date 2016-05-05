var current_request;
var vm = new Vue({
    el: ".scui-ne",
    data: {
        opertype: "",
        operation: "",
        formdata: {
            id: "",
            name: "",
            host: "",
            port: "",
            user: "",
            passwd: "",
            conntype: "SSH",
            type: "MME"
        },
        test_ok: false,
        test_failed: false,
        untested: true,
        loading: false,
    },
    methods: {
        verify_ne: function (event) {
            this.$data.untested = true;
            this.$data.test_ok = false;
            this.$data.test_failed = false;
            this.$data.loading = true;
            if ($("input,select,textarea").not("[type=submit]").jqBootstrapValidation("hasErrors")) {
                this.$data.loading = false;
                this.$data.untested = false;
                this.$data.test_ok = false;
                this.$data.test_failed = true;
                return false;
            }
            var self = this.$data;
            event.preventDefault();
            event.stopImmediatePropagation();

            current_request = $.post(SCRIPT_ROOT + 'verify',
                JSON.stringify(self.formdata),
                function (msg) {
                    if (msg.success) {
                        new PNotify({
                            title: "",
                            animation: "show",
                            styling: 'bootstrap3',
                            hide: true,
                            delay: 5000,
                            text: "测试通过！",
                            type: "success",
                        });
                        self.test_ok = true;
                        self.untested = false;
                        self.test_failed = false;
                    } else {
                        new PNotify({
                            title: "",
                            animation: "show",
                            styling: 'bootstrap3',
                            hide: true,
                            delay: 5000,
                            text: "测试失败！",
                            type: "error"
                        });
                        self.untested = false;
                        self.test_failed = true;
                        self.test_ok = false;
                    }
                    self.loading = false;
                }
            )
            return false;
        },
    }
})

var grid = $("#grid-data").bootgrid({
    ajax: true,
    templates: {
        header: "<div id=\"{{ctx.id}}\" class=\"{{css.header}}\"><div class=\"row\"><div class=\"col-sm-12 actionBar\"><div class=\"add-item pull-left\"><button class=\"btn btn-default\"><span class=\"glyphicon glyphicon-plus\"></span></button></div><p class=\"{{css.search}}\"></p><p class=\"{{css.actions}}\"></p></div></div></div>",
    },
    post: function ()
    {
        return {
            id: "b0df282a-0d67-40e5-8558-c9e93b7befed"
        };
    },
    url: SCRIPT_ROOT+"",
    formatters: {
        "commands": function(column, row)
        {
            return "<button type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\"><i class=\"icon-pencil\"></i></button> " +
                "<button type=\"button\" class=\"btn btn-xs btn-default command-delete\" data-row-id=\"" + row.id + "\"><i class=\"icon-trash\"></i></button>";
        }
    }
}).on("loaded.rs.jquery.bootgrid", function()
{
    /* Executes after data is loaded and rendered */
    grid.find(".command-edit").on("click", function(e)
    {
        current_request = $.post(SCRIPT_ROOT + 'get',
            JSON.stringify({id: $(this).data('row-id')}),
            function (result) {
                vm.$data.formdata.id = result.ne.id;
                vm.$data.formdata.name = result.ne.name;
                vm.$data.formdata.host = result.ne.address;
                vm.$data.formdata.port = result.ne.port;
                vm.$data.formdata.user = result.ne.user;
                vm.$data.formdata.passwd = result.ne.passwd;
                vm.$data.formdata.type = result.ne.type;
                vm.$data.formdata.conntype = result.ne.conntype;

                vm.$data.opertype = "修改网元";
                vm.$data.operation = SCRIPT_ROOT+"edit";
                $(vm.$els.modal).modal('toggle');
            }
        );
    }).end().find(".command-delete").on("click", function(e)
    {
        current_request = $.post(SCRIPT_ROOT + 'get',
            JSON.stringify({id: $(this).data('row-id')}),
            function (result) {
                swal({
                        title: "删除网元",
                        text: "是否删除网元 "+ result.ne.name,
                        type: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "确定",
                        cancelButtonText: "取消",
                        closeOnConfirm: true,
                        closeOnCancel: true},
                    function(isConfirm){
                        if (isConfirm) {
                            current_request = $.post(SCRIPT_ROOT + 'delete',
                                JSON.stringify({id: result.ne.id}),
                                function (result) {
                                    if (result.success) {
                                        swal("删除", "删除成功", "success");
                                    } else {
                                        swal("删除", "删除失败", "error");
                                    }
                                    $("#grid-data").bootgrid('reload');
                                }
                            );
                        }
                    }
                );
            }
        );

    });
});

$('.add-item').click(function(){
    vm.$data.opertype = "添加网元";
    vm.$data.operation = SCRIPT_ROOT+"add";
    $(vm.$els.modal).modal('toggle');
});

$(vm.$els.modal).on("hide.bs.modal", function () {
    if (current_request) {
        current_request.abort();
    }
    $("input,select,textarea").jqBootstrapValidation("destroy");
    $("input,select,textarea").not("[type=submit]").jqBootstrapValidation();
    vm.$data.loading = false;
    vm.$data.test_ok = false;
    vm.$data.test_failed = false;
    vm.$data.untested = true;
    vm.$data.formdata = {
        id: "",
        name: "",
        host: "",
        port: "",
        user: "",
        passwd: "",
        type: "MME",
        conntype: "SSH"
    };
});

