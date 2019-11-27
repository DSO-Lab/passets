### PF_RING安装

pf_ring需要在docker所在的宿主机上安装，详细说明，可以参见官方支持文档。

```
http://packages.ntop.org/
```

### 安装参考 - CentOS 7

> 系统版本: CentOS Linux release 7.7.1908 (Core)

pf_ring安装:

```
yum -y install wget net-tools
cd /etc/yum.repos.d/
wget http://packages.ntop.org/centos/ntop.repo -O ntop.repo
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum clean all
yum update
yum install pfring-dkms

systemctl start pf_ring
systemctl enable pf_ring
```

### 虚拟化场景网络配置

> 创建虚拟交换机网络，并分配独立物理网口，该网口用于接收流量镜像数据使用。

![exsi_vSwitch](images/exsi_vSwitch.png)

> 虚拟交换机属性配置，开启”混杂模式“。

![exsi_vSwitch_config](images/exsi_vSwitch_config.png)

### Docker安装

```
curl -fsSL https://get.docker.com/ | sh
yum -y install docker-compose
systemctl start docker
systemctl enable docker
```
