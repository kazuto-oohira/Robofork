if (typeof RBFK === "undefined") {
    var RBFK = {};
}

// テストデータ
RBFK.operationPlanData = {
    'master-markers-r': 8,
    'master-markers': [
        { x:69, y:104 },
        { x:69, y:198 },
        { x:69, y:198 },
        { x:194, y:245 },
        { x:194, y:245 },
        { x:231, y:198 },
        { x:231, y:198 },
        { x:231, y:104 }
    ]
};

RBFK.operationPlan = (function(global) {
    var self = function() {};

    var initialize = function() {
        var color = d3.scale.category10();
        self.svg = d3.select("#map-draw-layer");

        // マスターマーカーを設定
        self.svg.selectAll("circle").data(RBFK.operationPlanData['master-markers']).enter()
            .append('circle')
            .attr({
                'r': RBFK.operationPlanData['master-markers-r'],
                'fill': 'blue',
                'cx': function(d) { return d['x']; },
                'cy': function(d) { return d['y']; }
            })
            .style({ 'cursor': 'pointer' })
            .on('click', function(d) {
                alert(d['x'] + "/" + d['y']);
            });
    };

    self.initialize = initialize;

    return self;
})(window);

$(function() {
    RBFK.operationPlan.initialize();
});