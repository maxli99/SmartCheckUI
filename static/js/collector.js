var vm = new Vue({
    el: ".scui_collector",
    data: {
        notshown: false,
        item_map: {},
        ne_map: {},
        item_view: {
            id: "",
            name: "",
            type: "",
            cond: "",
            desc: "",
            oper: "",
        },
        mme_check_item_num: 0,
        mme_check_item: "",
        mme_check_ne_num: 0,
        mme_check_ne: "",
        mme_check_cmd: [],
        saegw_check_item_num: 0,
        saegw_check_item: "",
        saegw_check_ne_num: 0,
        saegw_check_ne: "",
        saegw_check_cmd: [],
        check_data: {},
        loading: true,
        check_result: [],
        current_log: {},
        mail_unsend: true,
        mail_sending: false,
        send_text: "邮件验证",
        send_success: false,
        send_failed: false,
        mme_editor: [],
        saegw_editor: []
    },
    methods: {
        downloadlog: function(msg, event) {
            var form = $("<form>");
            form.attr('style', 'display:none');
            form.attr('target', '');
            form.attr('method', 'post');
            form.attr('action', SCRIPT_ROOT+"download");

            var input1 = $('<input>');
            input1.attr('type', 'hidden');
            input1.attr('name', 'filename');
            if (msg=='mme') {
                input1.attr('value', vm.$data.current_log['mme_log_zip']);
            } else if (msg=='saegw') {
                input1.attr('value', vm.$data.current_log['saegw_log_zip']);
            }
            $('body').append(form);
            form.append(input1);
            form.submit();
        },
        sendmail: function(msg, event) {
            this.$data.mail_sending = true;
            var self = this.$data;
            $.post(SCRIPT_ROOT+"sendmail",
                JSON.stringify({"filename": vm.$data.current_log}),
                function (msg) {
                    if (msg.success) {
                        self.send_text = "邮件发送成功";
                        self.send_success = true;
                        self.send_failed = false;
                        self.mail_unsend= false;
                        new PNotify({
                            title: "",
                            animation: "show",
                            styling: 'bootstrap3',
                            hide: true,
                            delay: 5000,
                            text: "邮件发送成功",
                            type: "success"
                        });
                    } else {
                        self.send_text = "邮件发送失败";
                        self.send_failed = true;
                        self.send_success = false;
                        self.mail_unsend= false;
                        new PNotify({
                            title: "",
                            animation: "show",
                            styling: 'bootstrap3',
                            hide: true,
                            delay: 5000,
                            text: "邮件发送失败",
                            type: "error"
                        });
                    }
                    self.mail_sending = false;
                    self.mail_unsend= false;
                }
            );
        },
    }
})

//for wizard
$('.wizard').wizard();


var grid_check_item = $("#grid-check-item").bootgrid({
    ajax: true,
    post: function ()
    {
        return {
            id: "b0df282a-0d67-40e5-8558-c9e93b7beccd"
        };
    },
    url: SCRIPT_ROOT+"getitems",
    selection: true,
    sorting: false,
    multiSelect: true,
    rowSelect: false,
    keepSelection: true,
    formatters: {
        "view": function(column, row)
        {
            return "<button type=\"button\" class=\"btn btn-xs btn-default command-view\" data-row-id=\"" + row.id + "\"><i class=\"icon-eye-open\"></i></button>";
        }
    }
}).on("selected.rs.jquery.bootgrid", function(e, rows)
{
    for (var i = 0; i < rows.length; i++)
    {
        vm.$data.item_map[rows[i].id] = true;
    }
}).on("deselected.rs.jquery.bootgrid", function(e, rows)
{
    for (var i = 0; i < rows.length; i++)
    {
        vm.$data.item_map[rows[i].id] = false;
    }

}).on("loaded.rs.jquery.bootgrid", function()
{
    grid_check_item.find(".command-view").on("click", function(e)
    {
        $.post(SCRIPT_ROOT + 'getitem',
            JSON.stringify({id: $(this).data('row-id')}),
            function (result) {
                if (!result.success) {
                    new PNotify({
                        title: "",
                        animation: "show",
                        styling: 'bootstrap3',
                        hide: true,
                        delay: 5000,
                        text: "查询失败！",
                        type: "error"
                    });
                }
                vm.$data.item_view.id = result.module.id;
                vm.$data.item_view.name = result.module.name;
                vm.$data.item_view.type = result.module.type;
                vm.$data.item_view.cond = result.module.cond;
                vm.$data.item_view.desc = result.module.desc;
                vm.$data.item_view.oper = result.module.oper;

                $(vm.$els.view_modal).modal('toggle');
            }
        );
    })
});

