var RBFK_HOME = {
    // プロパティ
};

/**
 * 画面読み込み時処理
 */
RBFK_HOME.onLoad = function() {
    // 緊急停止監視開始
    watchEmergencyStatus();
    changeEmergencyStatus(false);

    // 緊急停止ボタン
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
        content: '発報しました',
        trigger: 'manual'
    });

    // 手動・自動
    $('.button-vehicle-auto, .button-vehicle-manual').click(function() {
        var $this = $(this);
        var vehicleId = $this.data('vehicle-id');
        var isToAuto = $this.data('is-to-auto');

        $.ajax({
            url: '/api/vehicle/auto_flag/' + vehicleId,
            method: 'POST',
            data: {
                set_auto_flag: isToAuto ? 1 : 0
            }
        }).done(function(data) {
            if (data["result"] && data["result"] === true) {
                $this.popover('show');
                setTimeout(function() {
                    $this.popover('hide');
                }, 1500);
            }
        });
    });
    $('.button-vehicle-auto, .button-vehicle-manual').popover({
        content: '送信しました',
        placement: 'left',
        trigger: 'manual'
    });

    // 車両停止
    $('.button-vehicle-stop').click(function() {
        var $this = $(this);
        var vehicleId = $this.data('vehicle-id');

        $.ajax({
            url: '/api/emergency/' + rbfkHomeIndexLocationId + '/execute',
            method: 'POST',
            data: {
                emergency_type: "0",
                vehicle_id: vehicleId,
                // is_cancel: isCancel ? "1" : "",
            }
        }).done(function(data) {
            if (data["result"] && data["result"] === true) {
                $this.popover('show');
                setTimeout(function() {
                    $this.popover('hide');
                }, 1500);
            }
        });
    });
    $('.button-vehicle-stop').popover({
        content: '停止要求を送信しました',
        placement: 'left',
        trigger: 'manual'
    });

    // 運行開始
    $('.button-route-execute').click(function() {
        var $this = $(this);
        var routeId = $this.data('route-id');

        $.ajax({
            url: '/api/operation_plan/' + routeId + '/execute'
        }).done(function(data) {
            if (data["result"] && data["result"] === true) {
                $this.popover('show');
                setTimeout(function() {
                    $this.popover('hide');
                }, 1500);
            }
        });
    });
    $('.button-route-execute').popover({
        content: '運行要求を送信しました',
        placement: 'left',
        trigger: 'manual'
    });

    // 各車両と緊急停止を監視する
    function watchEmergencyStatus() {
        var client = new WebSocket("ws://" + window.location.host + "/vehicle_operation_status/" + rbfkHomeIndexLocationId);
        client.onmessage = function(event) {
            var parsedData = JSON.parse(event.data);

            // 各車両
            for (var i = 0; i < parsedData["vehicles"].length; i++) {
                $('#vehicle_status_1_' + parsedData["vehicles"][i]["id"]).text(parsedData["vehicles"][i]["vehicle_status"]["status_name"]);
                $('#vehicle_operation_name_1_' + parsedData["vehicles"][i]["id"]).text(
                    $('#operation_plan_' + parsedData["vehicles"][i]["vehicle_status"]["vehicle_operation_plan_id"]).text()
                );
            }

            // 緊急状態化？
            var isEmergency = false;
            for (var i = 0; i < parsedData["vehicles"].length; i++) {
                if (parsedData["vehicles"][i] && parsedData["vehicles"][i]["vehicle_status"]
                    && parsedData["vehicles"][i]["vehicle_status"]["status_code"] != 0) {
                    isEmergency = true;
                }
            }

            if (parsedData["status"] == 2) {
                changeEmergencyStatus(true);
            } else {
                changeEmergencyStatus(false);
            }

            changeEmergencyStatus(isEmergency);
        }
        client.onerror = function(error) {
            console.log(error);
        }
    }

    // 緊急停止時の外観を設定する
    function changeEmergencyStatus(isEmergency) {
        // ステータス毎の色やClass
        var bgColor = isEmergency ? "#FF4444" : "#8c8c8c";

        // 変化
        $('.app-container').css('backgroundColor', bgColor);
    }
};

/**
 * マップ画面 フォーククリック時処理(Vuejs連携用)
 */
RBFK_HOME.onRoboforkChangeStatus = function(vehicleId) {
    console.log('Fork#' + vehicleId + ' selected');
};

// 画面読み込み時処理
$(RBFK_HOME.onLoad);
