#!/usr/bin/env python3

import argparse
import sys
import pandas as pd
import numpy as np
import bokeh.models
import bokeh.io
from bokeh.plotting import figure
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()


parser = argparse.ArgumentParser()
parser.add_argument(
    '-t',
    '--type',
    default='time-series',
    help='time-series, countup')
parser.add_argument('filepath')

args, extra_args = parser.parse_known_args()

filepath = args.filepath

# man ps
"""
    D    uninterruptible sleep (usually IO)
    R    running or runnable (on run queue)
    S    interruptible sleep (waiting for an event to complete)
    T    stopped by job control signal
    t    stopped by debugger during the tracing
    W    paging (not valid since the 2.6.xx kernel)
    X    dead (should never be seen)
    Z    defunct ("zombie") process, terminated but not reaped by its parent
"""

colormap = {
    'D': 'darkblue',
    'R': 'green',
    'S': 'powderblue',
    'T': 'red',
    't': 'orange',
    'W': 'brown',
    'X': 'black',
    'Z': 'blue',
}

legendmap = {
    'D': 'D: uninterruptible sleep (usually IO)',
    'R': 'R: running or runnable (on run queue)',
    'S': 'S: interruptible sleep (waiting for an event to complete)',
    'T': 'T: stopped by job control signal',
    't': 't: stopped by debugger during the tracing',
    'W': 'W: paging (not valid since the 2.6.xx kernel)',
    'X': 'X: dead (should never be seen)',
    'Z': 'Z: defunct ("zombie") process, terminated but not reaped by its parent',
}

plot = figure(
    plot_width=1200,
    plot_height=1200,
    title="[thread-viz] threads state")


def process_time_series(plot, filepath):
    with open(filepath) as f:
        lines = f.readlines()

    datas = [x.strip(' ').split() for x in lines]

    if len(datas) == 0:
        print('No data')
        sys.exit(1)

    n_data_header = len(datas[0])
    if n_data_header == 3:
        df = pd.DataFrame(
            datas,
            columns=[
                'time',
                'tid',
                'state',
            ])
    else:
        print('Syntax error: data length is {}'.format(n_data_header))
        sys.exit(1)

    # NOTE: for debug
    print(df)

    plot.xaxis.axis_label = "elapsed time [msec]"
    plot.yaxis.axis_label = "tid [-]"
    plot.x_range = bokeh.models.Range1d(
        start=float(df['time'].min()), end=float(df['time'].max())
    )
    plot.y_range = bokeh.models.Range1d(
        start=int(df['tid'].min()), end=int(df['tid'].max())
    )

    x = np.linspace(0, len(df.index), len(df.index))

    colors = [colormap[x] for x in df['state']]
    legends = [legendmap[x] for x in df['state']]
    source = bokeh.models.ColumnDataSource(dict(
        x=df['time'],
        y=df['tid'],
        color=colors,
        label=legends,
    ))

    # NOTE: this code must be before plot.rect() and so on
    plot.add_layout(bokeh.models.Legend(), 'above')
    plot.legend.orientation = "horizontal"

    # rect version (no auto range)
    plot.rect(
        x='x',
        y='y',
        width=1000,
        height=1,
        color='color',
        legend_field='label',
        source=source)

    # circle version (auto range)
    # plot.circle(
    # x='x',
    # y='y',
    # size=4,
    # color='color',
    # legend_field='label',
    # source=source)


# TODO: add text which shows count values
def process_countup(plot, filepath):
    # NOTE: header=0 means use first line as header
    df = pd.read_csv(filepath, header=0, delim_whitespace=True, comment='#')

    n_data_header = len(df.columns)
    if n_data_header != 9:
        print('Syntax error: data length is {}'.format(n_data_header))
        sys.exit(1)

    # NOTE: for debug
    print(df)

    plot.xaxis.axis_label = "count [-]"
    plot.yaxis.axis_label = "tid [-]"
    # NOTE: get total value of first line
    plot.x_range = bokeh.models.Range1d(
        start=0, end=int(df[1:1 + 1].drop(columns='TID').sum(axis=1)),
    )

    stackers = df.columns[1:]
    colors = [colormap[x] for x in stackers]
    legends = [legendmap[x] for x in stackers]
    source = bokeh.models.ColumnDataSource(dict(
        TID=df['TID'],
        D=df['D'],
        R=df['R'],
        S=df['S'],
        T=df['T'],
        t=df['t'],
        W=df['W'],
        X=df['X'],
        Z=df['Z'],
        DUMMY=df['Z'],
    ))
    # source = bokeh.models.ColumnDataSource(df)

    # NOTE: this code must be before plot.hbar_stack() and so on
    plot.add_layout(bokeh.models.Legend(), 'below')

    # WARN: dummy legend is workaround for zero length elements
    plot.hbar_stack(stackers=list(stackers) + ['DUMMY'],
                    y='TID',
                    height=1.0,
                    color=colors + ['white'],
                    source=source,
                    legend_label=legends + [''])


if args.type == "time-series":
    process_time_series(plot, filepath)
elif args.type == "countup":
    process_countup(plot, filepath)
else:
    parser.print_help()
    sys.exit(1)

filepath_svg = filepath + '.svg'
plot.output_backend = "svg"
print('[svg output]', filepath_svg)
bokeh.io.export_svgs(plot, filename=filepath_svg)
