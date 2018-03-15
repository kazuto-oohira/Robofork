$(function() {
    $('#button_start_operation').click(function() {
        $.ajax({
            url: '/api/operation_plan/1/execute'
        }).done(function(data) {
            if (data["result"] && data["result"] === true) {
                $('#button_start_operation').popover('show');
                setTimeout(function() {
                    $('#button_start_operation').popover('hide');
                }, 1500);
            }
        });
    });

    $('#button_start_operation').popover({
        content: '実行要求を送信しました',
        trigger: 'manual'
    });
});
