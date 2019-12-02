# 通过 Kibana 实现可视化展示

passets 被动资产发现框架内置了 `Kibana`，可以方便用户进行数据的可视化展示。

为了安全考虑，默认情况下 Kibana 仅对 `127.0.0.1` 开放，用户可以通过修改 `docker-compose.yml` 文件中的端口映射配置，使其可被外部访问。

```
services:
  ...
  kibana:
    ...
    ports:
      # 去除IP
      - "5601:5601"
```

修改配置后需要执行下面重新部署操作，使其生效：

```
docker-compose down
docker-compose up -d
```

初始化 Kibana 后，需要进行必要的配置，为便于使用可以通过导入配置文件完成以下步骤，已包含项目预定义的一套统计图表。

```
1、访问 Discover 模块，并自定义索引表达式为 passets
2、根据数据分析需求，创建Dashboard统计图表
```

通过 “`Management/Saved Objects`” 页面的 “`Import`” 功能导入。

[下载默认配置文件](../kibana.ndjson)

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

导入成功后，即可使用`Discover` 和 `Dashboard`等模块。

```
# 数据检索功能页面
http://x.x.x.x:5601/app/kibana#/discover
# 数据统计仪表板页面
http://x.x.x.x:5601/app/kibana#/dashboard/130f0440-102f-11ea-a7f8-65c9feeb13c9
```

