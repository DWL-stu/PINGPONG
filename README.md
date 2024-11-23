
<h1 align="center">PINGPONG -- python下强大的APT攻击框架</h1>
<div align="center">
<img src=https://files.cnblogs.com/files/blogs/820580/111.ico?t=1732333033&download=true>
</div>
<em><h3 align="center">使用python在瞬息万变的攻防战场上反弹你的shell并控制目标主机！</h3></em>
<p align="center">
<img src=https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge>
<img src=https://img.shields.io/badge/License-MIT-green?style=for-the-badge>
<img src=https://img.shields.io/badge/State-Developing-red?style=for-the-badge>
<img src=https://img.shields.io/badge/Platform-Windows-orange?style=for-the-badge>
<em><h5 align="center">一个基于pyinstaller进行免杀从而发动APT攻击的强大框架</h5></em>

> 🚧 **正在开发中......** 🚧
>
> PINGPONG框架正在经历一次彻底的重构。因此现在只具有基本的功能，脚本也很有限
# 目录

- [介绍](#介绍)
- [使用](#使用)
- [维护人员](#维护人员)
- [报告](#报告)
- [许可证](#许可证)

# 介绍

PINGPONG是一个开源免费的基于pyinstaller进行免杀的标准APT攻击框架。拥有优秀的免杀能力和极其简单的使用流程。是一个可以帮助你在攻防，渗透中提升成功率的利器。

## 为什么使用PINGPONG？

### 高免杀率  
在Virusscan.com上能做到100%免杀，拥有优秀的针对杀软的逃逸功能。  
![images](https://files.cnblogs.com/files/blogs/820580/www.virscan.org_report_a2832a4ad46407d8bbcc2b666093d7d16bd1efa478558f03bc2d69aa573ff7cf.ico?t=1732332626&download=true)
### 上手简单  
几乎不需要任何学习——PINGPONG中通过交互式菜单的方式实现了极高的易上手度。您只需要两分钟就可以创建一个强大的payload来反弹shell。  
![images](https://files.cnblogs.com/files/blogs/820580/1212.ico?t=1732333483&download=true)
### 功能众多  
除了基本的cmdshell以外，我们还提供了控制摄像头，提权，持久化，甚至是使目标主机蓝屏的一些脚本。为了使用简单，我们专门为设置做了一个UI界面
![images](https://files.cnblogs.com/files/blogs/820580/1111.ico?t=1732333273&download=true)
    
## 目前面临的问题
    
### 体积过大
一个基本的payload都要撑到5MB左右。在某些场景下不可接受
### 平台单一
只支持Windows平台，暂不支持Linux和MacOS
### 代码复杂
由于初期的开发问题，PINGPONG的代码写的极为混乱。本项目正在重构以解决此问题
    
# 使用
  ## 安装依赖
  ### Python 库安装

  ```
    pip install -u requirments.txt
  ```
  **本项目对pyinstaller的版本有严格要求，请按照requirments安装**
  ### 其余依赖
    
  upx 4.0（最好装一个，帮助你压缩payload体积）  
  ## 下载PINGPONG框架
  ```
 git clone https://github.com/DWL-stu/PINGPONG 
 ```
  ## 启动
   ```
   python main.py
   ```
  ## 工作流程
  - 通过payload generater生成payload
  - 通过handler打开监听
  - payload在目标机器上得到执行，反弹shell
  - 通过PINGPONG shell控制目标主机
     
   
# 维护人员
[@LamentXU](https://github.com/LamentXU123)

# 报告

请将你发现的bug或者你想提出的建议通过[github issue tracker](https://github.com/DWL-stu/PINGPONG/issues)发送给我，不胜感激！

 
# 许可证
[apache2 license](https://github.com/DWL-stu/PINGPONG/License).
