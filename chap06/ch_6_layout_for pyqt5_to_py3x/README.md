# 说明
1、此文件是《PyQt快速编程指南》一书中第六章的主要代码，包括习题答案和主窗口部件，都在mainwindow.py文件中。
2、新建对话框文件在newimagedlg.py中；此对话框对应的ui文件在ui_newimagedlg.py中。
3、resizedlg.py是更改图片尺寸的代码，这也是习题的一部分。
4、helpform.py是帮助文档的代码。
5、qrc_resources.py是resources.qrc使用pyrcc5生成的代码，命令是：pyrcc5 resources.qrc qrc_resources.py，其中文件地址在qrc文件中，生成结果是所有图片等素材打包到了这个py模块中。
6、推荐将pip的源改为清华大学镜像，国外主站速度实在太慢。


PyQt还是有一些坑的，这一章尤其是。我正是在QTCN.org/pyqtbook这个网站找到了PyQt5和Py3的大家修改的代码才真正开始自己的Python GUI编程的，
特别感谢这些网友提供的代码,因此，我希望自己也可以做出一些微不足道的贡献。

Corkine Ma <cm@mazj.me> 2017/10