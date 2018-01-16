# GC latency experiment

[My blog post](https://blog.hilzu.moe/2016/06/26/studying-gc-latencies/) about the results.
[Original blog post](http://prl.ccs.neu.edu/blog/2016/05/24/measuring-gc-latencies-in-haskell-ocaml-racket/)
that has the original experiment and code.

Since writing the blog post I've run the benchmark with newer versions of languages
and added a Go benchmark.

## Run benchmarks

```
./build-all.sh
pip install -r requirements.txt
python benchmark.py
```

## Results (milliseconds)

All tests run with MacBook Pro (Retina, 15-inch, Late 2013) and macOS 10.12.6.

|                             |  Java |  Scala |   Node | Node Imm | Haskell |    Go | Python | Swift |
| --------------------------- | ----: | -----: | -----: | -------: | ------: | ----: | -----: | ----: |
| **Version**                 | 9.0.1 | 2.12.4 |  9.4.0 |    9.4.0 |   8.0.2 | 1.9.2 |  3.6.4 | 4.0.3 |
| **Min**                     |   0.4 |    0.1 |    0.8 |      0.5 |     1.0 |   0.2 |        |       |
| **Median**                  |  16.4 |    2.9 |   35.1 |      5.7 |    24.0 |   3.8 |        |       |
| **Average**                 |  15.8 |    5.8 |   31.4 |      6.1 |    21.7 |   6.4 |        |       |
| **Max**                     |  47.5 |   33.9 |  128.8 |     22.7 |    64.0 |  26.0 |        |       |
| **Avg total pause per run** | 380.0 |  388.0 | 1006.2 |   1271.1 |   247.2 |  64.3 |        |       |
| **Avg pauses per run**      |    24 |   66.6 |     32 |      207 |    11.4 |    10 |        |       |
| **Avg run time (s)**        |  1.11 |   6.06 |   2.87 |     5.41 |    1.35 |  1.43 |   16.3 |  8.25 |

### Box plot of results

![Box plot](gc-latencies.svg)

### Box plot zoomed in without extreme outliers

![Box plot zoomed in](gc-latencies-zoomed-in.svg)
