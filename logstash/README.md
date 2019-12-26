# 简介

此文件夹用于放置 Logstash 相关配置文件。

**GeoLite2 IP定位库**

GEOIP 规则库用于识别数据中对应的IP所在的地理位置。由于库文件较大，需要自行从其官网下载，下载后解压缩提取其中的 GeoLite2-City.mmdb 文件放到 当前目录下。

```
$ curl -L https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -o GeoLite2-City.tar.gz
$ tar -C ./ --strip-components=1 -zxf GeoLite2-City.tar.gz
$ rm -f GeoLite2-City.tar.gz
```

**位置信息中文化**

如果需要将位置信息中的国家、城市等信息设置为中文，则可以使用框架自定义的geoip插件（位于./geoip）。详细配置如下：

1. 将修改后的插件映射到logstash gem目录下覆盖原插件：

```
services:
  logstash:
    ... ...
    volumes:
      ... ...
      - ./logstash/geoip:/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-filter-geoip-6.0.3-java
    ... ...
```

2. 修改 logstash/logstash.conf 文件中的geoip配置，添加如下属性设置：

```
geoip {
    ... ...
    locale => 'zh-CN'
}
```
