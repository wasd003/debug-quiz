#!/bin/bash

# 添加针对malloc的tracepoint
sudo perf probe -x /lib/x86_64-linux-gnu/libc.so.6 malloc

# trace这个新添加的tracepoint
sudo perf record -e probe_libc:malloc -F 100 -a -g --call-graph dwarf
