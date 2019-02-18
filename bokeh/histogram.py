#!/usr/bin/env python3
import os
import os.path
import sys
import yaml
import pandas

import numpy as np

import bokeh
# NOTE: slow to import [0.5ms]
import bokeh.io
import bokeh.models


def gen_histogram_graph(title, input_filepath, fill_color, label, range, scale, unit, size, output):
    df = pandas.read_csv(input_filepath)
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
    x = np.linspace(0, n * x_unit, n + 1)

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

    # yticker = bokeh.models.CompositeTicker(tickers=[bokeh.models.BasicTicker(), bokeh.models.SingleIntervalTicker(interval=5, num_minor_ticks=5)])
    # plot.yaxis.formatter = bokeh.models.NumeralTickFormatter(format="4 0000")
    # plot.yaxis.formatter = bokeh.models.PrintfTickFormatter(format="% 4d")
    # yaxis = bokeh.models.LinearAxis(ticker=yticker)

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

    def parse_outputpath(output, ext):
        dirpath = output.get('dirpath') or '.'
        filename = output.get('filename') or os.path.basename(input_filepath) + '.' + ext
        filepath = output.get('filepath') or os.path.join(dirpath, filename)
        return filepath
    if output.get('svg') is not None:
        plot.output_backend = "svg"
        filepath = parse_outputpath(output['svg'], 'svg')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        print('[svg output]', filepath)
        bokeh.io.export_svgs(plot, filename=filepath)
    if output.get('html') is not None:
        filepath = parse_outputpath(output['html'], 'html')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        print('[html output]', filepath)
        bokeh.io.output_file(filename=filepath, mode='inline')
        bokeh.io.save(plot)

    # NOTE: this method show last plot (for only one graph?)
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
        output = data['output']
        gen_histogram_graph(title, filepath, fill_color, label, range, scale, unit, size, output)
