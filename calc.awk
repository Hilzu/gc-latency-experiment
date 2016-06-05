#/usr/bin/env awk
{
    total += $1;
    amount++;
    all[NR] = $1;
}
END {
    print "avg:    " total / amount;
    if (NR % 2) {
        print "median: " all[(NR + 1) / 2];
    } else {
        print "median: ", (all[(NR / 2)] + all[(NR / 2) + 1]) / 2.0;
    }
    print "min:   ", all[1];
    print "max:   ", all[amount];
}
