#-*- coding:utf-8 -*-

import socket
import random
import json

server_ip = '192.168.199.10'
server_port = 5044

http_json = {"pro": "HTTP", "tag": "lo", "ip": "2001:DB8:0:23:8:0:0:1881", "port": 80, "method": "GET", "code": "200", "type": "text/html; charset=utf-8", "server": "", "header": "Date: Wed, 18 Nov 2020 10:54:24 GMT\r\nContent-Length: 955\r\nContent-Type: text/html; charset=utf-8", "url": "http://[2001:db8:0:23:8::1881]/", "body": "<!doctype html>\n<html lang=\"en\">\n\n<head>\n  <meta charset=\"utf-8\">\n  <title>Passets -- \u7ba1\u7406\u5e73\u53f0</title>\n  <base href=\"/\">\n\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <link rel=\"icon\" type=\"image/x-icon\" href=\"assets/favicon.ico\">\n<link rel=\"stylesheet\" href=\"/static/styles.392be9f96327b8a543a2.css\"></head>\n\n<body>\n  <app-root></app-root>\n<script src=\"/static/runtime-es2015.96d5615b06d74eaaeee8.js\" type=\"module\"></script><script src=\"/static/runtime-es5.96d5615b06d74eaaeee8.js\" nomodule defer></script><script src=\"/static/polyfills-es5.ef4b1e1fc703b3ff76e3.js\" nomodule defer></script><script src=\"/static/polyfills-es2015.2987770fde9daa1d8a2e.js\" type=\"module\"></script><script src=\"/static/scripts.7325031e99ec79e877aa.js\" defer></script><script src=\"/static/main-es2015.d2adbb6669d8e6a4ca42.js\" type=\"module\"></script><script src=\"/static/main-es5.d2adbb6669d8e6a4ca42.js\" nomodule defer></script></body>\n\n</html>\n"}
tcp_json = {"pro": "TCP", "tag": "lo", "ip": "220.194.238.58", "port": 47808, "data": "16030300550200005103035fbc76d565873c0a90c9c1c8421c4479a0dd93db0e669493440b67dd3f1a70ce205fbb71e157361cb06810d81fdd2c9fd5cc1f64e054d5a9f4899bd3fd6978233bc028000009ff0100010000170000"}
https_json = {"pro": "TCP", "tag": "lo", "ip": "59.111.239.61", "port": 443, "data": "160303007a020000760303344f5d69a6dcae82902adb80930fc61ad9094c70f8b7c1fbaa47f462df2241b62012bb5f0f6be9c0dd502c1413fa0144d664892ff6c4b9af58d50e2f237a18e136130100002e00330024001d00203157283f3310335bc869052990ec5019691faf6471c1001b9bf1289550aad040002b000203041403030001011703030c31cd164a8e5d11a3507b4582d966fd94e0b3bc586b7100ac02284d39e4acd81a52748d5fb575c0abe0e32ef63b888fafc04c29cc9c6f170b2d7a949f889b83291dd4c7faed27b436c6f2fe77617ee9224187ac2eb1b883d6316a5084231866bbd1e97f46f6dabcfe11744d83c53267e218c8b6d6bdc4e44a5f34e8ddc392ab14ccd7df299b148436620518572d198a9304fb2e672b687fcc13b8a919d041d62aeec60021932db4fbe36e9ca0c14a66b416219b0087e24e1bc9275798328870aeb6d13b6e81c000be00943d7efcf784d776db6fd8e2f12b2ee406d442854c880ce81792bf34650b3e0e588ca401bd7158e8844084590859a13b5426eddb565d29c535111c7013356e75e294e9190d655652566b184ae16b8da689fc07fb34541f0b1cb832ed7829df38db0c18cc2d49fa3b974b9932fcd3d32d8bba36c8833af833cbb41427b8c2fe4e2ec3596703457e353ebe36e938478d30a48c88f99a548fdfb9fcdac31c5f8b3fc213d296b5751a796bba9e293b1b9346db324c3632a12552e96ff3ad36aba49a565b9830f2db87e00b60c27259bc07db51deff299d1a21b685f7b5003d98e5d0c84012847391cd043f1ef68f6f6c63c2018f1fdef702d9207eaa0a314d1f1ccbd2d1f14820f44e4571f282c5605c920db1250f6bd232ef798f66646061b34485d1d26a82046e3e071610adbb9d4dce72161c60cda003146013771d7c931ea0eeb2f1040c4ba3575376fc5c3a63cd2362ba15a08e39bcc935b4f1fec3688bee9cfb3b2b28cbeefa239067d87276afa07f0ad0bc56143d9664b2eecfd2c86fce61ff6ede618cedf1eb3aba654a7243423a1517a96d5b6a8f91f769ac362483a7c0dc1e4207c155ab312c996be7ebc984c241fce8a5582c06296f17afd744745a5a802a08930781feed07542061bda19e0686494cd45a0ff1a36aad428bb57425fb02fdedefa785af9d28aa8ad64cbd3357b160b75ee8bb78beb8a223983c7009d52c25d36e02d8d29e43ddcead42f8a2dc02d275718cf2f3b615d7387d1fb435a8a78c252df71520dc10fadee0531136cc5d13477d2bcac5198824b191821eeada86aae1381c3665037d521e0eb8feb91a37bf6b2831170080dfc996e2bb3a64c9fc15ebfac7e6adb84cac824f8f372f4fac52a60673eeaca8a099bbb59d3822252f0d26a5784079685d2bb595a9c8e53746ea0c09773198230383a594cae4f023e650ab626abdf5b7428e3b0e4c71359c7f2a23df54325b8cbd845edfbc5bd7b21665974f942275fecc2ed638bf53e690fb199080b95542b7770e64f2c19023e76c37c88044affae6685d08e90df3cd9d05fd7ea59071366d7b7708023412cefbbb18de8848c26278a6c4ea9b62e5fc057e41ac933167717f7cb6e5a48f7db88f90fbfae1cfb673e4c6e6b93a095ea75d6be5ed2c6dcba424528c47c1f11cc0fe9c4c53c8cdeb0cbb524c32285961b3a7f9f297e4df3e760df17c09e208218a7959dd74ab4f398a457ca3b229db5489ffce89a0890671fb630191ab9047f78a0823dcb6da46f12435060fd3ae80dfeff4cd25a4bcbb123264e59e63b1ccae5d8cd58da95dd139d91231fff2610a9410513dbcd2002d7bd2c8de2b0b9e8d0cbbe18c4bfabe1e65379a07179846d95a2f751fc0694253d3b744edc91005e27d113c4d4046c3a1a87de427dbad89d754b07d54025cf398aa976d8888e7bdfe26dfe3cf5a35558f7d2cb0a63ce3e426ebe0168a5eaf1ee98c7ea5a6af76875823f7b2f46441f819d4e6a7a0824e7c4fff8a3614952658ad669a219a690c56e62d3dadc6fa0f57e7dfeec2b8c3da6d13378da6cea4086de9e2"}
msg_list = [http_json,tcp_json,https_json]
# TCP Send
class _tcp_msg_send:
	def __init__(self,server_ip,server_port):
		self.server_ip = server_ip
		self.server_port = server_port
		self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#心跳维护
		self.tcp_client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		self.tcp_client.connect((self.server_ip, self.server_port))

	def info(self,msg):
		try:
			self.tcp_client.send(msg.encode()+b"\n")
			return True
		except socket.error as e:
			if e.errno == 32:
				return False
		# self.tcp_client.close()


send_obj = _tcp_msg_send(server_ip,server_port)
while 1:
	msg =  random.choice(msg_list)
	send_obj.info(json.dumps(msg))