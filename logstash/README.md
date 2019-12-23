# 简介

此文件夹用于放置 Logstash 相关配置文件。

**GeoLite2 IP定位库**

GEOIP 规则库用于识别数据中对应的IP所在的地理位置。由于库文件较大，需要自行从其官网下载，下载后解压缩提取其中的 GeoLite2-City.mmdb 文件放到 当前目录下。

```
$ curl -L https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -o GeoLite2-City.tar.gz
$ tar -C ./ --strip-components=1 -zxf GeoLite2-City.tar.gz
$ rm -f GeoLite2-City.tar.gz
```