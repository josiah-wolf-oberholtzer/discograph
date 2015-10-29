function dg_network_getNodeText(d) {
    var name = d.name;
    if (50 < name.length) {
        name = name.slice(0, 50) + "...";
    }
    if (dg.debug) {
        var pages = '[' + d.pages + ']';
        return pages + ' ' + name;
    }
    return name;
}

function dg_network_onTextEnter(textEnter) {
    var textEnter = textEnter.append("g")
        .attr("class", function(d) {
            var classes = [
                "node",
                d.key,
                d.key.split('-')[0],
                ];
            return classes.join(" ");
        })
    textEnter.append("text")
        .attr("class", "outer")
        .attr("dx", function(d) { return dg_network_getOuterRadius(d) + 3; })
        .attr("dy", ".35em")
        .text(dg_network_getNodeText);
    textEnter.append("text")
        .attr("class", "inner")
        .attr("dx", function(d) { return dg_network_getOuterRadius(d) + 3; })
        .attr("dy", ".35em")
        .text(dg_network_getNodeText);
}

function dg_network_onTextExit(textExit) {
    textExit.remove();
}

function dg_network_onTextUpdate(textUpdate) {
    textUpdate.select('.outer').text(dg_network_getNodeText);
    textUpdate.select('.inner').text(dg_network_getNodeText);
}

