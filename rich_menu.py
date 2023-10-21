import requests
import json
import os
import sys
from linebot import LineBotApi, WebhookHandler

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

headers = {'Authorization':f'Bearer {channel_access_token}','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 843},   # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'Richmenu',                        # 選單名稱
    'chatBarText': 'magic',                    # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 834, 'height': 843}, # 選單位置與大小
          'action': {
              'type': 'postback', 
              'label': 'Tap area A', 
              'data' :'action=reminder'}                # 點擊後傳送文字
        },
        {
          'bounds': {'x': 835, 'y': 0, 'width': 1666, 'height': 843},
          'action': {
            #   'type': 'uri',
              'type': 'postback', 
              'label': 'Tap area B', 
            #   'uri': 'https://mc-hackathon-20231021.web.app/'}
              'data' :'action=anonymous'}
        }
    ]
  }

#刪除之前的richmenu
# richmeun = requests.request('GET', 'https://api.line.me/v2/bot/richmenu/list', headers=headers)
# for i in richmeun.json()['richmenus']:
#     requests.request('DELETE', f'https://api.line.me/v2/bot/richmenu/{i["richMenuId"]}', headers=headers)

# print(richmeun.json())
# 向指定網址發送 request
richmeun = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers, data=json.dumps(body).encode('utf-8'))
# 印出得到的結果
# print(richmeun.json())

line_bot_api = LineBotApi(channel_access_token)

with open('rich_menu.jpg', 'rb') as f:
    line_bot_api.set_rich_menu_image(richmeun.json()['richMenuId'], 'image/jpeg', f)

req = requests.request('POST', f'https://api.line.me/v2/bot/user/all/richmenu/{richmeun.json()["richMenuId"]}', headers=headers)