function dg_network_init() {
    var root = d3.select("#svg").append("g").attr("id", "networkLayer");
    dg.network.layers.root = root;
    dg.network.layers.halo = root.append("g").attr("id", "haloLayer");
    dg.network.layers.link = root.append("g").attr("id", "linkLayer");
    dg.network.layers.node = root.append("g").attr("id", "nodeLayer");
    dg.network.layers.text = root.append("g").attr("id", "textLayer");
    dg.network.selections.halo = dg.network.layers.halo.selectAll(".node");
    dg.network.selections.hull = dg.network.layers.halo.selectAll(".hull");
    dg.network.selections.link = dg.network.layers.link.selectAll(".link");
    dg.network.selections.node = dg.network.layers.node.selectAll(".node");
    dg.network.selections.text = dg.network.layers.text.selectAll(".node");
    dg.network.forceLayout = dg_network_setupForceLayout();
}