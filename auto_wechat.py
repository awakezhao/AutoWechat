import time
import win32con, win32api
import win32clipboard as w
import uiautomation as auto
import subprocess
import numpy as np
import pyperclip
# import virtkey
import time
import pyautogui, time, sys
import pyperclip


from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMimeData, QUrl

# # pip install pillow, 用Image模块操作图片文件
from PIL import Image
# # BytesIO是操作二进制数据的模块
from io import BytesIO

###########################################################################################################################
Delay = 0.2

# 调用win32api的模拟点击功能实现ctrl+v粘贴快捷键
def ctrlV():
    win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
    win32api.keybd_event(86,0,0,0)  #v键位码是86
    time.sleep(Delay)
    win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)

def click(element):
    x, y = element.GetPosition()
    auto.Click(x, y)


class WeChat():
    def __init__(self, path):
        # 微信打开路径
        self.path = path

        # 用于复制内容到剪切板
        self.app = QApplication([])
    
    # 打开微信客户端
    def open_wechat(self):
        subprocess.Popen(self.path)

    # 搜寻微信客户端控件
    def get_wechat(self):
        return auto.WindowControl(searchDepth=1, Name="微信")

    # 进入指定用户窗口
    def get_contact(self, name):
        self.open_wechat()
        wechat = self.get_wechat()

        search_box = wechat.EditControl(searchDepth=8, Name="搜索")
        click(search_box)

        pyperclip.copy(name)
        ctrlV()
        # 等待客户端搜索联系人
        # search_box.SendKeys(name, interval=0.1)
        search_box.SendKeys("{enter}")

        return search_box

    # 搜索指定用户名的联系人发送信息
    def send_msg(self, name, text):
        window = self.get_contact(name)
        pyperclip.copy(text)
        ctrlV()
        window.SendKeys("{enter}")
    
    # 搜索指定用户名的联系人发送文件
    def send_file(self, name, path):
        # 粘贴文件发送给用户
        window = self.get_contact(name)
        # 将文件复制到剪切板
        file = QMimeData()
        url = QUrl.fromLocalFile(path)
        file.setUrls([url])
        self.app.clipboard().setMimeData(file)

        # 暂停等待文件复制到剪切板
        time.sleep(0.5)
        ctrlV()
        window.SendKeys("{enter}")

    def send_image(self, name, path):
        window = self.get_contact(name)
        self.paste_img(path)

        # 暂停等待文件复制到剪切板
        time.sleep(0.5)
        ctrlV()
        window.SendKeys("{enter}")

    def send_msg_to_clip(self, type_data, msg):
        """
        操作剪贴板分四步：
        1. 打开剪贴板：OpenClipboard()
        2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
        3. 往剪贴板写入数据：SetClipboardData()
        4. 关闭剪贴板：CloseClipboard()

        :param type_data: 数据的格式，
        unicode字符通常是传 win32con.CF_UNICODETEXT
        :param msg: 要写入剪贴板的数据
        """
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(type_data, msg)
        w.CloseClipboard()

    def paste_img(self, file_img):
        """
        图片转换成二进制字符串，然后以位图的格式写入剪贴板

        主要思路是用Image模块打开图片，
        用BytesIO存储图片转换之后的二进制字符串

        :param file_img: 图片的路径
        """
        # 把图片写入image变量中
        # 用open函数处理后，图像对象的模式都是 RGB
        image = Image.open(file_img)

        # 声明output字节对象
        output = BytesIO()

        # 用BMP (Bitmap) 格式存储
        # 这里是位图，然后用output字节对象来存储
        image.save(output, 'BMP')

        # BMP图片有14字节的header，需要额外去除
        data = output.getvalue()[14:]

        # 关闭
        output.close()

        # DIB: 设备无关位图(device-independent bitmap)，名如其意
        # BMP的图片有时也会以.DIB和.RLE作扩展名
        # 设置好剪贴板的数据格式，再传入对应格式的数据，才能正确向剪贴板写入数据
        self.send_msg_to_clip(w.CF_DIB, data)
        

    # 获取所有通讯录中所有联系人
    def find_all_contacts(self):
        pass


if __name__ == '__main__':
    wechat = WeChat("aaa")
    print("hello python")