#!/usr/bin/env python
import requests
import os
import random
import time
import hmac
import hashlib
import base64
import urllib.parse

# 从环境变量获取敏感信息 - 添加详细检查
webhook_url = os.getenv('DINGTALK_WEBHOOK_URL', '').strip()
secret = os.getenv('DINGTALK_SECRET', '').strip()

# 添加详细的错误检查
if not webhook_url or not secret:
    print("错误：环境变量未正确设置！")
    print(f"WEBHOOK_URL: {'已设置' if webhook_url else '未设置'}")
    print(f"SECRET: {'已设置' if secret else '未设置'}")
    sys.exit(1)

# 验证URL格式
if "access_token=" not in webhook_url:
    print(f"错误：Webhook URL格式不正确！URL: {webhook_url[:50]}...")
    sys.exit(1)
    
safety_messages = [
    "野泳一时爽，危险藏身旁。去泳池记得结伴而行，安全第一！",
    "暑假玩水要小心！水库、野塘别靠近，正规泳池才安心。溺水事故多，别让青春变传说！",
    "重要提醒：发现小伙伴落水，别逞英雄跳下去！大喊呼救+找大人+抛漂浮物，三步救命法记心里！",
    "防溺水口诀：游泳去场馆，野水不能沾。同伴若落水，呼救莫拖延！",
    "提醒：自然水域暗流多，水性再好也翻车！",
    "溺水自救技能get：突然抽筋别慌张，仰面漂浮省力气，挥手呼救等人帮！",
    "危险水域黑名单：废弃矿坑＞水库闸口＞野河急流＞涨水河滩＞海边离岸流！见到请绕道！",
    "看到'水深危险'牌子别叛逆！那是用生命换来的警告，耍帅不如保命重要！",
    "警惕'安静溺水'：同伴游泳时突然安静/眼神呆滞，立即问'你还好吗？'",
    "水上安全冷知识：人溺水时无法挥手呼救！看到有人垂直漂浮快喊救援！",
    "游泳后不适别大意！咳嗽/呼吸困难可能是'干性溺水'，速去医院别拖延！",
    "河边自拍风险高！湿滑石头易落水，美景诚可贵，生命价更高！",
    "游泳比赛安全规则：①不推人下水 ②不潜水恶作剧 ③体力不支立刻停！",
    "看似平静的积水潭，可能是3米深坑！绕行！绕行！绕行！",
    "溺水误区纠正：'会游泳≠安全'！抽筋、暗流、水草都可能要命！",
    "同学互保计划：游泳时结'安全对子'，每10分钟确认对方状态！",
    "玩水遇险用这招：挥舞手臂交叉摆动（国际溺水求救信号）",
    "海边游玩必修课：识别离岸流（白色浪花间断区），遇险平行岸边游！",
    "溺水数据触目惊心：青少年占事故60%！别让自己成为统计数字！"
]

def send_dingtalk_message(content, at_all=False):
    headers = {"Content-Type": "application/json"}
    
    # 生成签名
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = f"{timestamp}\n{secret}"
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    full_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"

    # 构建消息体
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "安全提醒",
            "text": content
        },
        "at": {
            "isAtAll": at_all
        }
    }

    response = requests.post(full_url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    # 检查环境变量是否设置
    if not webhook_url or not secret:
        print("错误：未设置钉钉机器人环境变量！")
        exit(1)
        
    # 随机选择一条防溺水提示
    daily_message = random.choice(safety_messages)
    formatted_date = time.strftime("%m月%d日")
    
    # 使用Markdown格式高亮显示@所有人
    final_message = f"**<font color='#FFFFFF'><b>### ⚠ {formatted_date}安全提醒\n</b></font>**\n\n" \
                    f"{daily_message}"
    
    print(f"准备发送消息: {final_message}")
    result = send_dingtalk_message(final_message, at_all=True)
    print(f"发送状态: {result}")
