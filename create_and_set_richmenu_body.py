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
  "name": "richmenu0116",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 0,
        "y": 0,
        "width": 831,
        "height": 839
      },
      "action": {
        "type": "message",
        "text": "訂位查詢"
      }
    },
    {
      "bounds": {
        "x": 839,
        "y": 0,
        "width": 831,
        "height": 839
      },
      "action": {
        "type": "message",
        "text": "菜單查詢"
      }
    },
    {
      "bounds": {
        "x": 1673,
        "y": 0,
        "width": 827,
        "height": 843
      },
      "action": {
        "type": "message",
        "text": "會員資訊"
      }
    },
    {
      "bounds": {
        "x": 0,
        "y": 847,
        "width": 831,
        "height": 839
      },
      "action": {
        "type": "message",
        "text": "店家資訊"
      }
    },
    {
      "bounds": {
        "x": 835,
        "y": 843,
        "width": 825,
        "height": 843
      },
      "action": {
        "type": "message",
        "text": "店家導航"
      }
    },
    {
      "bounds": {
        "x": 1666,
        "y": 843,
        "width": 834,
        "height": 843
      },
      "action": {
        "type": "message",
        "text": "意見回饋"
      }
    }
  ]
}
# step1 設定好按鈕json,POST取得richmenu Id
#req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/', headers=headers,data=json.dumps(body).encode('utf-8'))
#print(req.text)

# step2 設定richmenu的圖片, 無回傳東西代表成功
#with open('../LineBot_Restaurant_Server/menu/client_icon/Client_rm0116.jpg', 'rb') as rm:
#  line_bot_api.set_rich_menu_image('richmenu-6a740f5e73525c3cd511fa71d2cf046b', 'image/jpeg', rm)

# step3 啟用richmenu, 成功的話會回傳{}, 之後看 https://medium.com/front-end-augustus-study-notes/line-bot-rich-menu-aa5fa67ac6ae, 用postman正式啟用
#req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-6a740f5e73525c3cd511fa71d2cf046b', 
#                       headers=headers)
#print(req.text)

# check全部的richmenu, 一個token最多1000個
#rich_menu_list = line_bot_api.get_rich_menu_list()
#for rich_menu in rich_menu_list:
#    print(rich_menu.rich_menu_id)

# 刪除不要的richmenu
#line_bot_api.delete_rich_menu('richmenu-1099e17c3dcc9fb2ac6b8407cbbac918')