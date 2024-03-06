using System;
using System.IO;
using System.Net.Http;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    // 调用 Windows API 设置桌面壁纸
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    private static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);

    static async Task Main(string[] args)
    {
        // 输出程序介绍和功能说明
        Console.WriteLine("！！！提示！！！\n此程序为满足我突然的需求制作，本人并不会C#语言，只是在ChatGPT的帮助下，完成此程序！\n图片均收集自网络AI生成图，使用的是我自己做的图片API！\n\n已实现功能：\n1.启动程序后，从API下载图片并设置为桌面壁纸\n2.每30秒下载一次图片更换壁纸\n3.更换壁纸后自动删除旧的照片\n");

        // 创建或跳过图片存储文件夹
        string pictureFolderPath = @"C:\ACDB_TEMP_PICS";
        Directory.CreateDirectory(pictureFolderPath);
        Console.WriteLine("文件夹创建成功\n");

        // 尝试清空文件夹内的旧图片
        try
        {
            DirectoryInfo directory = new DirectoryInfo(pictureFolderPath);
            foreach (FileInfo file in directory.GetFiles())
            {
                file.Delete();
            }
            Console.WriteLine("文件夹清空成功\n");
        }
        catch (Exception ex)
        {
            Console.WriteLine("An error occurred: " + ex.Message);
        }

        Console.WriteLine("程序开始干活\n");

        // 不断循环，每30秒下载并更换一次壁纸
        while (true)
        {
            // 生成随机数用于获取不同的图片
            Random random = new Random();
            int randomNumber = random.Next(1000, 9999);
            string imageUrl = "https://imgapi.160621.xyz/random.php?random=" + randomNumber;

            // 使用HttpClient下载图片
            using (HttpClient httpClient = new HttpClient())
            {
                string imageName = Path.Combine(pictureFolderPath, $"image_{randomNumber}.webp");
                HttpResponseMessage response = await httpClient.GetAsync(imageUrl);

                // 如果下载成功，则设置为桌面壁纸
                if (response.IsSuccessStatusCode)
                {
                    using (FileStream fileStream = new FileStream(imageName, FileMode.Create))
                    {
                        await response.Content.CopyToAsync(fileStream);
                    }

                    // 等待一段时间，让桌面壁纸显示出来
                    await Task.Delay(20000); 

                    // 设置桌面壁纸
                    SystemParametersInfo(0x0014, 0, imageName, 1);

                    // 等待一段时间，确保壁纸设置完成
                    await Task.Delay(10000); 

                    // 删除已设置为壁纸的图片，准备下一次更换
                    File.Delete(imageName); 
                }
            }
        }
    }
}