#!/usr/bin/env python3

import numpy as np

import bokeh
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import gridplot, column

import pandas


def rot_mat(degree):
    theta = np.deg2rad(degree)
    mat = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])
    return mat


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=float, default=60.0)
    parser.add_argument('--xmin', type=int, default=0)
    parser.add_argument('--xmax', type=int, default=128)
    parser.add_argument('--ymin', type=int, default=0)
    parser.add_argument('--ymax', type=int, default=128)
    parser.add_argument('--xflipped', action='store_true', help='flip(reverse) x axis or not')
    parser.add_argument('--yflipped', action='store_true', help='flip(reverse) y axis or not (for image coordinate)')
    parser.add_argument('--start', type=int, default=0, help='start with 0~')
    parser.add_argument('--step', type=int, default=1)
    parser.add_argument('--end', type=int, default=-1, help='start with -1(no end),0~')
    parser.add_argument('--loop', action='store_true')
    # parser.add_argument('-o', '--output-filepath', default='')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('csv_filepath')
    parser.add_argument('args', nargs='*')  # any length of args is ok

    args, extra_args = parser.parse_known_args()

    TOOLS = "pan,lasso_select,save,reset"

    df = pandas.read_csv(args.csv_filepath, comment='#')
    rect_data = {}
    # keys=df.columns
    for row in range(len(df.index)):
        shape = df["shape"][row]
        x = df["x"][row]
        y = df["y"][row]
        w = df["w"][row]
        h = df["h"][row]
        data = {}
        if shape == "rect":
            data = {
                'rect_x': x - (w - 1) / 2, 'rect_y': y - (h - 1) / 2,
                'rect_width': w, 'rect_height': h,
            }
        elif shape == "center_rect":
            data = {
                'rect_x': x, 'rect_y': y,
                'rect_width': w, 'rect_height': h,
            }
        else:
            print("unknown shape", shape)
            return 1
        for key in data.keys():
            if key not in rect_data:
                rect_data[key] = []
            rect_data[key].insert(0, data[key])

    if args.verbose:
        print(rect_data)

    rect_n = len(rect_data["rect_x"])
    rect_source = ColumnDataSource(data=dict(
        rect_x=[], rect_y=[], rect_width=[], rect_height=[]
    ))

    f = figure(tools=TOOLS, title="target",
               x_range=(args.xmin, args.xmax),
               y_range=(args.ymin, args.ymax),
               )
    if args.xflipped:
        f.x_range = bokeh.models.Range1d(f.x_range.end, f.x_range.start)
    if args.yflipped:
        f.y_range = bokeh.models.Range1d(f.y_range.end, f.y_range.start)

    f.rect(x='rect_x', y='rect_y', width='rect_width', height='rect_height', source=rect_source, fill_color="red", fill_alpha=0.1)

    start_cnt = args.start
    cnt = args.start
    end_cnt = args.end if args.end >= 0 and args.end < rect_n - 1 else rect_n - 1

    def update():
        nonlocal cnt
        cnt += args.step
        cnt = cnt if cnt < end_cnt else (start_cnt if args.loop else end_cnt)

        rect_data_step = cnt + 1
        rect_data_step = rect_data_step if rect_data_step < rect_n else rect_n
        rect_source.stream(rect_data, rect_data_step)

        f.title.text = "cnt={}".format(cnt)

    grid = gridplot([[f]])
    plot = column(Div(text="<h2>Rect anim plot</h2>"),
                  grid)
    document = curdoc()
    document.add_root(plot)
    period_milliseconds = 1000.0 / args.fps
    document.add_periodic_callback(update, period_milliseconds)


if __name__ == '__main__' or __name__.startswith('bk_script_'):
    main()
