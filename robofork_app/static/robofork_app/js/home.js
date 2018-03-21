$(function() {
    // TODO: 緊急停止状態を取得する
    changeEmergencyStatus(false);
    
    $('.button-emergency, .button-emergency-cancel').click(function() {
        var $this = $(this);
        var emergencyType = $this.data('emergency-type');
        var isCancel = $this.hasClass('button-emergency-cancel');
        $.ajax({
            url: '/api/emergency/' + rbfkHomeIndexLocationId + '/execute',
            method: 'POST',
            data: {
                emergency_type: emergencyType,
                is_cancel: isCancel ? "1" : "",
            }
        }).done(function(data) {
            if (data["result"] && data["result"] === true) {
                $this.parent().popover('show');
                setTimeout(function() {
                    $this.parent().popover('hide');
                }, 1500);
            }

            if (!isCancel) {
                changeEmergencyStatus(true);
            }
        });
    });

    $('.button-emergency, .button-emergency-cancel').parent().popover({
        content: '送信しました',
        trigger: 'manual'
    });

    function changeEmergencyStatus(isEmergency) {
        // ステータス毎の色やClass
        var bgColor = isEmergency ? "#FF4444" : "#8c8c8c";
        var labelClass = isEmergency ? "label-danger" : "label-success";
        var labelString = isEmergency ? "緊急停止中(車両単体含む)" : "通常運行中";

        // 変化
        $('.app-container').css('backgroundColor', bgColor);
        $('#emergency-status-label')
            .removeClass("label-danger label-success").addClass(labelClass);
        $('#emergency-status-label').text(labelString);
    }
});
