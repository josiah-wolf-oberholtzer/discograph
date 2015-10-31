function dg_network_onNodeEnter(nodeEnter) {
    var nodeEnter = nodeEnter.append("g")
        .attr("class", function(d) {
            var classes = [
                "node",
                d.key,
                d.key.split('-')[0],
                ];
            return classes.join(" ");
        })
        .style("fill", function(d) {
            if (d.type == 'artist') {
                return dg_color_heatmap(d);
            } else {
                return dg_color_greyscale(d);
            }
        })
        .call(dg.network.forceLayout.drag);
    dg_network_onNodeEnterElementConstruction(nodeEnter);
    dg_network_onNodeEnterEventBindings(nodeEnter);
}

function dg_network_onNodeEnterElementConstruction(nodeEnter) {

    var artistEnter = nodeEnter.select(function(d) {
        return d.type == 'artist' ? this : null;
    });
    artistEnter
        .append("circle")
        .attr("class", "shadow")
        .attr("cx", 5)
        .attr("cy", 5)
        .attr("r", function(d) {
            return 7 + dg_network_getOuterRadius(d)
        });
    artistEnter
        .select(function(d, i) {return 0 < d.size ? this : null; })
        .append("circle")
        .attr("class", "outer")
        .attr("r", dg_network_getOuterRadius);
    artistEnter
        .append("circle")
        .attr("class", "inner")
        .attr("r", dg_network_getInnerRadius);

    var labelEnter = nodeEnter.select(function(d) {
        return d.type == 'label' ? this : null;
    });
    labelEnter
        .append("rect")
        .attr("class", "inner")
        .attr("height", function(d) { return 2 * dg_network_getInnerRadius(d); })
        .attr("width", function(d) { return 2 * dg_network_getInnerRadius(d); })
        .attr("x", function(d) { return -1 * dg_network_getInnerRadius(d); })
        .attr("y", function(d) { return -1 * dg_network_getInnerRadius(d); });
    nodeEnter.append("path")
        .attr("class", "more")
        .attr("d", d3.svg.symbol().type("cross").size(64))
        .style("opacity", function(d) {return 0 < d.missing ? 1 : 0; });
    nodeEnter.append("title")
        .text(function(d) { return d.name; });
}

function dg_network_onNodeEnterEventBindings(nodeEnter) {
    nodeEnter.on("dblclick", function(d) {
        if (!dg.network.isUpdating) { dg_network_navigate(d.key, true); }
    });
    nodeEnter.on("mousedown", function(d) {
        if (!dg.network.isUpdating) {
            dg.network.pageData.nodes.forEach(function(n) { n.fixed = false; });
            d.fixed = true;
            dg_network_selectNode(d.key);
        }
        d3.event.stopPropagation(); // Prevents propagation to #svg element.
    });
    nodeEnter.on("mouseover", function(d) {
        var selection = dg.network.selections.node.select(function(n) {
            return n.key == d.key ? this : null;
        });
        selection.moveToFront();
    });
    nodeEnter.on("touchstart", function(d) {
        var thisTime = $.now();
        var lastTime = d.lastTouchTime;
        d.lastTouchTime = thisTime;
        if (!lastTime || (500 < (thisTime - lastTime))) {
            if (!dg.network.isUpdating) {
                dg.network.pageData.nodes.forEach(function(n) { n.fixed = false; });
                d.fixed = true;
                dg_network_selectNode(d.key);
            }
        } else if ((thisTime - lastTime) < 500) {
            if (!dg.network.isUpdating) { dg_network_navigate(d.key, true); }
        }
        d3.event.stopPropagation(); // Prevents propagation to #svg element.
    });
}

function dg_network_onNodeExit(nodeExit) {
    nodeExit.remove();
}

function dg_network_onNodeUpdate(nodeUpdate) {
    nodeUpdate.transition()
        .duration(1000)
        .style("fill", function(d) {
            if (d.type == 'artist') {
                return dg_color_heatmap(d);
            } else {
                return dg_color_greyscale(d);
            }
        })
    nodeUpdate.selectAll(".more").each(function(d, i) {
        var prevMissing = Boolean(d.hasMissing);
        var prevMissingByPage = Boolean(d.hasMissingByPage);
        var currMissing = Boolean(d.missing);
        if (!d.missingByPage) {
            var currMissingByPage = false;
        } else {
            var currMissingByPage = Boolean(
                d.missingByPage[dg.network.pageData.currentPage]
                );
        }
        d3.select(this).transition().duration(1000)
            .style('opacity', function(d) {
                return (currMissing || currMissingByPage) ? 1 : 0;
                })
            .attrTween('transform', function(d) {
                var start = prevMissingByPage ? 45 : 0;
                var stop = currMissingByPage ? 45 : 0;
                return d3.interpolateString(
                    "rotate(" + start + ")",
                    "rotate(" + stop + ")"
                    );
                });
        d.hasMissing = currMissing;
        d.hasMissingByPage = currMissingByPage;
    });
}