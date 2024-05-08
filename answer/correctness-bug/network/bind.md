## 解答
- 使用ftrace查看`__sys_bind`的调用路径，发现是`inet_csk_get_port`这个函数导致的报错
- 代码中有如下判断：
```
	if (!found_port) {
		if (!hlist_empty(&tb->owners)) {
			if (sk->sk_reuse == SK_FORCE_REUSE ||
			    (tb->fastreuse > 0 && reuse) ||
			    sk_reuseport_match(tb, sk))
				check_bind_conflict = false;
		}

		if (check_bind_conflict && inet_use_bhash2_on_bind(sk)) {
			if (inet_bhash2_addr_any_conflict(sk, port, l3mdev, true, true))
				goto fail_unlock;
		}

		head2 = inet_bhashfn_portaddr(hinfo, sk, net, port);
		spin_lock(&head2->lock);
		head2_lock_acquired = true;
		tb2 = inet_bind2_bucket_find(head2, net, port, l3mdev, sk);
	}
```
其中比较关键的是当`found_port`为false的时候，`sk->sk_reuse == SK_FORCE_REUSE`判断预期应该成立，从而使得`check_bind_conflict`变为false（如果是true后面会判断失败)
研究了一下这个REUSE发现bind之前应该提前为socketfd设置端口复用。一般来说，一个端口释放后会等待两分钟之后才能再被使用，`SO_REUSEADDR | SO_REUSEPORT`是让地址:端口释放后立即就可以被再次使用。
