import time
import util.auto_wechat as wechat

import requests
import hashlib

def md5_encode(text):
    """ 把數據 md5 化 """
    if not isinstance(text, str):
        text = str(text)
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    encodedStr = md5.hexdigest().upper()
    return encodedStr

app_key = 'c7d2beeeabbfd7aa6042a6989b798d87'
userid = 250
def get_ownthink_robot(text):
    """
    思知机器人，接口地址:<https://www.ownthink.com/>
    https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken=姚明多高啊？
    :param text: 发出的消息
    :param userid: 收到的内容
    :return:
    """
    try:
        # config.init()
        # info = config.get('auto_reply_info')['txapi_conf']
        # app_key = info.get('app_key', '')
        # if not re.findall(r'^[0-9a-z]{20,}$', app_key):  # 验证 app_key 是否有效
        #     app_key = ''

        params = {
            'appid': app_key,
            'userid': md5_encode(userid),
            'spoken': text
        }
        url = 'https://api.ownthink.com/bot'
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            # print(resp.text)
            content_dict = resp.json()
            if content_dict['message'] == 'success':
                data = content_dict['data']
                if data['type'] == 5000:
                    reply_text = data['info']['text']
                    return reply_text
                else:
                    print('返回的数据不是文本数据！')
            else:
                print('思知机器人获取数据失败:{}'.format(content_dict['msg']))

        print('获取数据失败')
        return None
    except Exception as exception:
        print(str(exception))

def ownthink(msg):
    # if msg.startswith("萌萌"):
    #     wechat.send_msg(name, get_ownthink_robot(msg[2:]))
    msg = handle_msg(msg)
    wechat.send_msg(name, get_ownthink_robot(msg))

def handle_msg(msg):
    if msg.startswith("@"):
        idx = msg.find(" ")
        return msg[idx:]
    return msg
    

URL = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'

def get_qingyunke(msg):
    """
    青云客智能聊天机器人API http://api.qingyunke.com/
    :param text: str 聊天
    :param userid: str 无用
    :return: str
    """
    try:
        # print('发出消息:{}'.format(text))
        resp = requests.get(URL.format(msg))
        if resp.status_code == 200:
            # print(resp.text)
            re_data = resp.json()
            if re_data['result'] == 0:
                return_text = re_data['content']
                return return_text

            error_text = re_data['content']
            print('青云客机器人错误信息：{}'.format(error_text))

        print('青云客机器人获取失败')
    except Exception as exception:
        print(str(exception))
        print('青云客机器人获取失败')

def qingyunke(msg):
    msg = handle_msg(msg)
    if msg.startswith("一狗"):
        wechat.send_msg(name, get_qingyunke(msg[2:]))

def copy(msg):
    wechat.send_msg(name, msg)

# 2. 根据信息做出相应
def process_msg(msg):
    global mode
    if msg.startswith("#"):
        mode = msg
    else:
        try:
            {
                "#copy": copy,
                "#qingyunke": qingyunke,
                "#ownthink": ownthink
            }[mode](msg)
        except KeyError:
            copy(msg)


if __name__ == '__main__':

    wechat_path = "D:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe"
    wechat = wechat.WeChat(wechat_path)

    last_msg = "聊天机器人(二狗)上线"
    names = ["凤凰城洗浴中心", "❤游戏界躺平乐享感恩群❤"]
    name = "凤凰城洗浴中心"
    # name = "❤游戏界躺平乐享感恩群❤"
    name = "武汉游戏联盟"
    name = "老吴培训"
    name = "524，"
    # name = "伊万"
    name = "超越"
    name = "文件传输助手"
    # copy(last_msg)
    mode = "#ownthink"

    MaxCD = 10
    MinCD = 0.1
    CD = 0.1
    
    # 1. 监听群信息
    while True:
        # for name in names:
        cur_msg = wechat.get_msg(name)
        # cur_msg = wechat.get_other_msg(name)
        process_msg(cur_msg)
        # if cur_msg == last_msg:
        #     CD *= 2
        #     if CD > MaxCD:
        #         CD = MaxCD
        # else:
        #     last_msg = cur_msg
        #     process_msg(cur_msg)
        #     CD = MinCD
        
        time.sleep(CD)
        

    