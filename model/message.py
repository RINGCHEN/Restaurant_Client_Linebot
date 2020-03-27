from datetime import datetime, timedelta
from linebot.models import (
    ImageSendMessage, FlexSendMessage, StickerSendMessage, TextSendMessage
)
from App_Config import Firebase_JsonPath, Restaurant_Name
''' firebase setting'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(Firebase_JsonPath)
firedb = firestore.client()
''' firebase setting end '''


class AllMessage():
    
    @staticmethod
    def Confirm_PostMessage(data, number):
        # 取消step2
        if number == 1:
            ConfirmMessage = FlexSendMessage(
                alt_text = '菜單查詢',
                position = 'absolute',
                contents = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "確定取消嗎?",
                                "margin": "md"
                            },
                            {
                                "type": "spacer"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"是的",
                                    "data": data
                                },
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"再想想好了",
                                    "data":"no"
                                },
                                "height": "sm"
                            }
                        ],
                        "flex": 0
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )
            
        # 確認是否答應 訂位Step6
        elif number == 2:
            print(data)
            ConfirmMessage = FlexSendMessage(
                alt_text = '確定此次訂位資訊嗎?\n姓名: ' + data[0] + '\n預約日期: ' + data[1].split('T')[0] + '\n預約時間: ' + data[1].split('T')[1] + "\n預約人數: " + data[2], #+ "\n選擇位置: " + data[4],
                position = 'absolute',
                contents = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": '確定此次訂位資訊嗎?\n姓名: ' + data[0] + '\n預約日期: ' + data[1].split('T')[0] + '\n預約時間: ' + data[1].split('T')[1] + "\n預約人數: " + data[2], #+ "\n選擇位置: " + data[4],
                                "margin": "md",
                                "wrap": True
                            },
                            {
                                "type": "spacer"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"訂單正確",
                                    "data": 'yes '+ data[0] + " " + data[1] + " " + data[2] + " " + data[3]
                                },
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"取消訂單",
                                    "data":'no ' + data[0] + " " + data[1] + " " + data[2] + " " + data[3]  # 3: UserId
                                },
                                "height": "sm"
                            }
                        ],
                        "flex": 0
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )
        
        # 確認是先生或小姐 訂位step2
        elif number == 3:
            ConfirmMessage = FlexSendMessage(
                alt_text = '請問是{0}先生還是{0}小姐呢?'.format(data[0]),
                position = 'absolute',
                contents = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": '請問是{0}先生還是{0}小姐呢?'.format(data[0]),
                                "margin": "md",
                                "wrap": True
                            },
                            {
                                "type": "spacer"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"先生",
                                    "data": '先生'
                                },
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"小姐",
                                    "data":'小姐'
                                },
                                "height": "sm"
                            }
                        ],
                        "flex": 0
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )
        
        elif number == 4:
            ConfirmMessage = FlexSendMessage(
                alt_text = '請問是要預約訂位還是取消預約呢?',
                position = 'absolute',
                contents = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": '請問是要預約訂位還是取消預約呢?',
                                "margin": "md",
                                "wrap": True
                            },
                            {
                                "type": "spacer"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type":"message",
                                    "label":"預約訂位",
                                    "text": '預約訂位'
                                },
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type":"message",
                                    "label":"取消預約",
                                    "text":'取消預約'
                                },
                                "height": "sm"
                            }
                        ],
                        "flex": 0
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )

        # 確認日期 訂位step3.5
        elif number == 5:
            print(data)
            ConfirmMessage = FlexSendMessage(
                alt_text = '確定此次日期資訊嗎?',
                position = 'absolute',
                contents = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": '確定此次日期資訊嗎?\n預約日期: ' + data.split('T')[0] + '\n預約時間: ' + data.split('T')[1],
                                "margin": "md",
                                "wrap": True
                            },
                            {
                                "type": "spacer"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"日期正確",
                                    "data": 'yes '+ data
                                },
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"重新選取",
                                    "data":'no ' + data
                                },
                                "height": "sm"
                            }
                        ],
                        "flex": 0
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )

        # 確認訂餐資訊
        elif number == 6:
            print(data)
            reply_message = '以下是您的訂餐詳細\n' 
            postmessage = ''
            for i in list(data.keys()):
                if data[i] != 0:
                    postmessage = postmessage + i + ' ' + str(data[i]) + " "
                    reply_message = reply_message + i + ' ' + str(data[i]) + "份\n"
            reply_message = reply_message + '確認無誤嗎?'
            ConfirmMessage = FlexSendMessage(
                alt_text = '餐點確認無誤嗎?',
                position = 'absolute',
                contents = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": reply_message,
                                "margin": "md",
                                "wrap": True
                            },
                            {
                                "type": "spacer"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"訂單正確",
                                    "data": 'yes menu ' + postmessage
                                },
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type":"postback",
                                    "label":"我要修改",
                                    "data":'no menu '
                                },
                                "height": "sm"
                            }
                        ],
                        "flex": 0
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )

        return ConfirmMessage
    
    @staticmethod
    def Img_Message(number):
        # 瑋瑋感謝你
        if number == 1:
            ImgMessage = ImageSendMessage( original_content_url='https://i.imgur.com/ZSsqBqW.jpg', preview_image_url = 'https://i.imgur.com/ZSsqBqW.jpg' )
        # 菜單1
        elif number == 2:
            ImgMessage = ImageSendMessage( original_content_url='https://i.imgur.com/r0NpeFD.jpg', preview_image_url = 'https://i.imgur.com/r0NpeFD.jpg' )
        # 菜單2
        elif number == 3:
            ImgMessage = ImageSendMessage( original_content_url='https://i.imgur.com/SuOPgeC.jpg', preview_image_url = 'https://i.imgur.com/SuOPgeC.jpg' )
        # 菜單3
        elif number == 4:
            ImgMessage = ImageSendMessage( original_content_url='https://i.imgur.com/C8JaNlT.jpg', preview_image_url = 'https://i.imgur.com/C8JaNlT.jpg' )
        # 座位照
        elif number == 5:
            ImgMessage = ImageSendMessage( original_content_url='https://i.imgur.com/uFoQLFA.jpg', preview_image_url = 'https://i.imgur.com/uFoQLFA.jpg' )
        return ImgMessage

    @staticmethod
    def Time_Message(number):
        # 選日期
        ntime = datetime.now()
        mtime = ntime + timedelta(days = 30)
        if number == 1:
            if len(str(ntime.month)) == 1:
                month = '0'+str(ntime.month)
            else:
                month = str(ntime.month)
            if len(str(ntime.day)) == 1:
                day = '0'+str(ntime.day)
            else:
                day = str(ntime.day)
            nowtime = str(ntime.year) + '-' + month + '-' + day + "T11:30" # 舊版
            if len(str(mtime.month)) == 1:
                month = '0'+str(mtime.month)
            else:
                month = str(mtime.month)
            if len(str(mtime.day)) == 1:
                day = '0'+str(mtime.day)
            else:
                day = str(mtime.day)
            maxtime = str(mtime.year) + '-' + month + '-' + day + "T19:50"
            #print(nowtime)
            TimeMessage = FlexSendMessage(
                alt_text='選時間',
                position = 'absolute',
                contents={
                    'type': 'bubble', 'direction': 'ltr',
                    'hero': {
                        'type': 'image',
                        'url': 'https://i.imgur.com/1sVGKkq.jpg',
                        'size': 'full',
                        'action': { 
                            "type":"datetimepicker",
                            "label":"select time", # 方便用post接收資料
                            "data":"selected time",
                            "mode":"datetime",
                            "initial":nowtime, # format: date
                            "max":maxtime,
                            "min":nowtime
                        }
                    }
                }
            )
        elif number == 2:
            '''
            if len(str(ntime.minute)) == 1:
                minute = '0'+str(ntime.minute)
            else:
                minute = str(ntime.minute)
            if len(str(ntime.hour)) == 1:
                hour = '0'+str(ntime.hour)
            else:
                hour = str(ntime.hour)
            nowtime = hour + ':' + minute
            #print(nowtime)'''
            TimeMessage = FlexSendMessage(
                alt_text='選時間',
                position = 'absolute',
                contents={
                    'type': 'bubble', 'direction': 'ltr',
                    'hero': {
                        'type': 'image',
                        'url': 'https://i.imgur.com/Cp3nmkw.jpg',
                        'size': 'full',
                        'action': { 
                            "type":"datetimepicker",
                            "label":"select time", # 方便用post接收資料
                            "data":"selected time",
                            "mode":"time", # format: time
                            "initial":'11:30',
                            "min": '11:30',
                            "max": '19:50'
                        }
                    }
                }
            )
        return TimeMessage

    @staticmethod
    def Sticker_Message(number):
        # 哭哭貼圖
        if number == 1:
            StickerMessage = StickerSendMessage(package_id='11538', sticker_id='51626522')
        elif number == 2:
            StickerMessage = StickerSendMessage(package_id='11539', sticker_id='52114113')
        return StickerMessage

    @staticmethod
    def Cancel_Message(UserId):
        firebase_rec = {}
        doc_ref = firedb.collection('訂位紀錄').document(UserId)
        doc = doc_ref.get().to_dict()
        if doc == None: # 無過往紀錄
            reply_message = [TextSendMessage(text='目前沒有訂位紀錄!!'), TextSendMessage(text='如需要訂位,麻煩按下訂位查詢喔~')]
        else:
            reply_message = []
            reply_data = []
            for k, v in doc.items():
                try:
                    if datetime.strptime(v[1], '%Y-%m-%dT%H:%M') < (datetime.now() - timedelta(minutes=30)):
                        pass
                    else:
                        reply_message.append(v[0])
                        reply_message.append(v[1].replace('T',' '))
                        reply_message.append(v[2])
                        reply_message.append(v[4])
                        reply_data.append(k)
                except:
                    pass
        
        if len(reply_message) == 0:
            reply_message = [TextSendMessage(text='目前沒有訂位紀錄!!'), TextSendMessage(text='如需要訂位,麻煩按下預約訂位喔~')]
        else:
            doc_ref = firedb.collection('是否訂位').document(UserId)
            firebase_rec['step'] = 'C1'
            firebase_rec['status'] = 'cancel'
            doc_ref.update(firebase_rec)

            Contents = []
            for t in range(0, len(reply_message), 4):
                Contents.append(
                    {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "姓名: " + reply_message[t] + "\n訂位時間: " + reply_message[t+1] + "\n人數: " + reply_message[t+2] + "\n訂單編號: " + reply_message[t+3],
                                    "margin": "md",
                                    "wrap": True
                                },
                                {
                                    "type": "button",
                                    "action":{
                                        "type":"postback",
                                        "label": "取消此次訂位",
                                        "data": reply_data[(t//4)]
                                    },
                                    "margin": "md",
                                    "weight": "bold",
                                    "align": "center"
                                }
                            ]
                        },
                        "styles": { "footer": { "separator": True } }
                    }
                )
                if t == 15: break # 最多長度為15
            reply_message = [TextSendMessage(text='僅顯示15筆訂單'),FlexSendMessage(
                alt_text = '取消訂位中',
                position = 'absolute',
                contents = {
                    "type": "carousel",
                    "contents": Contents
                }
            )]
            
        return reply_message

    @staticmethod
    def Use_Several_Times_Message(number, UserId, UserMessage):
        firebase_rec = {}
        if number == 1:
            doc_ref = firedb.collection('訂位紀錄').document(UserId)
            doc = doc_ref.get().to_dict()
            if doc == None: # 無過往紀錄
                reply_message = [TextSendMessage(text='目前沒有訂位紀錄!!'), TextSendMessage(text='如需要訂位,麻煩按下預約訂位喔~')] 
            else:
                reply_message = '目前有以下訂位紀錄:'
                for k, v in doc.items():
                    try:
                        if datetime.strptime(v[1], '%Y-%m-%dT%H:%M') < datetime.now():
                            pass
                        else:
                            reply_message += '\n\n姓名: ' + v[0] + '\n預約時間: ' + v[1].replace('T',' ') + "\n人數: " + v[2]
                    except:
                        pass         
        elif number == 2:
            doc_ref = firedb.collection('是否訂位').document(UserId)
            doc = doc_ref.get()
            if doc.to_dict() == None: # 無過往紀錄
                firebase_rec['status'] = 'order'
                firebase_rec['step'] = '1'
                doc_ref = firedb.collection('是否訂位').document(UserId)
                doc_ref.set(firebase_rec)

                stickermessage = AllMessage.Sticker_Message(number = 2)
                reply_message = [stickermessage, TextSendMessage(text='開始訂位!!'), TextSendMessage(text='請問貴姓?')] # 接續訂位step3
        elif number == 3:
            doc_ref = firedb.collection('是否訂位').document(UserId)
            doc = doc_ref.get()
            if '訂位' in UserMessage and doc.to_dict()['status'] == 'free': # 如果有關鍵字以及status為order
                firebase_rec['status'] = 'order'
                firebase_rec['step'] = '1'
                doc_ref = firedb.collection('是否訂位').document(UserId)
                doc_ref.update(firebase_rec)

                stickermessage = AllMessage.Sticker_Message(number = 2)
                reply_message = [stickermessage, TextSendMessage(text='開始訂位!!'), TextSendMessage(text='請問貴姓?')] # 接續訂位step3
        
        return reply_message
    
    @staticmethod
    def Menu_Message():
        Contents = []
        Menus = []
        Menus.append('https://i.imgur.com/ZSsqBqW.jpg 精緻簡餐 (本店週六、日用餐消費加收一成服務費，若有加贈甜點已美餐60分，送完為止。)\n附餐有:(熱)咖啡、紅茶、綠茶、柚子茶、巧克力、甜湯、綠茶、冰綠茶、咖啡、紅茶、奶茶、檸檬汁、蔓越莓冰醋 >>右滑看菜單>>')
        Menus.append('https://i.imgur.com/SBDmHrJ.jpg 芒果炒雞柳 -詳細介紹- NT$300')
        Menus.append('https://i.imgur.com/JCBXVEq.jpg 東坡肉 -詳細介紹- NT$310')
        Menus.append('https://i.imgur.com/gGhxvM6.jpg 嫩煎牛排 -詳細介紹- NT$320')
        Menus.append('https://i.imgur.com/MhAb8nA.jpg 蒜泥白玉蒸蝦 -詳細介紹- NT$330')
        Menus.append('https://i.imgur.com/JZssJkM.jpg 蒜苗炒松阪牛 -詳細介紹- NT$340')
        Menus.append('https://i.imgur.com/HJr3SU5.jpg 橙汁魚排 外銷日本潮鯛魚排輕裹粉煎酥佐以橙汁醬\n略帶酸甜口味開會美味好滋味 NT$290')
        for M in range(len(Menus)):
            Mlist = Menus[M].split(" ")
            if M == 0:
                Contents.append(
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": Mlist[0], # img 網址
                            "size": "full",
                            "aspectRatio": "10:9",
                            "aspectMode": "cover",
                            "backgroundColor": "#FFFFFF"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": Mlist[1],
                                    "weight": "bold",
                                    "size": "xl",
                                    "margin": "md",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": Mlist[2],
                                    "margin": "md",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": Mlist[3],
                                    "margin": "md",
                                    "weight": "bold",
                                    "align": "center",
                                    "wrap": True
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "spacer",
                                    "size": "xxl"
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#905c44",
                                    "action": 
                                    {
                                        "type": "postback",
                                        "label": "確定訂單",
                                        "data": "confirm"
                                    }
                                }
                            ]
                        }
                    }
                )
            else:
                Contents.append(
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": Mlist[0], # img 網址
                            "size": "full",
                            "aspectRatio": "10:9",
                            "aspectMode": "cover",
                            "backgroundColor": "#FFFFFF"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": Mlist[1],
                                    "weight": "bold",
                                    "size": "xl",
                                    "margin": "md",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": Mlist[2],
                                    "margin": "md",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": Mlist[3],
                                    "size": "md",
                                    "flex": 0
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "button", 
                                    "style": "primary",
                                    "cornerRadius": "75px",
                                    "color": "#905c44",
                                    "action": {
                                        "type":"postback",
                                        "label":"+",
                                        "data": '加 ' + Mlist[1]
                                    },
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#905c44",
                                    "cornerRadius": "100px",
                                    "action": {
                                        "type":"postback",
                                        "label":"-",
                                        "data":'減 ' + Mlist[1]
                                    },
                                    "height": "sm"
                                }
                            ],
                            "flex": 0
                        }
                    }
                )
        MenuMessage = FlexSendMessage(
            alt_text = '菜單查詢',
            position = 'absolute',
            contents = {
                "type": "carousel",
                "contents": Contents
            }
        )

        return MenuMessage

    @staticmethod
    def Navigate_Message():
        # 店家導航
        NavigateMessage =  FlexSendMessage(
            alt_text='店家導航',
            position = 'absolute',
            contents={
                'type': 'bubble', 'direction': 'ltr',
                'body':{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "注意!!請確認已下載Google Map再點選開始導航按鈕",
                            "size": "md",
                            "wrap": True,
                            "align": "center",
                            "margin": "md",
                            "color": "#905c44"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "action": {
                                "type": "uri",
                                "label": "開始導航",
                                "uri": "https://www.google.com/maps/dir/?api=1&destination=" + Restaurant_Name + "%2C"
                            },
                            "height": "sm"
                        }
                    ]
                }
            }
        )

        return NavigateMessage

    @staticmethod
    def Information_Message():
        # 店家資訊
        InformationMessage =  FlexSendMessage(
            alt_text='店家資訊',
            position = 'absolute',
            contents={
                'type': 'bubble', 'direction': 'ltr',
                'body':{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "action": {
                                "type": "uri",
                                "label": "店家資訊",
                                "uri": "line://app/1653717095-PowbzG8x"
                            },
                            "height": "sm"
                        }
                    ]
                }
            }
        )

        return InformationMessage

    @staticmethod
    def Choose_Seat_Message(dict_doc):
        Contents = []
        Seats = ['A桌(2人)', 'B桌(2人)', 'C桌(4人)', 'D桌(4人)', 'E桌(4人)', 'F桌(4人)', 'G桌(4人)', 'H桌(4人)', 'I桌(6人)', 'J桌(6人)']
        if (int)(dict_doc['Num_People']) <= 2:
            Seats = Seats[0:3]
        elif 2 < (int)(dict_doc['Num_People']) <= 4:
            Seats = Seats[2:8]
        elif 4 < (int)(dict_doc['Num_People']):
            Seats = Seats[-2:]
        elif int(dict_doc['Num_People']) > 6:
            ChooseSeatMessage = TextSendMessage(text = '因人數較多，麻煩您打電話至店裡，由店內人員幫您安排座位，感謝您!')
            return ChooseSeatMessage
        # 取得順位
        doc_ref = firedb.collection_group('訂位紀錄')
        docs = doc_ref.stream() # generator
        # 1個ID(collection)算一次迴圈
        for doc in docs:
            for d in doc.to_dict(): # for each in dict
                try:# 如果他訂的時間一小時內沒有人的話開放位置, 有的話就不開放      
                    selected_time = datetime.strptime(dict_doc['selected_time'], '%Y-%m-%dT%H:%M')
                    selected_time_plus = datetime.strptime(dict_doc['selected_time'], '%Y-%m-%dT%H:%M') + timedelta(hours = 1)
                    other_selected_time = datetime.strptime(doc.to_dict()[d][1], '%Y-%m-%dT%H:%M')
                    if selected_time <= other_selected_time and selected_time_plus >= other_selected_time: 
                        Seats.remove(doc.to_dict()[d][3])
                    else:
                        pass
                except:
                    pass
        
        for M in range(len(Seats)):
            Contents.append(
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#905c44",
                                "action": {
                                    "type": "postback",
                                    "label": Seats[M],
                                    "data": Seats[M]
                                },
                                "height": "sm"
                            }
                        ]
                    },
                    "styles": { "footer": { "separator": True } }
                }
            )
        ChooseSeatMessage = FlexSendMessage(
            alt_text = '選擇座位',
            position = 'absolute',
            contents = {
                "type": "carousel",
                "contents": Contents
            }
        )

        return ChooseSeatMessage
