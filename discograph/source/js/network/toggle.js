function dg_network_toggle(status) {
    if (status) {
        dg.network.forceLayout.stop()
        dg.network.isUpdating = true;
        dg.network.layers.root.transition()
            .duration(250)
            .style("opacity", 0.333);
        dg.network.layers.link.selectAll('.link')
            .classed('noninteractive', true);
        dg.network.layers.node.selectAll('.node')
            .classed('noninteractive', true);
    } else {
        dg.network.forceLayout.resume();
        dg.network.layers.root.transition()
            .delay(250)
            .duration(1000)
            .style("opacity", 1)
            .each('end', function(d, i) {
                dg.network.isUpdating = false;
                dg.network.layers.link.selectAll('.link')
                    .classed('noninteractive', false);
                dg.network.layers.node.selectAll('.node')
                    .classed('noninteractive', false);
            });
    }
}