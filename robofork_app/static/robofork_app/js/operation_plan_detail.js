if (typeof RBFK === "undefined") {
    var RBFK = {};
}

RBFK.operationPlan = (function(global) {
    var self = function() {};

    self.init = function() {
        var color = d3.scale.category10();
        var svg = d3.select("#map-draw-layer");
        svg.append('circle').attr({
            'cx': 100,
            'cy': 90,
            'r': 20,
            'fill': color(0),
        });
    };

    return self;
})(window);

$(function() {
    RBFK.operationPlan.init();
});