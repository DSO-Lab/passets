# 构建方法

1. 修改 build.gradle，将其中的 logstashCorePath 替换为 Logstash 中 logstash-core 目录所在的位置

2. 执行下面的命令：

```
gradlew

gradlew build
```

3. 将 build/libs/ 目录中提取生成的 logstash-filter-geoip-6.0.0.jar 放到 vendor/jar-dependencies/org/logstash/filters/logstash-filter-geoip/6.0.0/ 目录下

4. 删除 build 目录
