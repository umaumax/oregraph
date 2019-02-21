#!/usr/bin/env python3

from bokeh.plotting import figure, output_file, show
import bokeh.io
import bokeh.models
import numpy as np
import pandas as pd
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filepath')

args, extra_args = parser.parse_known_args()

filepath = args.filepath
with open(filepath) as f:
    lines = f.readlines()
# NOTE: remove 3lines
del lines[:3]
# print(lines)

datas = [x.strip(' ').split() for x in lines]
# print(datas)

# 09:28:35 PM   UID       PID    %usr %system  %guest    %CPU   CPU  Command
df = pd.DataFrame(datas, columns=['time', 'AM/PM', 'UID', 'PID', 'usr', 'system', 'guest', 'CPU rate', 'CPU no', 'COMMAND'])

# NOTE: for debug
print(df)

plot = figure(plot_width=600, plot_height=600, title="[pidstat] CPU usage")

plot.xaxis.axis_label = "elapsed time [sec]"
plot.yaxis.axis_label = "[%]"
plot.y_range = bokeh.models.Range1d(start=0.0, end=100.0)

x = np.linspace(0, len(df.index), len(df.index))
line_usr = plot.line(x, df['usr'], line_width=4, color="limegreen", alpha=0.5)
line_system = plot.line(x, df['system'], line_width=4, color="crimson", alpha=0.5)
line_usr_system = plot.line(x, (np.float_(df['usr']) + np.float_(df['system'])).tolist(), line_width=2, color="tomato", alpha=0.75)
line_guest = plot.line(x, df['guest'], line_width=4, color="dodgerblue", alpha=0.5)

legend = bokeh.models.Legend(items=[
    ("usr[%]", [line_usr]),
    ("system[%]", [line_system]),
    ("usr+system[%]", [line_usr_system]),
    ("guest[%]", [line_guest]),
], location=(0, 0))
plot.add_layout(legend, 'below')
plot.legend.orientation = "horizontal"

plot.xaxis[0].ticker.desired_num_ticks = 10
plot.yaxis[0].ticker.desired_num_ticks = 10

filepath_svg = filepath + '.svg'
plot.output_backend = "svg"
print('[svg output]', filepath_svg)
bokeh.io.export_svgs(plot, filename=filepath_svg)
