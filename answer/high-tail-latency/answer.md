## 题目描述
一个naive的方法是对第10000个请求的处理流程手动breakdown，测量程序每一部分的时间，但是这样很麻烦。目前想到了两种方法来debug这个问题。
事实上测量程序耗时最常用的工具就是perf，但是因为我们只关心第10000个请求，直接使用perf无法细粒度的trace这个具体的请求的时间分布。

### 法一
google-perftools可以通过代码开关：
```
if (cnt ++ == 10000) ProfilerStart("pprof.data");
handle_request()
if (cnt == 10000) ProfilerEnd();
```

### 法二
我们把原始的server进程称作被监测进程，那么可以另起一个进程用来trace server。
两个进程之间用任意方式（比如fifo）通信，当counter到达10000的时候，被监测进程通知监测进程执行事先写好的脚本
具体做法详见：`https://gitee.com/wasd003/dotfile/tree/master/perf/conditional_perf`
