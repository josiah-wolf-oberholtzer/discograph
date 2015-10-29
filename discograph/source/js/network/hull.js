function dg_network_onHullEnter(hullEnter) {
    var hullEnter = hullEnter.append("g")
        .attr("class", function(d) { return "hull hull-" + d.key });
    hullEnter.append("path");
}

function dg_network_onHullExit(hullExit) {
    hullExit.remove();
}

