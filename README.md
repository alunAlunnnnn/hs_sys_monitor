版本信息：

​        当前版本为 v0.1，在 win 10 19042、winserver 2019 中测试可用。并且 linux_py36 分支提供对 linux 的支持，因为适配环境为 centos7.9 的 py36 所以在性能上略有下降

​        目前仅支持写入 sqlite 数据库，后续会添加对 mysql、pgsql 的支持

​        当前的 linux 适配版仅为过渡使用，后续会基于 python 3.9 及 python 3.9 devel 进行完整性能版的适配

​        目前仅收集 CPU、RAM、DISK I/O 的信息，后续补充网络 I/O





注意事项：

1、受限于硬盘和cpu使用率计算逻辑的影响，最小的收集间隔为 3 秒，小于 3  秒的设置不会报错，但是无法生效

2、每次收集的数据插入 sqlite 后会占大约 1.5kb 的空间，所以当长时间监控，并且收集间隔很短的时候，一定要注意空间占用的问题





使用方法：

1、初始化 sqlite 数据库

> hs_system_monitor.exe init -d D:\systemonitor\example.db



2、单次收集数据

>hs_system_monitor.exe run -d D:/systemonitor/example.db.db



3、持续收集数据（默认间隔30秒）

> hs_system_monitor.exe run -d D:/systemonitor/example.db.db -l



4、持续收集数据（自定义间隔 此处为10秒）

> hs_system_monitor.exe run -d D:/systemonitor/example.db.db -l -s 10





源码打包：

>pyinstaller -F --distpath ./release --workpath ./release/build -i img\hispatial.ico -n hs_system_monitor sys_monitor_cli.py