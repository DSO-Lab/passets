## ![](docs/images/logo.png)

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![Ruby 2.5](https://img.shields.io/badge/ruby-2.5-red.svg)](https://www.ruby-lang.org/) [![Go 1.13.x](https://img.shields.io/badge/go-1.x-green.svg)](https://github.com/golang/go) [![Java 1.8](https://img.shields.io/badge/java-1.8-red.svg)](https://www.java.com/) [![Platform linux&docker](https://img.shields.io/badge/platform-linux&docker-9cf.svg)](https://www.docker.com/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/DSO-Lab/passets/raw/master/LICENSE)


## 概述

passets 是一套由 [DSO 安全实验室（DSO Security Lab）](http://www.dsolab.org)开源的被动资产识别框架，用于基于被动流量的网络资产发现。整体框架包括四大组件：

**[流量采集模块](https://github.com/DSO-Lab/passets-sensor)**
> 提供流量采集及基本的流量过滤和处理。

**数据存储模块（ELK）**
> 采用成熟的 [Elasticsearch](docs/ELASTICSEARCH.md) + [Logstash](https://github.com/DSO-Lab/passets-logstash) + [Kibana](docs/KIBANA.md) 框架， 负责采集数据的基本加工、存储及索引等。

**[数据清洗模块](https://github.com/DSO-Lab/passets-filter)**
> 根据数据清洗插件对数据进行深度清洗、标记和重组。

**[数据发布模块](https://github.com/DSO-Lab/passets-api)**
> 负责向第三方应用提供采集的资产数据。


## 特性

* 从采集到数据清洗全部支持分布式架构
* 居于流量的资产指纹识别
* 支持多种硬件架构（x86、ARM）
* 容器化部署，上手容易
* 更多...


## 环境

### 软件

- Linux
- [Docker](https://www.docker.com/)
- [docker-compose](https://github.com/docker/compose)

### 硬件

用户需要自行准备一台至少包含两块网卡的计算机设备。其中一个网卡用来接收交换机镜像的流量，另一个网卡则用于通过Web API向其它应用提供数据。

用户提供的计算机设备最小配置要求如下（默认保留近30天数据）：

| 参数项 | 百兆网(推荐配置) | 千兆网(推荐配置) |
| ------ | ---------------- | ---------------- |
| CPU    | 四核             | 八核             |
| 内存   | 8G               | 16G              |
| 存储   | 100G             | 500G             |

## 部署

依赖环境安装：

```bash
curl -fsSL https://get.docker.com/ | sh
yum -y install docker-compose
systemctl start docker
systemctl enable docker
```

### 单机快速部署

**第一步**：点击 [这里](https://github.com/DSO-Lab/passets/archive/master.tar.gz) 下载最新的部署文件包并解压缩：

```bash
curl -L https://github.com/DSO-Lab/passets/archive/master.tar.gz -o master.tar.gz
tar -zxf master.tar.gz
cd passets-master/
```

**第二步**：修改 [`docker-compose`] 配置文件中下列参数：

```
services:
    api:
    ...
      environment:
        ...
        # 配置API访问密钥，该密钥用于通过 API 获取资产数据
        SECRET=<dsolab-passets-api-secret>
    ...
    sensor:
        ...
        environment：
        # 流量镜像网卡配置
        - interface=<网卡编号>
```

**第三步**：获取最新的指纹库、IP定位数据库

获取最新的指纹库，保存到当前目录下的 rules 目录下。
``` bash
# Wappalyzer 指纹库
curl -L https://github.com/AliasIO/Wappalyzer/raw/master/src/apps.json -o ./rules/apps.json

# NMAP 指纹库
curl -L https://svn.nmap.org/nmap/nmap-service-probes -o ./rules/nmap-service-probes
```

IP 地址数据库的更新请参阅 [passets-logstash](https://github.com/DSO-Lab/passets-logstash) 的文档说明。

**第四步**：定义自己的内部IP地址

内部IP地址默认已配置为通用局域网IP地址，用户可以通过修改 `docker-compose.yml` 中 Logstash 容器的 `INNER_IP_LIST` 环境变量来自定义内部 IP 地址列表。格式为“<起始IP>-<结束IP>,IP”（单条记录支持IP范围和单个IP，多条记录用半角逗号分隔，不能有空格），配置示例如下：

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

**第五步**：创建数据、日志目录并赋权

在 docker-compose.yml 文件同级目录下创建下列目录：
``` bash
mkdir -p data/elasticsearch/nodes
mkdir -p data/logstash
mkdir -p data/kibana
mkdir -p data/logs
chown -R 1000 data
# E.L.K. 默认使用 uid 为 1000的用户运行
```

**第六步**：启动应用

``` bash
docker-compose up -d
```

启动时将首先从 Docker HUB 上下载各模块的镜像文件，然后运行，可能需要等待一段时间。等待系统启动完成后，可以通过下面的地址访问 API 接口：

http://x.x.x.x:8081/swagger-ui.html

或者通过集成的 Kibana 进行可视化查询或展示（[Kibana 配置方法示例](docs/KIBANA_HELP.md)）：

http://x.x.x.x:5601/

### 集群部署

采用集群部署时，需要根据需要创建各个模块的 docker-compose 配置文件，配置文件中需要调整的主要为环境变量和映射卷，主要配置参数请参考下表：

#### Elasticsearch

| 类型         | 参数名              | 参数说明
|--------------|---------------------|--------------------------------------------------|
| environment  | discovery.type      | 单节点模式时需配置为 single-node
| volumes      | /usr/share/elasticsearch/data    | Elasticsearch 数据目录
| volumes      | /usr/share/elasticsearch/logs    | Elasticsearch 日志目录
| port         | 9200                | 对外开放的 ES 端口，仅集群模式下主节点需要配置

#### Logstash

| 类型         | 参数名              | 参数说明
|--------------|---------------------|--------------------------------------------------|
| environment  | ELASTICSEARCH_URL   | ES 服务器地址:端口
| environment  | ELASTICSEARCH_INDEX | ES 索引前缀，系统会自动在后面追加 “-yyyyMMdd”，不建议修改
| environment  | INNER_IP_LIST       | 用于定义企业的内部IP地址，支持地址段和地址，多个以逗号分隔，不允许出现空格
| volumes      | /usr/share/logstash/data    | Logstash 数据目录
| volumes      | /usr/share/logstash/logs    | Logstash 日志目录

#### Kibana

| 类型         | 参数名                 | 参数说明
|--------------|------------------------|--------------------------------------------------|
| environment  | ELASTICSEARCH_HOSTS    | ES 服务器 URL，示例：http://127.0.0.1:9200
| environment  | I18N_LOCALE            | Kibana 使用的界面语言
| volumes      | /usr/share/kibana/data | Kibana 数据目录
| volumes      | /usr/share/kibana/logs | Kibana 日志目录
| port         | 5601                   | 对外开放的 Kibana 端口

#### Passets-Sensor

| 类型         | 参数名              | 参数说明
|--------------|---------------------|--------------------------------------------------|
| environment  | interface           | 流量采集网口编号，与宿主机相同，例如：eth0、ens160等
| environment  | ip                  | Logstash 服务器地址（只有集群模式才需要修改）
| environment  | port                | Logstash 服务器接收数据的端口
| environment  | tag                 | 记录标识，分布式场景下用于识别数据来自哪个采集模块
| environment  | cache               | 采集器缓存的已处理记录数，缓存时间120秒，先进先出
| environment  | timeout             | 采集器内存回收超时时间，超过指定的时间，采集器自动回收内存
| environment  | debug               | 调试模式开关，生产环境禁用，将产生大量输出

#### Passets-Filter

| 类型         | 参数名              | 参数说明
|--------------|---------------------|--------------------------------------------------|
| environment  | ELASTICSEARCH_URL   | ES 服务器地址:端口
| environment  | ELASTICSEARCH_INDEX | ES 索引前缀，需与Logstash配置保持一致
| environment  | THREADS             | 清洗线程数，默认10，建议不超过20
| environment  | RANGE               | 首次处理数据的时间提前量，单位分钟，默认15
| environment  | BATCH_SIZE          | 每线程单次处理的数据条数，默认20条
| environment  | CACHE_SIZE          | 清洗模块缓存的已处理记录数，默认1024
| environment  | CACHE_TTL           | 清洗模块缓存的过期时间，单位秒，默认600
| environment  | MODE                | 工作模式：1-主节点，0-从节点，默认为1
| environment  | DEBUG               | 调试模式开关，0以上整数，生产环境禁用
| volumes      | /opt/filter/rules/  | Wappalyzer、NMAP指纹库文件
| volumes      | /opt/filter/config/plugin.yml | 清洗插件配置，控制插件的启用和关闭，可不配置此项

#### Passets-Api

| 类型         | 参数名              | 参数说明
|--------------|---------------------|--------------------------------------------------|
| environment  | ELASTICSEARCH_URL   | ES 服务器地址:端口
| environment  | ELASTICSEARCH_INDEX | ES 索引前缀，需与Logstash配置保持一致
| environment  | SECRET              | API 认证密钥，任意不含空格的字符串，该密钥用于填充 API 模块的 X-Auth-Secret 参数，实现 API 访问认证
| port         | 8080                | 对外开放的 API 端口


**注** 此处仅列出了与各模块正常运行密切相关的一些配置参数，实际配置中还有一些跟容器相关的参数需要配置，例如： network、restart、depends_on、container_name、image等，请参考 [docker-compose](docker-compose.yml) 配置文件根据实际情况进行配置。

## 帮助文档

详细配置说明参见 [```docs```](./docs) 目录中的文档。


## 目录结构

```
├─ docker-compose.yml        # docker-compose 配置文件（X86_64）
├─ config                    # 配置文件
│  ├─ kibana.ndjson          # Kibana 配置文件
│  └─ plugin.yml             # 数据清洗模块配置文件
├─ docs                      # 文档
│  └─ ... ...
├─ rules                     # 指纹库
│  ├─ apps.json              # Wappalyzer 开源Web指纹库
│  └─ nmap-service-probes    # NMAP 指纹库
└─data                       # 容器数据目录，需自行创建
   ├─ elasticsearch          # Elasticsearch 数据
   ├─ logstash               # Logstash 数据
   ├─ kibana                 # Kibana 数据
   └─ logs                   # E.L.K 日志
```

## 链接

* [修改日志](./CHANGELOG.md)
* [缺陷跟踪](https://github.com/DSO-Lab/passets/issues)
* [软件授权](./LICENSE)
