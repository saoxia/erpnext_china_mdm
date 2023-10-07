## Medical Device Manufacturers（中国本地化的ERPNext医疗器械制造业解决方案）

### 功能介绍
使用ERPNext China作为基础，针对中国本地化医疗器械制造业进行定制。
#### 默认开启的功能：
开发中

#### 默认关闭的功能：
1. 飞鱼crm的销售线索自动更新到ERPNext的crm线索板块

#### 版本兼容性
V15：已通过兼容测试
V14：理论兼容，未测试


### 安装步骤

首先，获取app
```sh
$ bench get-app https://github.com/digitwise/erpnext_china_mdm.git
$ bench get-app https://github.com/digitwise/erpnext_china.git
```

然后，安装erpnext和erpnext_china
```sh
$ bench --site demo.com install-app erpnext erpnext_china erpnext_china_mdm
```