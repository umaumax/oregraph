# vmstat visualizer

## how to use
### get data
```
vmstat 1 > vmstat.log
```

### how to convert log to svg
```
./vmstat.py vmstat.log
# output: vmstat.log.svg

cat vmstat.log | ./vmstat.py -
# output: vmstat.svg

cat vmstat.log | ./vmstat.py /dev/stdin
# output: vmstat.svg
```

## NOTE
* only for CPU usage

## FYI
* [joewalnes/web\-vmstats: Prettify vmstats in your browser]( https://github.com/joewalnes/web-vmstats )

* [jsargiot/vmstatly: Creates charts from vmstat output\.]( https://github.com/jsargiot/vmstatly )

```
git clone https://github.com/jsargiot/vmstatly.git
cd vmstatly
python3 -m http.server 12345
# then drag and drop file!
# you can easily delete header or footer (by removing `index.html` codes)
```

## INFO
```
r: How many processes are waiting for CPU time.
b: Wait Queue - Process which are waiting for I/O (disk, network, user input,etc..)
free: Idle Memory
buff: Memory used as buffers, like before/after I/O operations
cache: Memory used as cache by the Operating System
(Ignored)swpd: shows how many blocks are swapped out to disk (paged). Total Virtual memory usage.
si: How many blocks per second the operating system is swapping in. i.e Memory swapped in from the disk (Read from swap area to Memory)
so: How many blocks per second the operating system is swaped Out. i.e Memory swapped to the disk (Written to swap area and cleared from Memory)
bi: Blocks received from block device - Read (like a hard disk)
bo: Blocks sent to a block device - Write
in: The number of interrupts per second, including the clock.
cs: The number of context switches per second.
us: percentage of cpu used for running non-kernel code. (user time, including nice time)
sy: percentage of cpu used for running kernel code. (system time - network, IO interrupts, etc)
id: cpu idle time in percentage.
wa: percentage of time spent by cpu for waiting to IO.
```
