# Linux 命令

1、nohup
nohup python3 -u command > record.txt 2>&1 &
-u 实时将程序中的print写入文件

2、

文件和目录

cd /home  :进入/home目录
pwd :显示工作路径
ls :显示目录中的文件
ls -F :显示目录中的文件
ls -l:显示文件和目录的详细信息
ls -a:显示隐藏文件

磁盘空间

df -h 显示已经挂载的分区列表

3、Crontab
4、Linux下四款Web服务器压力测试工具（http_load、webbench、ab、siege）
5、supervisord.conf:进程守护，能自动重启进程
 tail :命令从指定点开始将文件写到标准输出.使用tail命令的-f选项可以方便的查阅正在改变的日志文件,tail -f filename会把filename里最尾部的内容显示在屏幕上,并且不但刷新,使你看到最新的文件内容.