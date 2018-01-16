#!/usr/bin/env python3

from subprocess import check_output, STDOUT
from time import time
from random import shuffle
import matplotlib.pyplot as plt
import re

results = {}
iterations = 5


def benchmark(name, args, output_parser):
    start = time()
    output = check_output(args, universal_newlines=True, stderr=STDOUT)
    end = time()
    r = output_parser(output)
    if name not in results:
        results[name] = {"gc_times": [], "clock_times": []}
    results[name]["gc_times"].extend(r)
    results[name]["clock_times"].append(end - start)


def parse_java8_gc_output(output):
    times = []
    for line in output.split("\n"):
        if not line:
            continue
        if line.startswith("[GC concurrent"):
            continue
        m = re.search(r"(\d+[,.]\d+) secs]$", line)
        if not m:
            print("No match from line:", line)
            continue
        times.append(float(m.group(1).replace(",", ".")) * 1000)
    return times


def parse_java9_gc_output(output):
    times = []
    for line in output.split("\n"):
        if not line:
            continue
        m = re.search(r"GC\(\d+\) Pause.*?(\d+\.\d+)ms$", line.strip())
        if not m:
            if "[gc]" in line: continue
            print("No match from line:", line)
            continue
        times.append(float(m.group(1)))
    return times


def parse_v8_gc_output(output):
    times = []
    for line in output.split("\n"):
        if not line:
            continue
        m = re.search(r", (\d+\.\d+) / 0.0 ms", line)
        if not m:
            print("No match from line:", line)
            continue
        times.append(float(m.group(1)))
    return times


def parse_ghc_gc_output(output):
    times = []
    for line in output.split("\n"):
        if not line:
            continue
        try:
            elems = line.split()
            float(elems[0])
            float(elems[1])
            m = elems[4]
            pause_time = float(m)
        except (IndexError, ValueError):
            print("No match from line:", line)
            continue
        if pause_time == 0:
            continue
        times.append(pause_time * 1000)
    return times


def parse_go_gc_output(output):
    times = []
    for line in output.split("\n"):
        line = line.strip()
        if not line.startswith("gc "):
            print("No match from line:", line)
            continue
        m = re.search(r"([0-9+.]+) ms clock", line)
        if not m:
            print("No match from line:", line)
            continue
        times.append(sum([float(x) for x in m.group(1).split("+")]))
    return times


def benchmark_java():
    benchmark("Java", ["java", "-verbosegc", "-cp", "src/java/", "-Xmx1G", "Main"], parse_java9_gc_output)


def benchmark_java_g1():
    benchmark(
        "Java G1",
        ["java", "-XX:+UseG1GC", "-verbosegc", "-cp", "src/java", "-Xmx1G", "-XX:MaxGCPauseMillis=50", "Main"],
        parse_java_gc_output,
    )


def benchmark_node():
    benchmark("Node", ["node", "--trace-gc", "src/node/main.js"], parse_v8_gc_output)


def benchmark_node_immutable():
    benchmark("Node imm", ["node", "--trace-gc", "src/node/main-immutable.js"], parse_v8_gc_output)


def benchmark_python():
    benchmark("Python 3", ["python3", "src/python/main.py"], lambda x: [])


def benchmark_pypy():
    benchmark("PyPy", ["pypy", "src/python/main.py"], lambda x: [])

def benchmark_swift():
    benchmark("Swift", ["./src/swift/Main"], lambda x: [])

def benchmark_scala():
    benchmark("Scala", ["scala", "-cp", "src/scala", "-J-Xmx1G", "-J-verbosegc", "Main"], parse_java_gc_output)


def benchmark_haskell():
    benchmark("Haskell", ["./src/haskell/Main", "+RTS", "-S"], parse_ghc_gc_output)


def benchmark_go():
    benchmark("Go", ["env", "GODEBUG=gctrace=1", "./src/go/go"], parse_go_gc_output)


def avg(ls):
    return sum(ls) / len(ls)


def median(ls):
    ls = sorted(ls)
    if len(ls) % 2 == 1:
        return ls[len(ls) // 2]
    else:
        return avg([
            ls[len(ls) // 2 - 1],
            ls[len(ls) // 2],
        ])


def calculate_stats(times):
    if not times:
        return None
    fmt = "{0:.1f}"
    return {
        "average": fmt.format(avg(times)),
        "minimum": fmt.format(min(times)),
        "maximum": fmt.format(max(times)),
        "median": fmt.format(median(times)),
        "total": fmt.format(sum(times) / iterations),
        "amount": len(times) / iterations,
    }


if __name__ == "__main__":
    benchmarks = [
        benchmark_java, benchmark_node, benchmark_node_immutable, benchmark_python,
        benchmark_scala, benchmark_haskell, benchmark_swift, benchmark_go
    ]
    for i in range(iterations):
        shuffle(benchmarks)
        for b in benchmarks:
            b()
    print("\nRESULTS\n")
    data = []
    labels = []
    for name, res in results.items():
        print(name)
        print("Average clock time:", "{0:.2f}".format(avg(res["clock_times"])), "s")
        print("GC pause times:", calculate_stats(res["gc_times"]))
        print("---")
        if res["gc_times"]:
            data.append(res["gc_times"])
            labels.append(name)
    plt.boxplot(data, labels=labels, showmeans=True)
    plt.show()
