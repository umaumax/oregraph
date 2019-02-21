# pidstat visualizer

## how to use
```
pidstat -p $(pgrep htop | head -n 1) 1 > pidstat.log
```

```
./pidstat.py pidstat.log
```
