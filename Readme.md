# GC latency experiment

[My blog post](https://blog.hilzu.moe/2016/06/26/studying-gc-latencies/) about the results.
[Original blog post](http://prl.ccs.neu.edu/blog/2016/05/24/measuring-gc-latencies-in-haskell-ocaml-racket/)
that has the original experiment and code.

## Run benchmarks

```
./build-all.sh
pip install -r requirements.txt
python benchmark.py
```

## Results (milliseconds)

|                        | Java  | Java G1 | Scala  | Node   | Node Imm | Haskell
| ---                    | ---:  | ---:    | ---:   | ---:   |     ---: | ---:
| **Min**                |  23.8 |     0.8 |    2.7 |    0.5 |      0.4 |   1.0
| **Median**             |  56.5 |    15.0 |   18.2 |   63.6 |     13.8 |  26.0
| **Average**            |  58.7 |    15.0 |   24.1 |  111.7 |     17.2 |  20.6
| **Max**                | 126.1 |    83.8 |  129.4 |  529.1 |    157.3 |  50.0
| **Avg total pause**    | 704.2 |   380.7 | 1119.3 | 3240.3 |   3574.9 | 235.4
| **Avg pauses**         |    12 |    25.4 |   46.4 |     29 |      208 |  11.4
| **Avg clock time (s)** |   1.2 |     1.0 |    2.6 |    5.2 |      9.3 |   1.3

### Box plot of results

![Box plot](https://blog.hilzu.moe/assets/gc-latencies.svg)

### Box plot zoomed in without extreme outliers

![Box plot zoomed in](https://blog.hilzu.moe/assets/gc-latencies-zoomed-in.svg)
