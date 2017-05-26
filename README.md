# 备份工具

功能

* 备份指定文件到指定目录
* 清理过期备份数据

需要配合[计划任务](http://codingpub.github.io/2016/10/27/OS-X-%E6%B7%BB%E5%8A%A0%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1/)使用，目前只支持 Linux/Mac 系统。

*（Windows 系统应该可以通过安装 rsync 支持）*


需要创建配置文件，可以配置多个备份项：

```
<!-- config.json -->

[{
    "src": "src_file_or_dir_path",
    "dst_dir": "dst_dir_path",
    "retemtion_days": [10, 7, 3, 2, 1],
    "hours_last_day": 8
}]
```