var grid_ne = $("#grid-ne").bootgrid({
    ajax: true,
    post: function ()
    {
        return {
            id: "b0df282a-0d67-40e5-8558-c9e93b7becff"
        };
    },
    url: SCRIPT_ROOT+"getne",
    selection: true,
    sorting:true,
    multiSelect: true,
    rowSelect: true,
    keepSelection: true,
}).on("selected.rs.jquery.bootgrid", function(e, rows)
{
    for (var i = 0; i < rows.length; i++)
    {
        vm.$data.ne_map[rows[i].id] = true;
    }
}).on("deselected.rs.jquery.bootgrid", function(e, rows)
{
    for (var i = 0; i < rows.length; i++)
    {
        vm.$data.ne_map[rows[i].id] = false;
    }

});

$('.wizard').on('changed.fu.wizard', function (evt, data) {
    if (data["step"] == 3) {
        for (i = 0; i<vm.$data.mme_editor.length; i++) {
            vm.$data.mme_editor[i].toTextArea(false);
        }
        for (i = 0; i<vm.$data.saegw_editor.length; i++) {
            vm.$data.saegw_editor[i].toTextArea(false);
        }
        vm.$data.mme_check_cmd = [];
        vm.$data.saegw_check_cmd = [];
        vm.$data.mme_editor = [];
        vm.$data.saegw_editor = [];

        $.post(SCRIPT_ROOT+"precheck",
            JSON.stringify({"item": vm.$data.item_map, "ne": vm.$data.ne_map}),
            function(msg) {
                vm.$data.check_data = msg;
                vm.$data.mme_check_ne_num = msg.ne_mme.length;
                vm.$data.mme_check_ne = msg.ne_mme_desc;
                vm.$data.mme_check_item_num = msg.item_mme.length;
                vm.$data.mme_check_item = msg.item_mme_desc;
                vm.mme_check_cmd = vm.mme_check_cmd.concat(msg.item_mme_cmd);
                vm.$data.saegw_check_ne_num = msg.ne_saegw.length;
                vm.$data.saegw_check_ne = msg.ne_saegw_desc;
                vm.$data.saegw_check_item_num = msg.item_saegw.length;
                vm.$data.saegw_check_item = msg.item_saegw_desc;
                vm.$data.saegw_check_cmd = msg.item_saegw_cmd;
                Vue.nextTick(function () {
                    var cmds = $(".command");
                    for (i=0; i<cmds.length; i++) {
                        var editor = CodeMirror.fromTextArea(cmds[i], {
                            mode: "shell",
                            theme: "seti",
                            lineWrapping: true,
                            lineNumbers: false,
                            matchBrackets: true,
                            autoRefresh: true,
                            delay: 500
                        });
                        $(editor.getWrapperElement()).poshytip({
                            content: $(cmds[i]).attr("title"),
                            className: 'tip-yellow',
                            alignTo: 'target',
                            alignX: 'inner-left',
                            alignY: 'top',
                            offsetX: 20,
                            offsetY: -3,
                            showOn: 'none',
                        });
                        editor.on("focus", function(e) {
                            $(e.getWrapperElement()).poshytip('show');
                        });
                        editor.on("blur", function(e){
                            $(e.getWrapperElement()).poshytip('hide');
                        });
                        if ($(cmds[i]).hasClass("mme-command")) {
                            vm.$data.mme_editor.push(editor)
                        } else if ($(cmds[i]).hasClass("saegw-command")) {
                            vm.$data.saegw_editor.push(editor)
                        }
                    }
                });
            });
    }
    if (data["step"] == 4) {
        vm.$data.loading = true;
        vm.$data.mail_unsend = true;
        vm.$data.send_success = false;
        vm.$data.send_failed = false;
        vm.$data.mail_sending = false;
        vm.$data.send_text = "邮件验证";
        mme_command = [];
        saegw_command = [];
        for (i = 0; i<vm.$data.mme_editor.length; i++) {
            mme_command.push(vm.$data.mme_editor[i].getValue());
        }
        for (i = 0; i<vm.$data.saegw_editor.length; i++) {
            saegw_command.push(vm.$data.saegw_editor[i].getValue());
        }
        $.post(SCRIPT_ROOT+"check",
            JSON.stringify({"check_data": vm.$data.check_data, "mme_command": mme_command, "saegw_command": saegw_command}),
            function(msg) {
                vm.$data.check_result = msg.result;
                vm.$data.current_log = msg.zipfile;
                vm.$data.loading = false; });
    }
});

