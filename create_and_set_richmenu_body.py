import requests
import json

from linebot import (
    LineBotApi, WebhookHandler
)
line_bot_api = LineBotApi('dboqjKgzCLFQW8aAhN+ubZv0v78pdRXQ5fpSbXkPG/bzL9j15xW6RRJBibVuAtibU4amiYjYvTj3I4nxrNR+qrx4TARQ8zhkzpYJFq0r3EPt1cU0OBmO0F5gen1+uGXjqL6jrIfBl54GLe9ByH7zSQdB04t89/1O/w1cDnyilFU=')
headers = {"Authorization":"Bearer dboqjKgzCLFQW8aAhN+ubZv0v78pdRXQ5fpSbXkPG/bzL9j15xW6RRJBibVuAtibU4amiYjYvTj3I4nxrNR+qrx4TARQ8zhkzpYJFq0r3EPt1cU0OBmO0F5gen1+uGXjqL6jrIfBl54GLe9ByH7zSQdB04t89/1O/w1cDnyilFU=",
    "Content-Type":"application/json"}

body = {
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": 'true',
  "name": "richmenu0324",
  "chatBarText": "操作選單",
  "areas": [
    {
      "bounds": {
        "x": 0,
        "y": 0,
        "width": 830,
        "height": 840
      },
      "action": {
        "type": "message",
        "text": "預約訂位"
      }
    },
    {
      "bounds": {
        "x": 831,
        "y": 0,
        "width": 830,
        "height": 844
      },
      "action": {
        "type": "message",
        "text": "訂位管理"
      }
    },
    {
      "bounds": {
        "x": 1661,
        "y": 0,
        "width": 839,
        "height": 848
      },
      "action": {
        "type": "message",
        "text": "店內點餐"
      }
    },
    {
      "bounds": {
        "x": 0,
        "y": 835,
        "width": 831,
        "height": 851
      },
      "action": {
        "type": "message",
        "text": "當日外帶"
      }
    }
  ]
}
# step1 設定好按鈕json,POST取得richmenu Id
#req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/', headers=headers,data=json.dumps(body).encode('utf-8'))
#print(req.text)

# step2 設定richmenu的圖片, 無回傳東西代表成功
#with open('../LineBot_Restaurant_Server/menu/client_icon/Client_rm0324.jpg', 'rb') as rm:
#  line_bot_api.set_rich_menu_image('richmenu-4828bcd271ca7e91777c32aca57fcf75', 'image/jpeg', rm)

# step3 啟用richmenu, 成功的話會回傳{}, 之後看 https://medium.com/front-end-augustus-study-notes/line-bot-rich-menu-aa5fa67ac6ae, 用postman正式啟用
#req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-4828bcd271ca7e91777c32aca57fcf75', 
#                       headers=headers)
#print(req.text)

# check全部的richmenu, 一個token最多1000個
#rich_menu_list = line_bot_api.get_rich_menu_list()
#for rich_menu in rich_menu_list:
#    print(rich_menu.rich_menu_id)

# 刪除不要的richmenu
#line_bot_api.delete_rich_menu('richmenu-6a740f5e73525c3cd511fa71d2cf046b')