Android系统UI自动化测试项目
=
框架架构：
![](https://pic1.zhimg.com/80/v2-259b92e129cdbdd95c38e38b1b480cec_1440w.jpg)
<br>`效果：自己试了才知道！！！`<br> 
使用方法：<br> 
1、使用requirements.txt对依赖库进行安装<br> 
2、项目使用的是Python3.7（可自行调整）<br> 
3、最好使用Pycharm管理项目，方便修改<br> 
4、Pycharm使用的是Venv虚拟环境，即其Python包是独立的，便于将项目集成到其它地方<br> 
5、通过run_test.py定义需要执行的测试包<br> 
6、测试完成后生成的报告可浏览器打开查看<br> 

目前项目已实现功能：<br> 
1、批量管理设备：安装应用、应用授权<br> 
2、基于Pytest进行测试包测试<br> 
3、对Android系统应用通过Page划分集中管理<br> 

可能出现的问题：<br> 
1、首先对于pip3的报错使用该命令解决：<br>
```
sudo easy_install pip
```
如果出现通过pip3安装模块后，py运行还是失败的，使用pycharm的interpreter里面搜索对应模块再安装即可<br> 
2、# 本项目已修改源码：<br> 
路径：/Users/cgt/Library/Python/3.7/lib/python/site-packages/poco/drivers/android/uiautomation.py"<br> 
```
print("still waiting for uiautomation ready.")
```
```
self.adb_client.shell('am start -n {}/.TestActivity'.format(PocoServicePackage))<br>
``` 
3、# 兼容使用相对路径存在同目录下文件找不到问题：<br> 
修改Edit configurations -> 将Working directory改成当前项目目录即可<br> 
4、#airtest操作API<br> 
以下func大部分可单独运行：<br> 
a.单独调用 - 当前Device<br> 
b.指定device调用 - 控制不同设备（主要API选择）<br> 
以下是Airtest的API的用法，它提供了一些方法的封装，同时还对接了图像识别等技术，但Airtest也有局限性，不能根据DOM树
来选则对应但节点，依靠图像识别也有一定不精确之处，所以还需要另一个库Poco<br> 
5、遇到Python找不到，IntFlag时，unset PYTHONPATH<br> 
6、```"ImportError: sys.meta_path is None, Python is likely shutting down"``` <br>
这个报错是能忽略的，是因为poco报错后就退出了，主线程回收垃圾，剩下的子线程抛了这个错，是可以忽略的。<br> 
7、有些输入密码等界面因为Android安全机制保护，需要特别注意看是否能够获取到元素控件<br> 
8、# 修改源文件：<br> 
a.规避sys.meta_path is None, Python is likely shutting down问题导致的报错<br> 
/Users/cgt/PycharmProjects/AutomationProject/venv/lib/python3.7/site-packages/hrpc/object_proxy.py<br> 
``` 
try:    
    self._client__.evaluate(RpcObjectProxy(self._uri__, self._client__, action), wait_for_response=False)<br> 
except Exception as ex:
    print(ex)
``` 
9、Settings控制：<br> 
a、使用adb shell svc控制一些开关、wifi等<br> 
settings put和get有局限<br> 
b、注意流的开启和关闭对资源的消耗<br> 

`最后提到：`<br> 
`对于UI测试，不能覆盖所有的case，只能尽可能去转化一些case，不要为了自动化而自动化！！！`<br> 
<br>
[Bruce->知乎](https://zhuanlan.zhihu.com/p/356127011)


