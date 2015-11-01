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
    var aggregateRoleNames = [
        "Member Of", "Sublable Of",
        "Released On", "Compiled On",
        ]
    linkEnter.append("path")
        .attr("class", "inner")
    /*
    linkEnter.append("path")
        .attr("class", "outer")
    */
        .append("title").text(function(d) {
            var source = d.source.name,
                role = d.role,
                target = d.target.name;
            if (role == "Alias") {
                return source + " ↔ (" + role + ") ↔ " + target;
            } else {
                return source + " → (" + role + ") → " + target;
            }
        });
    linkEnter.append("text")
        .attr('class', 'outer')
        .text(function(d) {
            if (['Alias', 'Member Of', 'Sublabel Of'].indexOf(d.role) != -1) {
                return null;
            } else {
                return d.role.split(' ').map(function(x) {
                    return x[0];
                }).join('');
            }
        });
    linkEnter.append("text")
        .attr('class', 'inner')
        .text(function(d) {
            if (['Alias', 'Member Of', 'Sublabel Of'].indexOf(d.role) != -1) {
                return null;
            } else {
                return d.role.split(' ').map(function(x) {
                    return x[0];
                }).join('');
            }
        });
}

function dg_network_onLinkEnterEventBindings(linkEnter) {
    linkEnter.on("mouseover", function(d) {
        d3.select(this).select(".inner")
            .transition()
            .style("stroke-width", 3);
        });
    linkEnter.on("mouseout", function(d) {
        d3.select(this).select(".inner")
            .transition()
            .duration(500)
            .style("stroke-width", 1);
    });
}

function dg_network_onLinkExit(linkExit) {
    linkExit.remove();
}

function dg_network_onLinkUpdate(linkSelection) {
    if (dg.debug) {
        linkSelection.select('text').text(function(d) {
            return "[" + d.pages + "]";
        });
    }
}
