import os
import requests
import ctypes
import time
import schedule

def set_wallpaper(image_path):
    """
    设置指定图像路径为桌面壁纸。

    参数:
    image_path: 字符串，指定的图像文件路径。

    返回值:
    无
    """
    SPI_SETDESKWALLPAPER = 20  # 定义设置桌面壁纸的系统参数标识符
    # 使用ctypes调用Windows API来设置桌面壁纸
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def download_image(url):
    """
    从指定的URL下载图像并将其设置为桌面壁纸。
    
    参数:
    url: 图像的URL地址。
    
    返回值:
    无
    """
    # 设置请求头
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
    # 发起HTTP请求获取图像
    response = requests.get(url,headers=headers)
    # 确保响应成功
    if response.status_code== 200:
        with open("image.webp", "wb") as f:
            f.write(response.content)
        print("Image downloaded successfully!")
    else:
        print("Failed to download image. Status code:", response.status_code)

    # 拼接图像的保存路径（当前工作目录下的'image.webp'）
    image_path = os.path.join(os.getcwd(), 'image.webp')

    # 等待20秒，确保桌面壁下载完成
    time.sleep(20)

    # 设置保存的图像为桌面壁纸
    set_wallpaper(image_path)

def main():
    """
    主函数，用于演示从指定网址下载图片的功能。
    
    参数: 
    无
    
    返回值:
    无
    """
    url = 'https://imgapi.160621.xyz/random.php'  # 指定图片下载的URL
    download_image(url)  # 调用函数下载图片

# 循环执行任务
while True:
    main()
    time.sleep(10)
