这道题其实来源于上一道题，当时在写进程间fifo通信的时候发现启动一个进程，open fifo文件会卡死。
因为是syscall hang住，自然希望看到这个syscall内部函数调用，ftrace就是一个很好的选择。
利用ftrace可以看函数下游分布的特性，直接trace `do_sys_openat2` 这个函数，得到log。可以看到是在`wait_for_partner()`中主动调了`schedule()`，所以syscall没能返回。
查看kernel代码发现`wait_for_partner()`需要等待peer拿锁，所以需要通信双方都open才能够结束阻塞。而我在测试的时候只启动了一个进程，所以才有这个问题。
