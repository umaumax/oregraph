$(function() {
    var json_url = "https://raw.githubusercontent.com/d3/d3-hierarchy/v1.1.8/test/data/flare.json";
    json_url = "./sample.json";
    d3.json(json_url).then(function(data) {
        var graph_pattern = 'horizontal';
        // var graph_pattern = 'vertical';
        var graph_func_map_table = {
            'horizontal': {
                'size': (width, height) => [height, width],
                'sort': (a, b) => b.height - a.height || b.value - a.value,
                'transform': d => `translate(${d.y0},${d.x0})`,
                'width': d => d.y1 - d.y0,
                'height': d => d.x1 - d.x0,
                'ratio': (d, width, height) => (d.x1 - d.x0) / height,
            },
            'vertical': {
                'size': (width, height) => [width, height],
                'sort': (a, b) => b.width - a.width || b.value - a.value,
                'transform': d => `translate(${d.x0},${d.y0})`,
                'width': d => d.x1 - d.x0,
                'height': d => d.y1 - d.y0,
                'ratio': (d, width, height) => (d.y1 - d.y0) / width,
            },
        };
        var grap_func_map = graph_func_map_table[graph_pattern];
        var width = 1200;
        var height = 640;
        var sort_flag = false;
        var partition;
        if (sort_flag) {
            partition = data => d3.partition()
                .size(grap_func_map['size'](width, height))
                .padding(1)
                (d3.hierarchy(data)
                    .sum(d => d.value)
                    .sort(grap_func_map['sort'])
                )
        } else {
            partition = data => d3.partition()
                .size(grap_func_map['size'](width, height))
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
            .attr("transform", grap_func_map['transform']);

        cell.append("rect")
            .attr("width", grap_func_map['width'])
            .attr("height", grap_func_map['height'])
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
                    var ratio = grap_func_map['ratio'](d, width, height);
                    if (has_child) {
                        return parent_ratio_color(ratio / scale);
                    }
                    return children_ratio_color(ratio * scale);
                } else {
                    return '#ccc'
                }
            });

        const text = cell.append("text")
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
