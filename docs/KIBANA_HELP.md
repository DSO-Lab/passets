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

也可以使用下面的请求通过程序导入 Kibana 配置，实现自动化配置：

```
POST /api/saved_objects/_import?overwrite=true HTTP/1.1
Host: 127.0.0.1:5601
Connection: keep-alive
Content-Length: 36098
Origin: http://127.0.0.1:5601
kbn-version: 7.4.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarylDGWyMO66tGqmSoA
Accept: */*
Referer: http://127.0.0.1:5601/app/kibana
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9

------WebKitFormBoundarylDGWyMO66tGqmSoA
Content-Disposition: form-data; name="file"; filename="kibana.ndjson"
Content-Type: application/octet-stream

<导出的配置文件内容>
------WebKitFormBoundarylDGWyMO66tGqmSoA--
```