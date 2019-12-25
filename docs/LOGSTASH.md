# Logstash 使用说明

## 版本要求

- Logstash 7.4.1 及以上

## 容器安装

详细的安装说明，请参阅[官方支持文档](https://github.com/docker-library/docs/tree/master/logstash/)。

### 获取镜像

通过下面的命令从 Docker HUB 上获取 Logstash 镜像：

```
docker pull logstash:7.4.1
```

## Logstash 配置

Passets 被动资产识别引擎中在 Logstash 模块位置集成了四个数据处理规则，其中ip、url采用外部脚本来实现，分别如下：

| 插件名 | 插件用途 | 数据变化 |
|--------|----------|----------|
| ip     | 识别内网IP   | 生成ip_num（IP地址的数值形式）、inner（标识内外网）属性
| url    | 拆分URL，生成URL模板 | 生成site（站点）、path（路径）、url_tpl（URL模板）属性
| geoip  | 识别IP的地理位置     | 生成geoip.country_name（国家）、geoip.city_name（城市）、geoip.location.lon（经度）、geoip.location.lat（维度）属性

***注意：ip、url和geoip三个规则没有顺序要求。***

配置文件 logstash.conf 示例：

```
# 数据结构调整规则，生成host字段，将 message 字段的子字段全部移到上一级，并删除 message 字段
mutate {
    add_field => {
        "host" => "%{ip}:%{port}"
    }
    remove_field => ["message"]
}
# 内网IP识别规则，通过inner_ips定义内网地址端（示例中使用IPv4定义的局域网IP地址段）
ruby {
    path => '/usr/share/logstash/config/ip.rb'
    script_params => {
        'inner_ips' => [
            '10.0.0.0-10.255.255.255',
            '172.16.0.0-172.31.255.255',
            '192.168.0.0-192.168.255.255',
            '169.254.0.0-169.254.255.255',
            '127.0.0.1-127.0.0.255'
        ]
    }
}
# IP归属地识别规则
geoip {
    source => "ip"
    target => "geoip"
    fields => ["city_name", "country_name", "longitude", "latitude"]
    database => "/usr/share/logstash/config/GeoLite2-City.mmdb"
    add_field => {
        "[geoip][location][lon]" => "%{[geoip][longitude]}"
        "[geoip][location][lat]" => "%{[geoip][latitude]}"
    }
    remove_field => ["[geoip][longitude]", "[geoip][latitude]"]
}
mutate {
    convert => ["[geoip][location]","float"]
}
# URL拆分规则
if [pro] == 'HTTP' {
    ruby {
        path => '/usr/share/logstash/config/url.rb'
    }
}
```

## 创建数据、日志目录

```
mkdir data/logstash -p -m 777
mkdir data/logs -p -m 777
```

**注意**: 目录权限必须为777


## 容器启动

### 使用 docker 命令启动

```
docker run -p 5044 -e "TZ=Asia/Shanghai" -e "ELASTICSEARCH_URL=passets-elasticsearch:9200" -e "ELASTICSEARCH_INDEX=logstash-passets" -e "INNER_IP_LIST=192.168.0.0-192.168.255.255" -v "$(pwd)/data/logstash:/usr/share/logstash/data" -v "$(pwd)/data/logs:/usr/share/logstash/logs" -v "$(pwd)/logstash/:/usr/share/logstash/config/" -v "$(pwd)/rules/GeoLite2-City.mmdb:/usr/share/logstash/config/GeoLite2-City.mmdb" -d  logstash:7.4.1 /usr/share/logstash/bin/logstash -f /usr/share/logstash/config/logstash.conf --config.reload.automatic
```

### 使用 Docker Compose 启动

```
version: "3"

services:
  logstash:
    image: logstash:7.4.1
    container_name: passets-logstash
    environment:
      - TZ=Asia/Shanghai
      - ELASTICSEARCH_URL=http://passets-elasticsearch:9200    # Elasticsearch URL
      - ELASTICSEARCH_INDEX=logstash-passets                   # Elasticsearch 索引
    ports:
      - 5044:5044/udp                                          # 指定接收流量数据的端口
    volumes:
      - ./data/logstash:/usr/share/logstash/data               # 将数据目录映射到容器外
      - ./data/logs:/usr/share/logstash/logs                   # 将日志目录映射到容器外
      - ./logstash/:/usr/share/logstash/config/                # 使用容器外部的配置文件
      - ./rules/GeoLite2-City.mmdb:/usr/share/logstash/config/GeoLite2-City.mmdb # 使用容器外部的IP归属地数据库
    entrypoint: ['/usr/share/logstash/bin/logstash', '-f', '/usr/share/logstash/config/logstash.conf', '--config.reload.automatic'] # 覆盖容器默认的启动命令
```

启动容器：

```
docker-compose up
```
