function dg_network_getOuterRadius(d) {
    if (0 < d.size) {
        return 12 + (Math.sqrt(d.size) * 2);
    }
    return 9 + (Math.sqrt(d.size) * 2);
}

function dg_network_getInnerRadius(d) {
    return 9 + (Math.sqrt(d.size) * 2);
}

function dg_network_splineInner(sX, sY, sR, cX, cY) {
    var dX = (sX - cX),
        dY = (sY - cY);
    var angle = Math.atan(dY / dX);
    dX = Math.abs(Math.cos(angle) * sR);
    dY = Math.abs(Math.sin(angle) * sR);
    sX = (sX < cX) ? sX + dX : sX - dX;
    sY = (sY < cY) ? sY + dY : sY - dY;
    return [sX, sY];
}

function dg_network_spline(d) {
    //console.log(d);
    var sX = d.source.x;
    var sY = d.source.y;
    var tX = d.target.x;
    var tY = d.target.y;
    var tR = d.target.radius;
    var sR = d.source.radius;
    if (d.intermediate) {
        var cX = d.intermediate.x;
        var cY = d.intermediate.y;
        sXY = dg_network_splineInner(sX, sY, sR, cX, cY);
        tXY = dg_network_splineInner(tX, tY, tR, cX, cY);
        return (
            "M " + sXY[0] + "," + sXY[1] + " " +
            "S " + cX + "," + cY + " " +
            " " + tXY[0] + "," + tXY[1] + " "
            );
    } else {
        return "M " + [sX, sY] + " L " + [tX, tY];
    }
}

function dg_network_getHullVertices(nodes) {
    var vertices = [];
    nodes.forEach(function(d) {
        var radius = d.radius;
        vertices.push([d.x + radius, d.y + radius]);
        vertices.push([d.x + radius, d.y - radius]);
        vertices.push([d.x - radius, d.y + radius]);
        vertices.push([d.x - radius, d.y - radius]);
    });
    return vertices;
}

var unlabeled_roles = [
    'Alias',
    'Member Of',
    'Sublabel Of',
    ];

function dg_network_tick_link(d, i) {
    var group = d3.select(this);
    var paths = group.selectAll('path');
    paths.attr('d', dg_network_spline(d));
    var x1 = d.source.x,
        y1 = d.source.y,
        x2 = d.target.x,
        y2 = d.target.y;
    //paths.attr("x1", x1).attr("y1", y1).attr("x2", x2).attr("y2", y2);
    if (unlabeled_roles.indexOf(d.role) == -1) {
        var path = paths.node();
        var point = path.getPointAtLength(path.getTotalLength() / 2);
        var x = point.x, y = point.y;
        var angle = Math.atan2((y2 - y1), (x2 - x1)) * (180 / Math.PI);
        var text = group.selectAll('text')
            .attr('dx', point.x)
            .attr('dy', point.y)
            .attr('transform', 'rotate(' + angle + ' ' + x + ' ' + y + ')');
    }
}

function dg_network_translate(d) {
    return "translate(" + d.x + "," + d.y + ")";
}

function dg_network_tick(e) {
    var k = e.alpha * 5;
    var centerNode = dg.network.data.nodeMap.get(dg.network.data.json.center.key);
    if (!centerNode.fixed) {
        var dims = dg.dimensions;
        var dx = ((dims[0] / 2) - centerNode.x) * k;
        var dy = ((dims[1] / 2) - centerNode.y) * k;
        centerNode.x += dx;
        centerNode.y += dy;
    }
    dg.network.selections.link.each(dg_network_tick_link);
    dg.network.selections.halo.attr("transform", dg_network_translate);
    dg.network.selections.node.attr("transform", dg_network_translate);
    dg.network.selections.text.attr("transform", dg_network_translate);
    dg.network.selections.hull.select("path").attr("d", function(d) {
        var vertices = d3.geom.hull(dg_network_getHullVertices(d.values));
        return "M" + vertices.join("L") + "Z"; });
}