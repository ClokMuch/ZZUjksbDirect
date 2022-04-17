# ZZUjksbDirect
关键词： **健康打卡 郑州大学 健康上报 jksb zzu**

[![最后一次Action运行标记](https://github.com/ClokMuch/ZZUjksbDirect/actions/workflows/python-app.yml/badge.svg)](https://github.com/ClokMuch/ZZUjksbDirect/actions/workflows/python-app.yml)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![stable](http://badges.github.io/stability-badges/dist/stable.svg)](http://github.com/badges/stability-badges)

&emsp;&emsp;郑州大学健康上报/打卡的自动实现，本方法不再使用无头浏览器模拟登入，而是使用更直接的方式进行，并且更新了可用性.

# 使用说明


## 开箱即用的操作指南
**建议使用电脑进行操作**

### 1. 配置您的隐私信息：学号、密码、地址等

> 学号，密码，城市码，地理位置，真实姓名，反馈邮箱（接收邮件），可选疫苗接种情况默认3次全部接种！学号2，密码2，城市码2，地理位置2，真实姓名2，反馈邮箱2

**对于地理位置，支持修正只读文本框（对应 memo22 ）的获取情况，修正方法：`可自己填写的地理位置框@只读文本框自动获取的位置`，当有多个@存在时，仅解析首个@对应的两侧内容，可参考示例模仿.**

**注意事项：分割每一位用户是中文叹号 `！`，分割单个用户具体信息是中文逗号`，`  单个用户使用时不需要添加中文叹号**
举例：
> 2009788745693，eG43&tQgDF2KzF#M，1012，河南省.猫猫市.郑州大学@郑州大学主校区，钱青玉龙，septemberRecever2413@qq.com

### 2. 备用：项目更新方法
~~**可以使用 @d6imde9 提到的 删库-重建 更新法**~~ **建议不要使用删库重建法，因为删库重建后需要重新配置密码等信息，比较麻烦，参考方法如下：**

![img.png](image_folder/step04.png)
* 按图片指示顺序点击；
* 若未自行修改/优化代码，则能顺利同步更新；若您优化/修改了代码，您可以自行比对进行更新.

# 结束
* 感谢项目 [d6imde9/ZZUClock](https://github.com/d6imde9/ZZUClock) 提供的 Actions 技巧；
* 同类项目推荐：[mauhin/justsoso](https://github.com/mauhin/justsoso)  （如果不允许推荐，请发布 Issue 或电邮联系我 (._. )）
* 如有异常问题，您可以将失败的邮件转发给我（注意删去关键隐私信息），我**不一定**会帮助您处理异常；
* 如您喜欢全球最大的同性交友网站，您可以尝试创建 Issue 来描述您的问题，**请注意不要泄露您的反馈邮件**；
* 也欢迎您通过电邮联系我 1831158739@qq.com （此 QQ 无法添加好友，但您可以直接发送电邮）；
* 本项目随时可能会删库跑路（很快了，大概很快就要跑路了 (｀∇´)
