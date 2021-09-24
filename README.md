注意事项：

1、受限于硬盘和cpu使用率计算逻辑的影响，最小的收集间隔为 3 秒，小于 3  秒的设置不会报错，但是无法生效





使用方法：

1、初始化 sqlite 数据库

> hs_system_monitor.exe init -d D:\systemonitor\example.db



2、单次收集数据

>hs_system_monitor.exe run -d D:/systemonitor.db



3、持续收集数据（默认间隔30秒）

> hs_system_monitor.exe run -d D:/systemonitor.db -l



4、持续收集数据（自定义间隔 此处为10秒）

> hs_system_monitor.exe run -d D:/systemonitor.db -l -s 10





源码打包：

>pyinstaller -F --distpath ./release --workpath ./release/build -i img\hispatial.ico -n hs_system_monitor sys_monitor_cli.py