## CUUSP后端代码
### 简介

CUUSP(College and University unified service platform)

中文名为高校统一服务平台，其主要功能是聚合高校里比较常用的服务。如各种教务信息(通知，课表，成绩，考试等)，其它聚合信息（失物招领，跳蚤市场）。
项目对标的是超级课程表，也可以说是开源版的超级课程表。


### 使用

1. 克隆本项目
2. 执行`pip install -r requirements.txt`
2. 在项目主目录里的`config.py`里配置好mysql连接地址
3. 进入项目主目录`cd cuusp_backend`
4. 执行`flask fake`生成虚拟数据
5. 执行`flask test`进行单元测试
6. 执行`flsk run`运行开发服务器

### 参与开发
目前整个项目只有三个人开发(2前端+1后端)。整体来说，开发难度较大，我们希望更多的人能参加到此项目中，为项目贡献代码
#### 环境
开发环境：python 3.7.5
后端框架：Flask
ORM: Peewee
数据库：mysql 5.7.26

项目采用的是多前端+单后端模式
多前端包括H5,微信小程序,QQ小程序,原生APP
目前正在开发微信小程序
#### 项目目录说明
```
cuusp_backend
├── README.md --项目说明文档
├── app --应用程序主目录
│   ├── __init__.py --应用程序初始化(工厂模式)
│   ├── api --所有业务
│   │   ├── __init__.py
│   │   ├── authentication.py --用户认证相关
│   │   ├── decorators.py --装饰器
│   │   ├── microservice.py --微服务相关
│   │   └── service --对查询结果的包装
│   │       ├── auth_service.py --对应authentication.py
│   │       └── ms_service.py --对应microservice.py
│   ├── models.py --数据库模型文件
│   └── utils --工具类
│       ├── __init__.py
│       ├── crypto_util.py --加解密工具
│       ├── jwt_util.py --jwt相关工具
│       ├── log_util.py --日志工具
│       ├── login_util.py --第三方登录相关工具
│       ├── req_util.py --http请求相关工具
│       ├── requests_util.py --requests库简易包装
│       ├── resp_code_util.py --内建响应码到Json支持
│       └── ret_util.py --项目状态码
├── boot.py --项目引导文件
├── config.py --项目配置文件(已不采用)
├── fake --虚拟数据
│   └── __init__.py
├── logs --日志文件
│   └── CUUSP_2020-02-08.log
├── requirements.txt --项目依赖文件
└── tests --单元测试
	├── .env_test --测试用配置文件
    ├── __init__.py
    ├── test_auth_service.py
    ├── test_authentication.py
    ├── test_base.py
    ├── test_microservice.py
    └── test_ms_service.py
```
因开发还未完成，项目目录会有所增加或减少
###  开发日志

2020 2.8:搭建项目框架

