# DolphinDB Tutorial: Moving Averages

## Overview
This tutorial covers how to calculate moving averages in DolphinDB using the `mavg` function.

## Code Sample
See `scripts/dos_samples/moving_average.dos` for the full script.

```dolphindb
t = table(1..10 as id, rand(10.0, 10) as val)
res = select id, val, mavg(val, 3) as ma3 from t
print(res)
```
