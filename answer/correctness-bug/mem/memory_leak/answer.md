## 参考解答
可以使用`gdb-helper.py`，自动收集每次malloc和free的情况。
最后使用`dump`命令看未释放内存所属调用链
