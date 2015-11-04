function dg_color_greyscale(d) {
    var hue = 0;
    var saturation = 0;
    var lightness = (d.distance / (dg.network.data.maxDistance + 1));
    return d3.hsl(hue, saturation, lightness).toString();
}

function dg_color_heatmap(d) {
    var hue = ((d.distance / 12) * 360) % 360;
    var variation_a = ((d.id % 5) - 2) / 20;
    var variation_b = ((d.id % 9) - 4) / 80;
    var saturation = 0.67 + variation_a;
    var lightness = 0.5 + variation_b;
    return d3.hsl(hue, saturation, lightness).toString();
}

