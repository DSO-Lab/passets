## ![](docs/images/logo.png)

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![Ruby 2.5](https://img.shields.io/badge/ruby-2.5-red.svg)](https://www.ruby-lang.org/) [![Nodejs 8.x](https://img.shields.io/badge/nodejs-8.x-green.svg)](https://www.ruby-lang.org/) [![Java 1.8](https://img.shields.io/badge/java-1.8-red.svg)](https://www.java.com/) [![Platform linux&docker](https://img.shields.io/badge/platform-linux&docker-9cf.svg)](https://www.java.com/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/knownsec/Pocsuite/master/docs/COPYING)


## 概述

passets 是一套由 [DSO 安全实验室（DSO Security Lab）](http://www.dsolab.org)开源的被动资产识别框架，用于基于被动流量的网络资产发现。整体框架包括四大组件：

**[流量采集模块](https://github.com/DSO-Lab/passets-sensor)**
> 提供流量采集及基本的流量过滤和处理。

**数据存储模块（ELK）**
> 采用成熟的 Elasticsearch + Logstash + Kibana 框架， 负责采集数据的基本加工、存储及索引等。

**[数据清洗模块](https://github.com/DSO-Lab/passets-filter)**
> 根据数据清洗插件对数据进行深度清洗、标记和重组。

**[数据发布模块](https://github.com/DSO-Lab/passets-api)**
> 负责向第三方应用提供采集的资产数据。


## 特性
* 从采集到数据清洗全部支持分布式架构
* 数据清洗插件可自行定制
* 支持多种硬件环境（x86、ARM）
* 容器化部署，操作简单
* 更多...


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
| CPU  | 四核   | 八核    |
| 内存 | 8G     | 16G      |
| 存储 | 100G  | 1T       |


## 部署方法

依赖环境安装：

```bash
$ curl -fsSL https://get.docker.com/ | sh
$ yum -y install docker-compose
$ systemctl start docker
$ systemctl enable docker
```

### 单机快速部署

**第一步**：点击 [这里](https://github.com/DSO-Lab/passets/archive/master.tar.gz) 下载最新的部署文件包并解压缩：

```bash
$ curl -L https://github.com/DSO-Lab/passets/archive/master.tar.gz -o master.tar.gz
$ tar -zxf master.tar.gz
$ cd passets-master/
```

**第二步**：根据所需的软/硬件平台修改对应 [`docker-compose`](#directory) 配置文件中下列参数：

```
services：
    ...
    sensor：
        ...
        environment：
        # 流量镜像网卡配置
        - interface=<网卡编号>
        # 是否开启详细http数据分析（包含：Http Body、Http Header、详细应用指纹识别等）
        - switch=on
```

**第三步**：获取最新的指纹库、IP定位数据库

``` bash
# Wappalyzer 指纹库
$ curl -L https://github.com/AliasIO/Wappalyzer/raw/master/src/apps.json -o ./rules/apps.json

# NMAP 指纹库
$ curl -L https://github.com/nmap/nmap/raw/master/nmap-service-probes -o ./rules/nmap-service-probes

# GeoLite2 IP定位库
$ curl -L https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -o GeoLite2-City.tar.gz
$ tar -C ./rules/ --strip-components=1 -zxf GeoLite2-City.tar.gz
$ rm -f GeoLite2-City.tar.gz
```

**第四步**：定义自己的内部IP地址

内部IP地址默认已配置为通用局域网IP地址，用户可以通过修改 `docker-compose.yml` 中 Logstash 容器的 `INNER_IP_LIST` 环境变量来自定义内部 IP 地址列表。格式为“<起始IP>-<结束IP>,IP”（单条记录支持IP范围和单个IP，多条记录用半角逗号分隔，不能有空格），默认配置如下：

```
version: "3"

services:
  ... ...
  
  logstash:
    ... ...
    environment:
      ... ...
      - INNER_IP_LIST=10.0.0.0-10.255.255.255,172.16.0.0-172.31.255.255,192.168.0.0-192.168.255.255,169.254.0.0-169.254.255.255,127.0.0.1-127.0.0.255
```

**第五步**：数据目录赋权

``` bash
$ chmod -R 777 ./data
$ chmod -R 777 ./rules
```

**第六步**：启动应用

``` bash
$ docker-compose up -d
```

启动后等待一段时间，则可以通过下面的地址访问 API 接口：

http://x.x.x.x:8081/swagger-ui.html#/

或者通过集成的 Kibana 进行可视化查询或展示（[Kibana 配置方法示例](docs/KIBANA_HELP.md)）：

http://x.x.x.x:5601/

### 集群部署

待完善。

## 帮助文档

详细配置说明参见 [```docs```](./docs) 目录中的文档。


## 目录结构<div id="directory"></div>

```
├─ docker-compose.yml        # docker-compose 配置文件（X86_64）
├─ docker-compose_armv7.yml  # docker-compose 配置文件（ARMv7）
├─ config                    # 配置文件
│  ├─ kibana.ndjson          # Kibana 配置文件
│  └─ plugin.yml             # 数据清洗模块配置文件
├─ docs                      # 文档
│  └─ ... ...
├─ plugins                   # 数据清洗插件
│  └─ ... ...
├─ rules                     # 指纹库
│  ├─ apps.json              # Wappalyzer 开源Web指纹库
│  ├─ GeoLite2-City.mmdb     # GEOIP2 IP 定位数据库
│  ├─ nmap-service-probes    # NMAP 指纹库
│  └─ nmap.json              # 解析后的 NMAP 指纹库，自动生成
├─ logstash                  # Logstash 相关配置文件
│  ├─ ip.rb                  # 识别内外网IP的过滤插件
│  ├─ url.rb                 # 识别站点、路径及URL模板的过滤插件
│  ├─ logstash.yml
│  ├─ logstash.conf
│  └─ log4j2.properties
└─data                       # 容器数据
   ├─ elasticsearch          # Elasticsearch 数据
   ├─ logstash               # Logstash 数据
   ├─ kibana                 # Kibana 数据
   └─ logs                   # E.L.K 日志
```

## 链接

* [修改日志](./CHANGELOG.md)
* [缺陷跟踪](https://github.com/DSO-Lab/passets/issues)
* [软件授权](./LICENSE)
