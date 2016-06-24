from __future__ import division, print_function
from subprocess import check_output
from time import time
from random import shuffle
import re

results = {}
iterations = 5


def benchmark(name, args, output_parser):
    start = time()
    output = check_output(args, universal_newlines=True)
    end = time()
    r = output_parser(output)
    if name not in results:
        results[name] = {"gc_times": [], "clock_times": []}
    results[name]["gc_times"].extend(r)
    results[name]["clock_times"].append(end - start)


def parse_java_gc_output(output):
    times = []
    for line in output.split("\n"):
        if not line:
            continue
        m = re.search(r"(\d+[,.]\d+) secs]$", line)
        if not m:
            print("No match from line:", line)
            continue
        times.append(float(m.group(1).replace(",", ".")) * 1000)
    return times


def parse_v8_gc_output(output):
    times = []
    for line in output.split("\n"):
        if not line:
            continue
        m = re.search(r", (\d+\.\d+) / 0 ms", line)
        if not m:
            print("No match from line:", line)
            continue
        times.append(float(m.group(1)))
    return times


def benchmark_java():
    benchmark("Java", ["java", "-verbosegc", "-cp", "src/java/", "-Xmx4G", "Main"], parse_java_gc_output)


def benchmark_java_g1():
    benchmark("Java G1", ["java", "-XX:+UseG1GC", "-verbosegc", "-cp", "src/java", "-Xmx4G", "Main"], parse_java_gc_output)


def benchmark_node():
    benchmark("Node.js", ["node", "--trace-gc", "src/node/main.js"], parse_v8_gc_output)


def benchmark_node_immutable():
    benchmark("Node.js immutable", ["node", "--trace-gc", "src/node/main-immutable.js"], parse_v8_gc_output)


def benchmark_python():
    benchmark("Python", ["python", "src/python/main.py"], lambda x: [])


def benchmark_pypy():
    benchmark("PyPy", ["pypy", "src/python/main.py"], lambda x: [])


def benchmark_scala():
    benchmark("Scala", ["scala", "-cp", "src/scala", "-J-Xmx4G", "-J-verbosegc", "Main"], parse_java_gc_output)


def avg(ls):
    return sum(ls) / len(ls)


def median(ls):
    ls = sorted(ls)
    if len(ls) % 2 == 1:
        return ls[len(ls) // 2]
    else:
        return avg([len(ls) // 2 - 1, len(ls) // 2])


def calculate_stats(times):
    fmt = "{0:.1f}"
    return {
        "average": fmt.format(avg(times)),
        "minimum": fmt.format(min(times)),
        "maximum": fmt.format(max(times)),
        "median": fmt.format(median(times)),
        "total": fmt.format(sum(times)),
    }


if __name__ == "__main__":
    benchmarks = [
        benchmark_java, benchmark_java_g1, benchmark_node, benchmark_node_immutable, benchmark_python, benchmark_pypy,
        benchmark_scala,
    ]
    for i in range(iterations):
        shuffle(benchmarks)
        for b in benchmarks:
            b()
    print("Results")
    for name, res in results.items():
        print(name)
        print("average clock time:", avg(res["clock_times"]))
        print("GC pause times")
        print(calculate_stats(res["gc_times"]))
        print("---")
