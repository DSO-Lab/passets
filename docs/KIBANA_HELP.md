# 通过 Kibana 实现可视化展示

Passets 被动资产发现框架内置了 `Kibana`，可以方便用户进行数据的可视化展示。

为了安全考虑，默认情况下 Kibana 仅对 `127.0.0.1` 开放，用户可以通过修改 `docker-compose.yml` 文件中的端口映射配置，使其可被外部访问。

```
services:
  ... ...
  kibana:
    ... ...
    ports:
      - "5601:5601"
```

修改配置后需要执行下面重新部署操作，使其生效：

```
docker-compose down
docker-compose up -d
```

初次使用 Kibana 时，需要进行必要的配置，主要是在访问 `Discover` 模块的时候定义索引表达式为 `passets`。为了便于使用，本项目定义了一套简单的图表，可以在初始使用的时候通过 “`Management/Saved Objects`” 页面的 “`Import`” 功能导入。

[下载基本配置文件](../kibana.ndjson)

导入成功后，即可使用`Discover` 和 `Dashboard`等模块。