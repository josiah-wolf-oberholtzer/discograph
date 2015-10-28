function dg_warn() {
}

function dg_style_loading(state) {
    if (state) {
        dg.network.layers.root.transition()
            .duration(250)
            .style("opacity", 0.333);
        $("#page-loading")
            .removeClass("glyphicon-random")
            .addClass("glyphicon-animate glyphicon-refresh");
    } else {
        dg.network.layers.root.transition()
            .delay(250)
            .duration(1000)
            .style("opacity", 1);
        $("#page-loading")
            .removeClass("glyphicon-animate glyphicon-refresh")
            .addClass("glyphicon-random");
    }
}

function dg_svg_init() {
    d3.selection.prototype.moveToFront = function() {
        return this.each(function(){ this.parentNode.appendChild(this); });
    };
    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0];
    dg.network.dimensions = [
        w.innerWidth || e.clientWidth || g.clientWidth,
        w.innerHeight|| e.clientHeight|| g.clientHeight,
    ];
    dg.network.newNodeCoords = [
        dg.network.dimensions[0] / 2,
        dg.network.dimensions[1] / 2,
    ];
    window.addEventListener("resize", function() {
        dg.network.dimensions = [
            w.innerWidth || e.clientWidth || g.clientWidth,
            w.innerHeight|| e.clientHeight|| g.clientHeight,
        ];
        d3.select("#svg")
            .attr("width", dg.network.dimensions[0])
            .attr("height", dg.network.dimensions[1]);
        dg.timeline.layers.root.select('g')
            .attr('transform', "translate(" +
                dg.network.dimensions[0] / 2 +
                "," +
                dg.network.dimensions[1] / 2 +
                ")"
                );
        dg.network.forceLayout.size(dg.network.dimensions).start();
    });
    d3.select("#svg")
        .attr("width", dg.network.dimensions[0])
        .attr("height", dg.network.dimensions[1]);
    dg_svg_setupDefs();
}

