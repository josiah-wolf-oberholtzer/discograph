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

function dg_network_linkTitle(d) {
    var source = d.source.name,
        role = d.role,
        target = d.target.name;
    if (role == "Alias") {
        return source + " ↔ (" + role + ") ↔ " + target;
    } else {
        return source + " → (" + role + ") → " + target;
    }
}

var nonAnnotatedRoles = [
    'Alias',
    'Member Of',
    'Sublabel Of',
    ]

function dg_network_linkAnnotation(d) {
    if (nonAnnotatedRoles.indexOf(d.role) != -1) {
        return null;
    } else {
        return d.role.split(' ').map(function(x) {
            return x[0];
        }).join('');
    }
}

function dg_network_onLinkEnterElementConstruction(linkEnter) {
    linkEnter.append("path")
        .attr("class", "inner")
        .append("title").text(dg_network_linkTitle);
    linkEnter.append("text")
        .attr('class', 'outer')
        .text(dg_network_linkAnnotation)
        .append("title").text(dg_network_linkTitle);
    linkEnter.append("text")
        .attr('class', 'inner')
        .text(dg_network_linkAnnotation)
        .append("title").text(dg_network_linkTitle);
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