# threads

## how to setup
```
pip install pandas bokeh selenium geckodriver-autoinstaller
```
[PythonでWebDriverのインストールを自動化したり補助するモジュールまとめ \- Qiita]( https://qiita.com/QutaPase/items/f895e7f1ba887fa52ce1 )

[Installation — Bokeh 2\.1\.1 Documentation]( https://docs.bokeh.org/en/latest/docs/installation.html )

> Selenium, GeckoDriver, Firefox
> Necessary for Exporting Plots to PNG and SVG images.

## how to get data
```
while true; do sleep 1.0; bash -c "clear; { date +%s%3N; ps -FLl -p $PID | awk 'NR>1 {print \$6, \$2}'; }  | tee -a ps.log"; done
```

## how to use
```
./threads-viz.py plot.data
```

## data

e.g. ps.log
```
100
1 R
2 R
3 D
101
1 R
2 D
3 D
102
1 S
2 S
3 R
```

```
cat ps.log | awk 'NF==1{t=$1;} NF==2{print t,$1,$2}' > plot.data
```

e.g. plot.data
```
100 1 R
100 2 R
100 3 D
101 1 R
101 2 D
101 3 D
102 1 S
102 2 S
102 3 R
```