function dg_svg_setupDefs() {
    var defs = d3.select("#svg").append("defs");
    // ARROWHEAD
    defs.append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "-5 -5 10 10")
        .attr("refX", 4)
        .attr("refY", 0)
        .attr("markerWidth", 8)
        .attr("markerHeight", 8)
        .attr("markerUnits", "strokeWidth")
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M 0,0 m -5,-5 L 5,0 L -5,5 L -2.5,0 L -5,-5 Z")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round");
    // AGGREGATE
    defs.append("marker")
        .attr("id", "aggregate")
        .attr("viewBox", "-5 -5 10 10")
        .attr("refX", 5)
        .attr("refY", 0)
        .attr("markerWidth", 8)
        .attr("markerHeight", 8)
        .attr("markerUnits", "strokeWidth")
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M 0,0 m 5,0 L 0,-3 L -5,0 L 0,3 L 5,0 Z")
        .attr("fill", "#fff")
        .attr("stroke", "#000")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 1.5);
    // GAUSSIAN BLUR
    var filter = defs.append("filter")
        .attr("id", "drop-shadow")
        .attr("y", "-50%")
        .attr("x", "-50%")
        .attr("height", "300%")
        .attr("width", "300%");
    filter.append("feGaussianBlur")
        .attr("in", "SourceAlpha")
        .attr("stdDeviation", 3)
        .attr("result", "blur");
    filter.append("feOffset")
        .attr("in", "blur")
        .attr("dx", 4)
        .attr("dy", 4)
        .attr("result", "offsetBlur");
    var feComponentTransfer = filter.append("feComponentTransfer")
        .attr("in", "offsetBlur")
        .attr("result", "lightenedBlur");
    feComponentTransfer.append("feFuncA")
        .attr("type", "linear")
        .attr("slope", 0.25)
        .attr("intercept", 0);
    var feMerge = filter.append("feMerge");
    feMerge.append("feMergeNode")
        .attr("in", "lightenedBlur")
    feMerge.append("feMergeNode")
        .attr("in", "SourceGraphic");
    // RADIAL GRADIENT
    var gradient = defs.append('radialGradient')
        .attr('id', 'radial-gradient');
    gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '100%');
    gradient.append('stop')
        .attr('offset', '50%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '33%');
    gradient.append('stop')
        .attr('offset', '75%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '11%');
    gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', '#333')
        .attr('stop-opacity', '0%');
}

$(document).ready(function() {
    dg_svg_init();
    dg_network_init();
    dg_timeline_init();
    dg_typeahead_init();
    if (dgData) {
        var params = {'roles': $('#filter select').val()};
        dg_history_replaceState(dgData.center.key, params);
        dg_network_handleAsyncData(dgData, false);
    }
    $('[data-toggle="tooltip"]').tooltip();
    (function() {
        var click = $.debounce(300, function() {
            var url = '/api/random?' + Math.floor(Math.random() * 1000000);
            if (!dg.network.isUpdating) {
                dg.network.layers.root.transition()
                    .style("opacity", 0.333);
                $("#page-loading")
                    .removeClass("glyphicon-random")
                    .addClass("glyphicon-animate glyphicon-refresh");
                d3.json(url, function(error, json) {
                    if (error) { dg_network_handleAsyncError(error); return; }
                    dg_network_navigate(json.center, true);
                });
            } else {
                dg_warn();
            }
        });
        $('#brand').on("click touchstart", function(event) {
            click();
            $(this).tooltip('hide');
            event.preventDefault();
        });
    }());
    $('#paging .previous a').click(function(event) {
        dg_network_prevPage();
        $(this).tooltip('hide');
        event.preventDefault();
    });
    $('#paging .next a').click(function(event) {
        dg_network_nextPage();
        $(this).tooltip('hide');
        event.preventDefault();
    });
    $('#filter-roles').multiselect({
        buttonWidth: "160px",
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        //includeSelectAllOption: true,
        inheritClass: true,
        enableClickableOptGroups: true,
        maxHeight: 400,
        nonSelectedText: 'Select relationships'
    });
    $('#filter').on('reset', function(event) {
        $('#filter-roles option:selected').each(function() {
            $(this).prop('selected', false);
        });
        $('#filter-roles').multiselect('refresh');
        event.preventDefault();
    });
    $('#filter').submit(function(event) {
        dg_network_navigate(dg.network.data.json.center.key, true);
        event.preventDefault();
    });
    $('#filter').fadeIn(3000);
    window.addEventListener("popstate", dg_history_onPopState);
    console.log('discograph initialized.');
});

dg.selectPage = function(page) {
    dg_network_selectPage(page);
    dg_network_startForceLayout();
}

function makeArcs() {
    var start = Date.now();
    var data = [
        {value: 1}, {value: 2}, {value: 3}, {value: 4},
        {value: 5}, {value: 6}, {value: 7}, {value: 8},
        ];
    dg.timeline.layers.root.selectAll('g').remove();
    var group = dg.timeline.layers.root.append('g')
        .attr('class', 'radial')
        .attr('transform', 'translate(' +
            dg.network.dimensions[0] / 2 +
            ',' +
            dg.network.dimensions[1] / 2 +
            ')'
            );
    var arc = d3.svg.arc()
        .startAngle(function(d) { return d.startAngle; })
        .endAngle(function(d) { return d.endAngle; })
        .innerRadius(function(d) { return d.innerRadius; })
        .outerRadius(function(d) { return d.outerRadius; });
    var barHeight = 200;
    var barScale = d3.scale.linear()
        .domain([1, 8])
        .range([barHeight / 4, barHeight]);
    var segments = group.selectAll('path')
        .data(data)
        .enter().append('path')
        .attr('class', 'arc')
        .each(function(d, i) { 
            d.startAngle = 2 * Math.PI * Math.random();
            d.endAngle = 2 * Math.PI * Math.random();
            d.rotationRate = Math.random() * 10;
            d.innerRadius = 0;
            d.outerRadius = 0;
        })
        .attr('d', arc);
    segments.transition()
        .ease("elastic")
        .duration(500)
        .delay(function(d, i) { return (data.length - i) * 50; })
        .attrTween('d', function(d, i) {
            var inner = d3.interpolate(d.innerRadius, barScale(d.value - 1));
            var outer = d3.interpolate(d.outerRadius, barScale(d.value));
            return function(t) {
                d.innerRadius = inner(t);
                d.outerRadius = outer(t);
                return arc(d, i);
            };
        });
    d3.timer(function() {
        if (dg.network.isUpdating) {
            return true;
        }
        segments.attr('transform', function(d) {
            var angle = (Date.now() - start) * d.rotationRate;
            if (0 < d.outerRadius) {
                angle = angle / d.outerRadius;
            }
            return 'rotate(' + angle + ')';
        });
    });
}