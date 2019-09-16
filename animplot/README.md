# animplot

## how to run
```
bokeh serve --show animplot.py --args --xmax 384 --ymax 256 --fps 2 --loop ./data.csv
```

## TODO
* csvから読み込む機能を追加
* gif保存機能の追加

## FMI
### ColumnDataSource
* shape毎にsourceを作成し，source.dataの値を変更することでanimationが可能
  * keyはfigureにshapeを登録する際に定義するkeyと一致させる必要がある
  * WARN: BokehUserWarning: ColumnDataSource's columns must be of the same length.
* 新規データを利用したい場合
  * 基本的に，データサイズは変更させないが，`stream`を利用することで，変更可能
  * [Providing Data for Plots and Tables — Bokeh 1\.3\.4 documentation]( https://bokeh.pydata.org/en/latest/docs/user_guide/data.html#streaming )
