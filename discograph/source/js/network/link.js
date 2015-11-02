var tip = d3.tip()
    .attr('class', 'd3-tip')
    .direction('e')
    .offset([0, 20])
    .html(dg_network_tooltip);

function dg_network_onLinkEnter(linkEnter) {
    var linkEnter = linkEnter.append("g")
        .attr("class", function(d) {
            var parts = d.key.split('-');
            var role = parts.slice(2, 2 + parts.length - 4).join('-')
            var classes = [
                "link",
                "link-" + d.key,
                role,
                ];
            return classes.join(" ");
        });
    dg_network_onLinkEnterElementConstruction(linkEnter);
    dg_network_onLinkEnterEventBindings(linkEnter);
}

function dg_network_onLinkEnterElementConstruction(linkEnter) {
    linkEnter.append("path")
        .attr("class", "inner");
    linkEnter.append("text")
        .attr('class', 'outer')
        .text(dg_network_linkAnnotation);
    linkEnter.append("text")
        .attr('class', 'inner')
        .text(dg_network_linkAnnotation);
}

function dg_network_onLinkEnterEventBindings(linkEnter) {
    var debounce = $.debounce(250, function(self, d, status) {
        if (status) {
            tip.show(d, d3.select(self).select('text').node());
        } else {
            tip.hide(d);
        }
    });
    linkEnter.on("mouseover", function(d) {
        d3.select(this).select(".inner")
            .transition()
            .style("stroke-width", 3);
        debounce(this, d, true);
    });
    linkEnter.on("mouseout", function(d) {
        d3.select(this).select(".inner")
            .transition()
            .duration(500)
            .style("stroke-width", 1);
        debounce(this, d, false);
    });
}

function dg_network_tooltip(d) {
    var parts = [
        '<p>' + d.source.name + '</p>',
        '<p><strong>&laquo; ' + d.role + ' &raquo;</strong></p>',
        '<p>' + d.target.name + '</p>',
        ];
    return parts.join('');
}

function dg_network_linkAnnotation(d) {
    return d.role.split(' ').map(function(x) { return x[0]; }).join('');
}

function dg_network_onLinkExit(linkExit) {
    linkExit.remove();
}

function dg_network_onLinkUpdate(linkSelection) {
}