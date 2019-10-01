$(function() {
    var json_url = "https://raw.githubusercontent.com/d3/d3-hierarchy/v1.1.8/test/data/flare.json";
    json_url = "./sample.json";
    d3.json(json_url).then(function(data) {
        var width = 640
        var height = 480
        var sort_flag = false;
        var partition;
        if (sort_flag) {
            partition = data => d3.partition()
                .size([height, width])
                .padding(1)
                (d3.hierarchy(data)
                    .sum(d => d.value)
                    .sort((a, b) => b.height - a.height || b.value - a.value))
        } else {
            partition = data => d3.partition()
                .size([height, width])
                .padding(1)
                (d3.hierarchy(data)
                    .sum(d => d.value)
                )
        }
        // var color_pattern = 'children';
        var color_pattern = 'ratio';
        var children_color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, data.children.length + 1))
        var parent_ratio_color = d3.interpolate("green", "yellow");
        var children_ratio_color = d3.interpolate("yellow", "red");
        var scale = 2.0;
        var format = d3.format(",d")
        var font_size = 16.0;
        var value_unit = '[ms]'; // or '%'

        const root = partition(data);

        var body = d3.select("body");
        body.append("text")
            .text(d => data.title);
        var svg = body.append("svg")
            .attr("viewBox", [0, 0, width, height])
            .style("font", font_size + "px sans-serif");

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
                if ('color' in d.data) {
                    return d.data['color'];
                }
                var has_child = 'children' in d;
                if (color_pattern == 'children') {
                    if (!d.depth) return "#ccc";
                    while (d.depth > 1) d = d.parent;
                    return children_color(d.data.name);
                } else if (color_pattern == 'ratio') {
                    var value = (d.x1 - d.x0) / height;
                    var ratio = value;
                    if (has_child) {
                        return parent_ratio_color(ratio / scale);
                    }
                    return children_ratio_color(ratio * scale);
                } else {
                    return '#ccc'
                }
            });

        const text = cell.filter(d => (d.x1 - d.x0) > 16).append("text")
            .attr("x", font_size)
            .attr("y", font_size)
            .attr("dx", "0em")
            .attr("dy", "0em")
        text.append("tspan")
            .text(d => d.data.name)
        text.append("tspan")
            .attr("x", font_size)
            .attr("dy", "1em")
            .attr("fill-opacity", 0.7)
            .text(d => d.value)
        text.append("tspan")
            .text(d => value_unit)
    }).catch(function(error) {
        console.log('json load error', error);
    });
});
