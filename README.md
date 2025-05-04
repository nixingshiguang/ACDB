# ACDB
ACDB——Automatic Change Desktop Background，即自动更换电脑桌面壁纸

## 介绍
此程序为满足我突然的需求制作！

## 功能
1. 启动程序后，从API下载图片并设置为桌面壁纸
2. 每n秒下载一次图片更换壁纸
3. 下载的壁纸会替换旧的壁纸，不会留下过多的壁纸

## 下载
请从[release](https://github.com/nixingshiguang/ACDB/releases)下载扩展名为`exe`程序

## 使用方法
  1. 运行程序
  2. 输入图片API的网址（使用默认配置可直接按回车键）  
  3. 输入切换壁纸时间间隔（使用默认配置可直接按回车键）  

## 自行编译
1. 安装Python
2. 安装依赖库：`pip install -r requirements.txt`
3. 打包成单文件程序：`pyinstaller --onefile -n acdb acdb.py`

## 注意事项
切换壁纸时可能会有黑屏，是正常现象，因为没有做过渡处理，暂时没能力解决这问题