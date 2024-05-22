## 题目描述
本题出自于CMU 10-414/714: Deep Learning Systems的Lab2

在使用needle训练mlp_resnet的时候发生了内存泄漏，现象是进程的内存用量显著上升，
训练只能完成一个epoch就会oom
