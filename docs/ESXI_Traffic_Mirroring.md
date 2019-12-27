### ESXI场景流量镜像配置

**第一步**：创建虚拟交换机网络，并分配独立物理网口，该网口用于接收流量镜像数据使用。

![exsi_vSwitch](images/exsi_vSwitch.png)

**第二步**：虚拟交换机属性配置，开启”混杂模式“。

![exsi_vSwitch_config](images/exsi_vSwitch_config.png)