# Passets

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![Ruby 2.5](https://img.shields.io/badge/ruby-2.5-red.svg)](https://www.ruby-lang.org/) [![Nodejs 8.x](https://img.shields.io/badge/nodejs-8.x-green.svg)](https://www.ruby-lang.org/) [![Java 1.8](https://img.shields.io/badge/java-1.8-red.svg)](https://www.java.com/) [![Platform linux&docker](https://img.shields.io/badge/platform-linux&docker-9cf.svg)](https://www.java.com/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/knownsec/Pocsuite/master/docs/COPYING)


## 概述

Passets 是一套由 DSO 安全实验室（DSO Security Lab）开源的被动资产识别框架，用于基于被动流量的网络资产发掘。整体框架包括四大组件：

**[passets-sensor](https://github.com/DSO-Lab/passets-sensor)**
> 网络流量采集模块：提供流量采集及基本的流量过滤和处理。

**[passets-logstash](https://github.com/DSO-Lab/passets-logstash)**
> 数据清洗模块：根据数据清洗插件对数据进行深度清洗、标记和重组。

**ElasticSearch**
> 数据存储模块：负责数据的存储、检索、汇聚等。

**[passets-api](https://github.com/DSO-Lab/passets-api)**
> 外部接口模块：负责根据业务需求提供所需的数据。


## 特性
* 从采集到数据清洗全部支持分布式架构
* 数据清晰插件可定制
* 支持多种硬件环境（x86、ARM）
* 容器化部署，操作简单
* 更多 ...


## 环境

### 软件
- Linux
- [Docker](https://www.docker.com/)
- [docker-compose](https://github.com/docker/compose)

### 硬件

用户需要自行准备一台至少包含两块网卡的计算机设备。其中一个网卡用来接收交换机镜像的流量，另一个网卡则用于通过Web API向其它应用提供数据。

用户提供的计算机设备最小配置要求如下：

| 参数项 | 最小配置 | 推荐配置 |
|------|----------|----------|
| CPU  | 无     | 四核     |
| 内存 | 8G     | 16G      |
| 存储 | 40G    | 1T       |


## 安装方法

快速部署方法：

**第一步**：点击 [这里](https://github.com/DSO-Lab/passets/archive/master.zip) 下载最新的部署文件包并解压缩：

```bash
$ curl https://github.com/DSO-Lab/passets/archive/master.zip -o master.zip
$ unzip master.zip
```

**第二步**：根据所的软/硬件平台修改对应 [`docker-compose`](#directory) 配置文件中下列参数中的监听网口编号：

```
services.sensor.environment
- interface=<网卡编号>
```

**第三步**：下载最新的指纹库

``` bash
$ curl -L https://github.com/AliasIO/Wappalyzer/raw/master/src/apps.json -o ./rules/apps.json
```

**第四步**：数据目录赋权

``` bash
$ chmod -R 777 ./data
```

**第五步**：启动应用:

``` bash
$ docker-compose up -d
```

启动后等待一段时间，则可以通过下面的地址访问 API 接口：

http://127.0.0.1:8081/

或者通过下面的地址访问原始数据：

http://127.0.0.1:5601/


## 帮助文档

帮助文档位于 [```docs```](./docs) 目录.


## 目录结构<div id="directory"></div>

```
├─ docker-compose.yml        # 适用于 X86_64 平台的 docker-compose 配置文件
├─ docker-compose_armv7.yml  # 适用于 ARMv7 平台的 docker-compose 配置文件
├─ rules                     # 指纹库文件夹
│  └─ apps.json              # 从 Wappalyzer 开源项目下获取 指纹库文件,默认为空文件，上线需要用最新的文件替换
└─data                       # 容器数据目录
   ├─ elasticsearch          # ES 数据目录
   ├─ logstash               # Logstash 数据目录
   ├─ kibana                 # Kibana 数据目录
   └─ logs                   # E.L.K 日志目录
```

## 链接

* [修改日志](./CHANGELOG.md)
* [缺陷跟踪](https://github.com/DSO-Lab/passets/issues)
* [软件授权](./LICENSE)
