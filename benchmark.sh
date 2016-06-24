#!/usr/bin/env bash

set -e

ITER=5

function parse_java_gc_times {
    grep -o -E '\d+[,.]\d+ secs]$' $1 | tr ',' '.' | grep -o -E '[0-9.]+'| awk '{print $1*1000}' | sort -n | awk -f calc.awk
}

function parse_v8_gc_times {
    grep -o -E ', \d+\.\d+ / 0 ms' $1 | grep -o -E '\d+\.\d+' | sort -n | awk -f calc.awk
}

> java.log
> javag1.log
> js.log
> js-immutable.log

for i in `seq 1 ${ITER}`
do
    java -verbosegc -cp . Main >> java.log
    java -XX:+UseG1GC -verbosegc -cp . Main >> javag1.log
    node --trace-gc main.js >> js.log
    node --trace-gc main-immutable.js >> js-immutable.log
done

echo Java default
parse_java_gc_times java.log

echo Java G1
parse_java_gc_times javag1.log

echo Node
parse_v8_gc_times js.log

echo Node Immutable
parse_v8_gc_times js-immutable.log
