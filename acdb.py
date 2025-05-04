import os
import requests
import ctypes
import time
import json
from colorama import init, Fore, Style

# 初始化colorama
init()

# 配置文件路径
CONFIG_FILE = "acdb_config.json"

# 默认配置
DEFAULT_CONFIG = {
    "url": "https://api.160621.xyz/img/ai/index.php",
    "interval": 60
}

# 全局变量
config = DEFAULT_CONFIG.copy()
count = 1
running = True

# 加载配置
def load_config():
    global config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            print(f"{Fore.CYAN}[INFO] 已加载配置文件{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}[WARN] 配置文件不存在，将使用默认配置{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR] 加载配置失败: {e}{Style.RESET_ALL}")
        config = DEFAULT_CONFIG.copy()
        return False

# 保存配置
def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        print(f"{Fore.GREEN}[SUCCESS] 配置已保存到 {CONFIG_FILE}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] 保存配置失败: {e}{Style.RESET_ALL}")

# 设置壁纸
def set_wallpaper(image_path):
    try:
        spi_setdeskwallpaper = 20
        ctypes.windll.user32.SystemParametersInfoW(spi_setdeskwallpaper, 0, image_path, 3)
        return True
    except Exception as e:
        print(f"{Fore.RED}[ERROR] 设置壁纸失败: {e}{Style.RESET_ALL}")
        return False

# 下载并设置壁纸
def download_image(img_url):
    global count
    print(f"{Fore.CYAN}[INFO] {Fore.YELLOW}第 {count} 次切换壁纸...{Style.RESET_ALL}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(img_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            with open("image.webp", "wb") as f:
                f.write(response.content)
            print(f"{Fore.GREEN}[SUCCESS] 下载图片成功！{Style.RESET_ALL}")
            
            image_path = os.path.join(os.getcwd(), 'image.webp')
            print(f"{Fore.CYAN}[INFO] 等待5秒钟准备设置壁纸...{Style.RESET_ALL}")
            time.sleep(5)
            
            if set_wallpaper(image_path):
                print(f"{Fore.GREEN}[SUCCESS] 壁纸切换成功！{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[INFO] 下一次切换将在 {config['interval']} 秒后进行{Style.RESET_ALL}")
                count += 1
                return True
            return False
        else:
            print(f"{Fore.RED}[ERROR] 下载图片失败，状态码: {response.status_code}{Style.RESET_ALL}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR] 网络请求异常: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR] 发生未知错误: {e}{Style.RESET_ALL}")
        return False
    finally:
        print("-" * 50)

# 获取用户配置
def get_user_config():
    global config
    
    print(f"{Fore.CYAN}[配置] 请输入图片API URL (默认: {DEFAULT_CONFIG['url']}):{Style.RESET_ALL}")
    url_input = input().strip()
    if url_input:
        config['url'] = url_input
    
    while True:
        print(f"{Fore.CYAN}[配置] 请输入壁纸切换间隔(秒) (默认: {DEFAULT_CONFIG['interval']}):{Style.RESET_ALL}")
        interval_input = input().strip()
        
        if not interval_input:
            break
            
        try:
            interval = int(interval_input)
            if interval < 10:
                print(f"{Fore.YELLOW}[WARN] 间隔时间太短，已设为最小值10秒{Style.RESET_ALL}")
                interval = 10
            config['interval'] = interval
            break
        except ValueError:
            print(f"{Fore.RED}[ERROR] 请输入有效的整数{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}[配置] 当前配置:{Style.RESET_ALL}")
    print(f"  API URL: {config['url']}")
    print(f"  切换间隔: {config['interval']}秒")
    
    save_config()

# 主函数
def main():
    global running, config
    
    print(f"{Fore.CYAN}=" * 50)
    print(f"{Fore.CYAN}ACDB 壁纸自动更换器 - 控制台版")
    print(f"=" * 50 + Style.RESET_ALL)
    
    # 加载配置，如果配置不存在则获取用户输入
    if not load_config():
        get_user_config()
    
    print(f"{Fore.GREEN}[INFO] 程序已启动，按 Ctrl+C 停止程序{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[INFO] 当前配置: URL={config['url']}, 间隔={config['interval']}秒{Style.RESET_ALL}")
    
    try:
        while running:
            if download_image(config['url']):
                time.sleep(config['interval'])
            else:
                # 如果下载失败，等待较短时间后重试
                print(f"{Fore.YELLOW}[WARN] 将在30秒后重试...{Style.RESET_ALL}")
                time.sleep(30)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}[INFO] 程序已停止{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] 程序异常: {e}{Style.RESET_ALL}")
    finally:
        print(f"{Fore.CYAN}[INFO] 感谢使用ACDB壁纸自动更换器{Style.RESET_ALL}")

if __name__ == "__main__":
    main()