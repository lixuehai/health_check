## 监控脚本说明
- check.py

定义要监控的主机，并且监控中间件服务

- ops.py

监控openstack服务

- os_system.py

监控服务器的cpu、mem等


## 运行监控脚本
将三个脚本放到一个文件夹下，执行check.py

```
python check.py

脚本返回health.txt 文件

```