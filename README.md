# ACDB
ACDB——Automatic Change Desktop Background，即自动更换电脑桌面壁纸

## 介绍
+ 此程序为满足我突然的需求制作！

## 功能
1. 启动程序后，从API下载图片并设置为桌面壁纸
2. 每n秒下载一次图片更换壁纸
3. 下载的壁纸会替换旧的壁纸，不会留下过多的壁纸

## 下载
请从`dist`文件夹下载对应版本的程序

## 版本
1. `acdb.exe`：带控制台输出，关闭控制台窗口=结束程序
2. `acdb_no_console.exe`：无控制台输出，静静地运行在后台，关闭程序需要通过任务管理器关闭

## 使用方法
+ 使用我的API，直接运行程序即可，窗口可以直接关闭
+ 使用你自己的API，或者需要修改切换间隔，按以下步骤来：
  1. 运行程序
  2. 输入图片API的网址
  3. 输入切换壁纸时间间隔
  4. 确认

## 自行编译
1. 安装Python
2. 安装依赖库：`pip install -r requirements.txt`
3. 编译：
   + 带控制台输出版本：`pyinstaller --onefile -n acdb acdb.py`
   + 后台运行版本：`pyinstaller --noconsole --onefile -n acdb_no_console acdb.py`

## 注意事项
1. 关闭交互窗口不会影响程序运行
2. 切换壁纸时可能会有黑屏，是正常现象，因为没有做过渡处理，暂时没能力解决这问题