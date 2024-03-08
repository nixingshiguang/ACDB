import tkinter as tk
import os
import requests
import ctypes
import time
import threading

# 默认的URL和间隔时间
url = "https://imgapi.160621.xyz/random.php"
interval = 60

# 计数起始值
count = 1

# 设置壁纸
def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20  # 定义设置桌面壁纸的系统参数标识符
    # 使用ctypes调用Windows API来设置桌面壁纸
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

# 下载并设置壁纸
def download_image(url):
    global count  # 声明count为全局变量
    print(f"第{count}次切换壁纸...")
    
    # 设置请求头，伪装为浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    # 发送GET请求获取图像
    response = requests.get(url, headers=headers)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 以二进制方式写入图像数据到本地文件
        with open("image.webp", "wb") as f:
            f.write(response.content)
        print("下载图片成功！")
    else:
        # 请求失败，打印状态码
        print("下载图片失败，状态码:", response.status_code)

    # 获取图像文件的完整路径
    image_path = os.path.join(os.getcwd(), 'image.webp')
    # 暂停2秒，确保图像文件写入完成
    time.sleep(2)
    # 设置图像为桌面壁纸
    set_wallpaper(image_path)
    print("切换壁纸成功！")
    count += 1

# 更换壁纸
def wallpaper_change():
    global url, interval
    def wallpaper_changer():
        while True:  # 不断循环，定期执行下载和设置壁纸的操作
            download_image(url)  # 下载图片
            time.sleep(interval)  # 按照设定间隔休眠，单位为秒
    
    thread = threading.Thread(target=wallpaper_changer)
    thread.start()

wallpaper_change()  # 启动壁纸切换线程

# 确认按钮事件
def on_submit():
    # 从交互界面获取用户输入的URL和间隔时间
    global url, interval
    url = url_entry.get()
    interval = int(interval_entry.get())

# 创建GUI界面
root = tk.Tk()
# 标题
root.title("ACDB 壁纸自动更换器")
# 图片API_url标签
url_label = tk.Label(root, text="图片API_URL:")
url_label.pack()  # 将标签添加到根窗口
url_entry = tk.Entry(root, width=50) # 创建输入框，设置宽度为50字符
url_entry.pack()  # 将输入框添加到根窗口
# 时间间隔标签
interval_label = tk.Label(root, text="壁纸切换间隔 (秒):")
interval_label.pack()
interval_entry = tk.Entry(root)
interval_entry.pack()
# 确认按钮
submit_button = tk.Button(root, text="确认", command=on_submit)
submit_button.pack()

root.mainloop()

