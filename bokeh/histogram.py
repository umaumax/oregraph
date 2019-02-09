#!/usr/bin/env python3
import os
import sys
import yaml
import pandas

import numpy as np

import bokeh
# NOTE: slow to import [0.5ms]
import bokeh.io
import bokeh.models


def gen_histogram_graph(title, filepath, fill_color, label, range, scale, unit, size):
    df = pandas.read_csv(filepath)
    data = df["data"]

    # NOTE: for e.g. convert ms -> sec
    # TODO: use scale['y']
    scale = scale['x']
    # NOTE: unitでhistogramのgraphの単位を調整
    # TODO: use unit['y']
    x_unit = unit['x']

    # NOTE: ある一定ごとの範囲に区切って、棒グラフを生成
    fuzzy_range_data = list(map(lambda x: int(x / x_unit) // scale, data))
    x_max = (np.amax(fuzzy_range_data) + 1)
    if range:
        # TODO: x_min = min(x_min, range['x']['min'])
        x_max = max(x_max, int(range['x']['max'] / x_unit))
    fuzzy_range_count = np.array([0] * x_max)
    for v in fuzzy_range_data:
        fuzzy_range_count[v] += 1
    print(list(fuzzy_range_data))
    y = fuzzy_range_count

    # NOTE: same processing
    # x = list(map(lambda x: x * x_unit, range(0, len(fuzzy_range_count))))
    n = len(fuzzy_range_count)
    x = np.linspace(0, n * x_unit, n)

    source = bokeh.models.ColumnDataSource(dict(x=x, top=y,))

    t = bokeh.models.annotations.Title()
    t.text = title
    plot = bokeh.models.Plot(
        title=t, plot_width=size['width'], plot_height=size['height'],
        h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)

    glyph = bokeh.models.glyphs.VBar(x="x", top="top", bottom=0, width=x_unit, fill_color=fill_color)
    plot.add_glyph(source, glyph)

    xaxis = bokeh.models.LinearAxis()
    plot.add_layout(xaxis, 'below')

    yaxis = bokeh.models.LinearAxis()
    plot.add_layout(yaxis, 'left')

    xaxis.axis_label = label['x_axis']
    yaxis.axis_label = label['y_axis']

    plot.add_layout(bokeh.models.Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(bokeh.models.Grid(dimension=1, ticker=yaxis.ticker))

    # NOTE: average line
    vline = bokeh.models.Span(location=np.average(data) / scale, dimension='height', line_color='red', line_width=3)
    plot.renderers.extend([vline])

    bokeh.io.curdoc().add_root(plot)

    # NOTE: svg
    plot.output_backend = "svg"
    svg_filepath = os.path.basename(filepath) + ".svg"
    print('[output]', svg_filepath)
    bokeh.io.export_svgs(plot, filename=svg_filepath)

    # NOTE: html
    # NOTE: for bokeh.io.show() and avoid below warning
    # UserWarning: save() called but no resources were supplied and output_file(...) was never called, defaulting to resources.CDN
    html_filepath = os.path.basename(filepath) + ".svg"
    bokeh.io.output_file(filename=html_filepath, mode='inline')
    # bokeh.io.save(plot, filename=os.path.basename(filepath) + ".html")
    # NOTE: このshowはlast plotに統一して表示されるため，for 1 graph?
    # bokeh.io.show(plot)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='plot.yml')
    args, extra_args = parser.parse_known_args()

    with open(args.file, 'r') as f:
        bokeh_plot = yaml.load(f)

    data_list = bokeh_plot['data']
    default_setting = bokeh_plot['default']
    print('default_setting', default_setting)
    for tmp_data in data_list:
        data = dict(default_setting)
        data.update(tmp_data)
        print('merged_data_setting', data)
        title = data['title']
        filepath = data['filepath']
        fill_color = data['fill_color']
        label = data['label']
        range = data['range']
        scale = data['scale']
        unit = data['unit']
        size = data['size']
        gen_histogram_graph(title, filepath, fill_color, label, range, scale, unit, size)
