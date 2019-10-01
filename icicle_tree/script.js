$(function() {
    var json_url = "https://raw.githubusercontent.com/d3/d3-hierarchy/v1.1.8/test/data/flare.json";
    json_url = "./sample.json";
    d3.json(json_url).then(function(data) {
        var width = 640
        var height = 480
        var partition = data => d3.partition()
            .size([height, width])
            .padding(1)
            (d3.hierarchy(data)
                .sum(d => d.value)
                .sort((a, b) => b.height - a.height || b.value - a.value))
        console.log(data)
        console.log(data.children)
        var children_color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, data.children.length + 1))
        var ratio_color = d3.interpolate("green", "red");
        var scale = 2.0;
        var format = d3.format(",d")

        const root = partition(data);

        var body = d3.select("body");
        var svg = body.append("svg")
            .attr("viewBox", [0, 0, width, height])
            .style("font", "10px sans-serif");

        const cell = svg
            .selectAll("g")
            .data(root.descendants())
            .join("g")
            .attr("transform", d => `translate(${d.y0},${d.x0})`);

        cell.append("rect")
            .attr("width", d => d.y1 - d.y0)
            .attr("height", d => d.x1 - d.x0)
            .attr("fill-opacity", 0.6)
            .attr("fill", d => {
                if (!d.depth) return "#ccc";
                if (d.depth < -20) {
                    while (d.depth > 1) d = d.parent;
                    return children_color(d.data.name);
                } else {
                    var value = (d.x1 - d.x0) / height;
                    return ratio_color(value * scale);
                }
            });

        const text = cell.filter(d => (d.x1 - d.x0) > 16).append("text")
            .attr("x", 4)
            .attr("y", 13);

        text.append("tspan")
            .text(d => d.data.name);

        text.append("tspan")
            .attr("fill-opacity", 0.7)
            .text(d => ` ${format(d.value)}`);

        cell.append("title")
            .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);
    }).catch(function(error) {
        console.log('json load error', error);
    });
});
