#!/usr/bin/env python3

import numpy as np
import pandas as pd
import bokeh.io
import bokeh.models
from bokeh.plotting import figure, output_file, show

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filepath')

args, extra_args = parser.parse_known_args()

filepath = args.filepath
if filepath == '-':
    filepath = '/dev/stdin'
with open(filepath) as f:
    lines = f.readlines()
# print(lines)
lines = [x for x in lines if not x.startswith('proc') and not x.startswith(' r')]
datas = [x.strip(' ').split() for x in lines]
# print(datas)
df = pd.DataFrame(datas, columns=['r', 'b', 'swpd', 'free', 'buff', 'cache', 'si', 'so', 'bi', 'bo', 'in', 'cs', 'us', 'sy', 'id', 'wa', 'st'])

# NOTE: for debug
print(df)

plot = figure(plot_width=600, plot_height=600, title="[vmstat] CPU usage")

plot.xaxis.axis_label = "elapsed time [sec]"
plot.yaxis.axis_label = "[%]"
plot.y_range = bokeh.models.Range1d(start=0.0, end=100.0)

x = np.linspace(0, len(df.index), len(df.index))
line_us = plot.line(x, df['us'], line_width=4, color="limegreen", alpha=0.5)
line_sy = plot.line(x, df['sy'], line_width=4, color="crimson", alpha=0.5)
line_us_sy = plot.line(x, (np.float_(df['us']) + np.float_(df['sy'])).tolist(), line_width=2, color="tomato", alpha=0.75)
line_id = plot.line(x, df['id'], line_width=4, color="lightsteelblue", alpha=0.5)
line_wa = plot.line(x, df['wa'], line_width=4, color="dodgerblue", alpha=0.5)

legend = bokeh.models.Legend(items=[
    ("us(user)[%]", [line_us]),
    ("sy(system)[%]", [line_sy]),
    ("us+sy(user+system)[%]", [line_us_sy]),
    ("id(idle)[%]", [line_id]),
    ("wa(wait)[%]", [line_wa]),
], location=(0, 0))
plot.add_layout(legend, 'below')
plot.legend.orientation = "horizontal"

plot.xaxis[0].ticker.desired_num_ticks = 10
plot.yaxis[0].ticker.desired_num_ticks = 10

filepath_svg = filepath + '.svg'
if filepath == '/dev/stdin':
    filepath_svg = 'vmstat.svg'
plot.output_backend = "svg"
print('[svg output]', filepath_svg)
bokeh.io.export_svgs(plot, filename=filepath_svg)
