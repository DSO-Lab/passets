# Elasticsearch 使用说明

Elasticsearch 7.4.1安装，详细说明，可以参见[官方支持文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/docker.html)。

## 获取镜像

通过下面的命令从 Docker HUB 上获取 Elasticsearch 镜像：

```
docker pull elasticsearch:7.4.1
```

## 创建数据、日志目录

```
mkdir data/elasticsearch -p -m 777
mkdir data/logs -p -m 777
```

**注意**: 目录权限必须为777

## 容器启动

### 单节点 ES 容器启动

```
docker run -p 9200:9200 -e "TZ=Asia/Shanghai" -e "discovery.type=single-node" -v "$(pwd)/data/logs:/usr/share/elasticsearch/logs" -v "$(pwd)/data/elasticsearch:/usr/share/elasticsearch/data" -d elasticsearch:7.4.1
```

### 采用 Docker Compose 启动单节点 ES 容器

```
version: "3"

services:
  elasticsearch:
    image: elasticsearch:7.4.1
    container_name: passets-elasticsearch
    environment:
      - TZ=Asia/Shanghai
      - discovery.type=single-node
    ports:
      - "9200:9200"
    volumes:
      - ./data/logs:/usr/share/elasticsearch/logs
      - ./data/elasticsearch:/usr/share/elasticsearch/data
    restart: unless-stopped
```

启动容器：

```
docker-compose up
```

### 采用 Docker Compose 启动 ES 容器集群

多个容器节点需要启动时推荐使用 `Docker Compose` 来进行。

首先，创建 `elasticsearch.yml` 配置文件：

```
http.cors.enabled: true
http.cors.allow-origin: "*"
```

然后，创建 `docker-compose.yml` 文件：

```
version: "3"

services:
  elasticsearch:
    image: elasticsearch:7.4.1
    container_name: passets-elasticsearch
    environment:
      - TZ=Asia/Shanghai
      - cluster.name=docker-cluster       #集群名称，两个节点需要保持一致
      - bootstrap.memory_lock=true        #可根据需要配置
      - node.name=node-0                  #节点名称，与另外一个节点区分开
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - ./data/logs:/usr/share/elasticsearch/logs
      - ./data/elasticsearch:/usr/share/elasticsearch/data
      - ./elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    restart: unless-stopped

  elasticsearch2:
    image: elasticsearch:7.4.1
    container_name: passets-elasticsearch2
    environment:
      - TZ=Asia/Shanghai
      - cluster.name=docker-cluster       #集群名称，两个节点需要保持一致
      - bootstrap.memory_lock=true        #可根据需要配置
      - node.name=node-1                  #节点名称，与另外一个节点区分开
      - xpack.security.enabled=false
      - discovery.zen.ping.unicast.hosts=passets-elasticsearch  # 指定主节点的容器名
    volumes:
      - ./data/logs1:/usr/share/elasticsearch/logs
      - ./data/elasticsearch1:/usr/share/elasticsearch/data
      - ./elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    restart: unless-stopped
```

启动容器：

```
docker-compose up
```