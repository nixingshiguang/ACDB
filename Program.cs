using System;
using System.IO;
using System.Net;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    private static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);

    static void Main(string[] args)
    {
        //输出初始内容
        Console.WriteLine("！！！提示！！！\n此程序为满足我突然的需求制作，本人并不会C#语言，只是在ChatGPT的帮助下，完成此程序！\n图片均收集自网络AI生成图，使用的是我自己做的图片API！\n已实现功能：\n1.启动程序后，从API下载图片并设置为桌面壁纸\n2.每30秒下载一次图片更换壁纸\n3.更换壁纸后自动删除旧的照片\n");

        //设置文件保存路径
        string pictureFolderPath = @"C:\ACDB_TEMP_PICS";

        //创建文件夹
        Directory.CreateDirectory(pictureFolderPath);
        Console.WriteLine("文件夹创建成功\n");

        //清空文件夹
        try
        {
            DirectoryInfo directory = new DirectoryInfo(pictureFolderPath);

            // 删除目录中的所有文件
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

        //自动下载照片并设置为壁纸一直循环
        while (true)
        {
            // 生成随机数作为查询字符串
            Random random = new Random();
            int randomNumber = random.Next(1000, 9999);

            // 构建带随机数的图片链接
            string imageUrl = "https://imgapi.160621.xyz/random.php?random=" + randomNumber;

            // 发送 HTTP 请求获取图片
            using (WebClient webClient = new WebClient())
            {
                string imageName = Path.Combine(pictureFolderPath, $"image_{randomNumber}.jpg");
                webClient.DownloadFile(imageUrl, imageName);

                // 等待10秒
                Thread.Sleep(10000);

                // 设置桌面背景
                SystemParametersInfo(0x0014, 0, imageName, 1);

                // 等待10秒
                Thread.Sleep(10000);

                // 删除旧图片
                File.Delete(imageName);

                // 等待10秒
                Thread.Sleep(10000);
            };
        }
    }
}
