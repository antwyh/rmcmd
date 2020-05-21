## 1 RMCMD-远程控制、登录、传输便携终端管理器

单机跑一个程序 、部署一个程序都是非常简答的工作，可是当你的代码需要在足够多的目标机运行的时候，痛点就来了，他们有可能是：

* 目标机太多，无法不通过软件借助每一个ip地址；
* 需要将环境部署到多个主机，而有些更有可能在docker容器内；
* 希望有时通过一个命令就能很简单的远程执行一个主机甚至执行一堆主机的命令，并且不需要每次都要输入令人厌恶的IP地址或者密码；

remote-cotroll便是我对于自己日常工作中遇到的这个问题的一个解答，我希望通过简单的yaml配置，就再也不需要输入ip地址或者密码就能方便的在一个shell终端执行之前非常痛苦的多机部署、日志拷贝、日志分析、远程状态查看等问题。

> 目标只有一个，最简单的代码实现，以及最少的配置，实现一机安装，多处控制。
>

远程控制指令演示:
```shell script
rmc cmd --index=7 --value="docker exec -i 8bd4dd7ef18a /bin/bash -c 'cd /root/simulator/python;pwd;./func-simu-client.py list-id'"
```


>
>
>
>
>
>