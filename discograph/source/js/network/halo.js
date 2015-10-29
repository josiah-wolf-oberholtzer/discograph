function dg_network_onHaloEnter(haloEnter) {
    var haloEnter = haloEnter.append("g")
        .attr("class", function(d) {
            var classes = [
                "node",
                d.key,
                d.key.split('-')[0],
                ];
            return classes.join(" ");
        })
    haloEnter.append("circle")
        .attr("class", "halo")
        .attr("r", function(d) { return dg_network_getOuterRadius(d) + 40; });
}

function dg_network_onHaloExit(haloExit) {
    haloExit.remove();
}

