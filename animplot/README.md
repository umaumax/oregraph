# animplot

## how to run
```
bokeh serve --show animplot.py --args --xmax 384 --ymax 256 --fps 2 --loop ./data.csv
```

## how to gen gif
```
convert -fuzz 10% -delay 1x8 *.png animation.gif
```

## TODO
* csvから読み込む機能を追加
* gif保存機能の追加

## FMI
* [（続き）Bokeh をつかって行列演算を可視化する\(with animation\) \- Qiita]( https://qiita.com/SatoshiTerasaki/items/b7a5bf61f572aac1e358 )
### ColumnDataSource
* shape毎にsourceを作成し，source.dataの値を変更することでanimationが可能
  * keyはfigureにshapeを登録する際に定義するkeyと一致させる必要がある
  * WARN: BokehUserWarning: ColumnDataSource's columns must be of the same length.
* 新規データを利用したい場合
  * 基本的に，データサイズは変更させないが，`stream`を利用することで，変更可能
  * [Providing Data for Plots and Tables — Bokeh 1\.3\.4 documentation]( https://bokeh.pydata.org/en/latest/docs/user_guide/data.html#streaming )
