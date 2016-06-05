#!/usr/bin/env bash

set -e

ITER=5

function parse_java_gc_times {
    grep -o -E '\d+[,.]\d+ secs]$' $1 | tr ',' '.' | grep -o -E '[0-9.]+'| sort -n | awk -f calc.awk
}

> java.log
> javag1.log

for i in `seq 1 ${ITER}`
do
    java -verbosegc -cp . Main >> java.log
    java -XX:+UseG1GC -verbosegc -cp . Main >> javag1.log
done

echo Java default
parse_java_gc_times java.log

echo Java G1
parse_java_gc_times javag1.log
