''' 此為客戶端 '''
'''
    4大button功能
    1. 訂位預約
    2. 訂位管理
    3. 店內點餐
    4. 當日外帶
    訂餐步驟: 按下linebot的訂餐時，會先要求客人掃桌面上的QRcode，QRcode中有金鑰及桌號，會比對金鑰及桌號後，才可開始點餐
    當日外帶: 客人選完時間之後，會比對時間自動將時間轉換成30分或整點，並提前半小時通知(使用定時系統)
'''
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, FollowEvent, UnfollowEvent,
    TextMessage, ImageMessage, TextSendMessage, ImageSendMessage, 
    FlexSendMessage, StickerSendMessage
)

app = Flask(__name__)

from App_Config import (
    serverId, Firebase_JsonPath, 
    LineBot_Token, LineBot_Secret, Server_LineBot_Token, Server_LineBot_Online_Token, 
    Richmenu_Client_Id, Restaurant_Name
)

line_bot_api_server = LineBotApi(Server_LineBot_Online_Token)
line_bot_api = LineBotApi(LineBot_Token)
handler = WebhookHandler(LineBot_Secret)

''' firebase setting'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(Firebase_JsonPath)
firebase_admin.initialize_app(cred)
firedb = firestore.client()
''' firebase setting end '''

import re
from datetime import datetime
import cv2 # 限定ngrok才能用
from pyzbar import pyzbar

# import Message template from ./model/message.py(for use reply message)
from model.message import AllMessage
#from model.menu import Menus


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(PostbackEvent)
def handle_postback(event):
    UserId = event.source.user_id
    ert = event.reply_token
    firebase_rec = {}
    data = event.postback.data
    doc_ref = firedb.collection('是否訂位').document(UserId)
    doc = doc_ref.get()
    print(event.postback)

    ''' 訂位功能step3 '''
    if doc.to_dict()['status'] == 'order' and doc.to_dict()['step'] == '2':
        firebase_rec['step'] = '3'
        firebase_rec['Name'] = doc.to_dict()['Name'] + event.postback.data
        doc_ref.update(firebase_rec)
        TimeMessage = AllMessage.Time_Message(number = 1)
        line_bot_api.reply_message(ert, TimeMessage) # 傳送選擇日期的Message
        return 0

    ''' 訂位功能step3.5 '''
    if event.postback.data == 'selected time' and doc.to_dict()['status'] == 'order' and doc.to_dict()['step'] == '3':        
        # 傳送選擇時間的Message, if 正確下一個step, 錯誤叫他重新點
        hour = int(event.postback.params['datetime'][-5:-3])
        minute = int(event.postback.params['datetime'][-2:])
        Select_time = hour*3600+minute*60
        if 49800 >= Select_time >= 41400 or 71400 >= Select_time >= 61200:
            firebase_rec['step'] = '3.5'
            doc_ref.update(firebase_rec)
            ConfirmPostMessage = AllMessage.Confirm_PostMessage(event.postback.params['datetime'], number = 5)
            line_bot_api.reply_message(ert, ConfirmPostMessage)
        else:
            line_bot_api.reply_message(ert, TextSendMessage(text='麻煩請選擇其他時間') )
        return 0

    ''' 訂位功能step4 '''
    if doc.to_dict()['status'] == 'order' and doc.to_dict()['step'] == '3.5':
        if 'yes' in event.postback.data:
            data = event.postback.data.split(' ') 
            firebase_rec['step'] = '4'
            firebase_rec['selected_time'] = data[1]
            doc_ref.update(firebase_rec)
            line_bot_api.reply_message(ert, TextSendMessage(text='請問共有幾位貴賓?') )
        else:
            firebase_rec['step'] = '3'
            doc_ref.update(firebase_rec)
            TimeMessage = AllMessage.Time_Message(number = 1)
            line_bot_api.reply_message(ert, TimeMessage) # 傳送選擇日期的Message
        return 0

    ''' 取消訂位step2 '''
    if doc.to_dict()['step'] == 'C1' and doc.to_dict()['status'] == 'cancel':
        firebase_rec['step'] = 'C2'
        doc_ref.update(firebase_rec)

        ConfirmMessage = AllMessage.Confirm_PostMessage(data, number = 1)
        line_bot_api.reply_message(ert, ConfirmMessage)
        return 0

    ''' 取消訂位step3 '''
    if doc.to_dict()['step'] == 'C2' and doc.to_dict()['status'] == 'cancel':
        if data == 'no':
            firebase_rec['step'] = 'F'
            firebase_rec['status'] = 'free'
            doc_ref.update(firebase_rec)
            line_bot_api.reply_message(ert, TextSendMessage(text='感謝您不取消訂位~'))
            return 0
        doc_ref = firedb.collection('訂位紀錄').document(UserId)
        doc = doc_ref.get()
        reply_message = '[取消訂位]\n詳細資訊如下:\n姓名: ' + doc.to_dict()[data][0] + '\n預約日期: ' + doc.to_dict()[data][1].split('T')[0] + '\n預約時間: ' + doc.to_dict()[data][1].split('T')[1] + '\n預約人數: ' +  doc.to_dict()[data][2] + '\n訂單編號: ' +  doc.to_dict()[data][4]
        
        cancel_rec = {}
        cancel_rec[data] = None
        doc_ref.update(cancel_rec) # 用None 取代

        firebase_rec['step'] = 'F'
        firebase_rec['status'] = 'free'
        doc_ref = firedb.collection('是否訂位').document(UserId)
        doc_ref.update(firebase_rec)

        line_bot_api.reply_message(ert, TextSendMessage(text=reply_message))
        
        doc_ref = firedb.collection_group('控制端')
        docs = doc_ref.stream() # generator
        for doc in docs:
            line_bot_api_server.push_message(doc.to_dict()['User_Id'] , TextSendMessage(text='[客人取消訂位]\n詳細資訊如下:\n' + reply_message[10:])) # 通知Manager端 取消訂位

        return 0

    ''' 新增餐點 '''
    if bool(re.match('加', event.postback.data)):
        data = event.postback.data.split(' ') # list
        if doc.to_dict()['status'] == 'oout':
            doc_ref = firedb.collection('外帶購物車').document(UserId)
        else: 
            doc_ref = firedb.collection('內用購物車').document(UserId)
        doc = doc_ref.get()
        if doc.to_dict() == None: # 無過往紀錄
            firebase_rec[data[1]] = 1
            doc_ref.set(firebase_rec)
        else:
            if data[1] in doc.to_dict():
                firebase_rec[data[1]] = doc.to_dict()[data[1]] + 1
                doc_ref.update(firebase_rec)
            else:
                firebase_rec[data[1]] = 1
                doc_ref.update(firebase_rec)
        return 0
    
    ''' 刪除餐點 '''
    if bool(re.match('減', event.postback.data)):
        data = event.postback.data.split(' ')
        if doc.to_dict()['status'] == 'oout':
            doc_ref = firedb.collection('外帶購物車').document(UserId)
        else: 
            doc_ref = firedb.collection('內用購物車').document(UserId)
        doc = doc_ref.get()
        if doc.to_dict() == None: # 無過往紀錄
            pass
        else:
            if data[1] in doc.to_dict():
                if doc.to_dict()[data[1]] == 0:
                    pass
                else:
                    firebase_rec[data[1]] = doc.to_dict()[data[1]] - 1
                    if firebase_rec[data[1]] == 0:
                        firebase_rec[data[1]] = None
                    doc_ref.update(firebase_rec)
            else:
                pass
        return 0

    ''' 當日外帶 step3 '''
    if doc.to_dict()['status'] == 'oout' and doc.to_dict()['step'] == '3':
        # 傳送選擇時間的Message, if 正確下一個step, 錯誤叫他重新點
        hour = int(event.postback.params['datetime'][-5:-3])
        minute = int(event.postback.params['datetime'][-2:])
        Select_time = hour*3600+minute*60
        if 49800 >= Select_time >= 41400 or 71400 >= Select_time >= 61200:
            firebase_rec['step'] = '3.5'
            doc_ref.update(firebase_rec)
            ConfirmPostMessage = AllMessage.Confirm_PostMessage(event.postback.params['datetime'], number = 5)
            line_bot_api.reply_message(ert, ConfirmPostMessage)
        else:
            line_bot_api.reply_message(ert, TextSendMessage(text='麻煩請選擇其他時間') )
        return 0

    ''' 當日外帶 step4 '''
    if doc.to_dict()['status'] == 'oout' and doc.to_dict()['step'] == '3.5':
        if bool(re.match('yes', event.postback.data)):
            data = event.postback.data.split(' ') 
            firebase_rec['selected_time'] = data[1]
            firebase_rec['step'] = 'F'
            firebase_rec['status'] = 'free'
            doc_ref.update(firebase_rec)
            
            doc_ref = firedb.collection('外帶購物車').document(UserId)
            dict_doc = doc_ref.get().to_dict()

            profile = line_bot_api.get_profile(UserId)
            reply_message = "顧客 " + profile.display_name + " 的外帶詳細如下:" + "\n外帶時間: " + data[1]
            for key, value in dict_doc.items():
                reply_message += "\n" + key + ":" + str(value) + "份"
            firebase_rec = None
            doc_ref.set(firebase_rec)
            line_bot_api.reply_message(ert, TextSendMessage(text=reply_message) )

            doc_ref = firedb.collection_group('控制端')
            docs = doc_ref.stream() # generator
            for doc in docs:
                line_bot_api_server.push_message(doc.to_dict()['User_Id'] , TextSendMessage(text=reply_message)) # 通知Manager端, 讓其確認是否同意
        else:
            firebase_rec['step'] = '3'
            doc_ref.update(firebase_rec)
            TimeMessage = AllMessage.Time_Message(number = 1)
            line_bot_api.reply_message(ert, TimeMessage) # 傳送選擇日期的Message
        return 0

    if bool(re.match('confirm', event.postback.data)):
        firebase_rec['step'] = '2'
        doc_ref.update(firebase_rec)
        if doc.to_dict()['status'] == 'oout':
            doc_ref = firedb.collection('外帶購物車').document(UserId)
        else:
            doc_ref = firedb.collection('內用購物車').document(UserId)
        doc = doc_ref.get()
        dict_doc = doc.to_dict()
        #{'東坡肉': 1, '芒果炒雞柳': 3}
        ConfirmPostMessage = AllMessage.Confirm_PostMessage(dict_doc, 6)
        line_bot_api.push_message(UserId, ConfirmPostMessage)
        return 0

    ''' 確認餐點 step2'''
    if bool(re.match('menu', event.postback.data)) and doc.to_dict()['step'] == '2':
        if bool(re.match('yes', event.postback.data)):
            if doc.to_dict()['status'] == 'oin':
                firebase_rec['step'] = 'F'
                firebase_rec['status'] = 'free'
                doc_ref.update(firebase_rec)
                doc_ref = firedb.collection('內用購物車').document(UserId)
                line_bot_api.push_message(UserId, TextSendMessage(text = '好的! 已幫您告知告知店家，請於用餐完畢後結帳，感謝您!'))
                
                data = event.postback.data.split(' ')[2:]
                profile = line_bot_api.get_profile(UserId)
                reply_message = "顧客 " + profile.display_name + " 的店內點餐餐點詳細如下:"
                for d in range(0,len(data)-1,2):
                    reply_message = reply_message + '\n' + data[d] + ' ' + data[d+1] + "份"
                firebase_rec = None
                doc_ref.set(firebase_rec)
                doc_ref = firedb.collection_group('控制端')
                docs = doc_ref.stream() # generator
                for doc in docs:
                    line_bot_api_server.push_message(doc.to_dict()['User_Id'] , TextSendMessage(text = reply_message)) # 通知Manager端, 讓其確認
            else:
                firebase_rec['step'] = '3'
                doc_ref.update(firebase_rec)
                TimeMessage = AllMessage.Time_Message(number = 1)
                line_bot_api.reply_message(ert, TimeMessage) # 傳送選擇日期的Message
        else:
            Menu_Message = AllMessage.Menu_Message()
            line_bot_api.push_message(UserId, Menu_Message)
        return 0
    else:
        line_bot_api.reply_message(ert, TextSendMessage(text='麻煩請重新操作!!') )
        return 0
    #print(event.postback.params['datetime']) # {"data": "seleced", "params": {"datetime": "2019-12-21T18:44"}}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print(event)
    UserId = event.source.user_id
    UserMessage = event.message.text
    ert = event.reply_token
    firebase_rec = {}
    doc_ref = firedb.collection('是否訂位').document(UserId)
    doc = doc_ref.get()
    
    ''' 訂位管理 '''
    if bool(re.match('訂位管理', UserMessage)):
        ConfirmPostMessage = AllMessage.Confirm_PostMessage(UserMessage, number = 4)
        line_bot_api.push_message(UserId, ConfirmPostMessage)
        return 0

    ''' 訂位功能step1 '''
    if doc.to_dict() == None: # 無過往紀錄
        UseSeveralTimesMessage = AllMessage.Use_Several_Times_Message(number = 2, UserId = UserId, UserMessage = UserMessage)
        line_bot_api.reply_message(ert, UseSeveralTimesMessage) # 接續step3
        return 0
    elif '預約訂位' in UserMessage and doc.to_dict()['status'] == 'free':# 如果有關鍵字以及status為order
        UseSeveralTimesMessage = AllMessage.Use_Several_Times_Message(number = 3, UserId = UserId, UserMessage = UserMessage)
        line_bot_api.reply_message(ert, UseSeveralTimesMessage) # 接續step3
        return 0
    
    ''' 訂位功能step2 '''
    if doc.to_dict()['status'] == 'order' and doc.to_dict()['step'] == '1' and '訂位管理' not in UserMessage and '店內點餐' not in UserMessage and '預約訂位' not in UserMessage:
        firebase_rec['Name'] = UserMessage[0] # 取第一個字
        firebase_rec['step'] = '2'
        doc_ref = firedb.collection('是否訂位').document(UserId)
        doc_ref.update(firebase_rec)

        ConfirmPostMessage = AllMessage.Confirm_PostMessage(UserMessage, number = 3)
        line_bot_api.reply_message(ert, ConfirmPostMessage) # 傳送先生小姐按鈕
        return 0
    # 如果中途按下其他按鈕，取消訂位並狀態清空
    elif doc.to_dict()['status'] == 'order' and doc.to_dict()['step'] == '1': 
        firebase_rec['step'] = 'F'
        firebase_rec['status'] = 'free'
        doc_ref = firedb.collection('是否訂位').document(UserId)
        doc_ref.update(firebase_rec)
        if bool(re.match('訂位管理', UserMessage)):
            line_bot_api.reply_message(ert, TextSendMessage(text='取消訂位'))
            UseSeveralTimesMessage = AllMessage.Use_Several_Times_Message(number = 1, UserId = UserId, UserMessage = UserMessage)
            line_bot_api.push_message(UserId, TextSendMessage(text=UseSeveralTimesMessage))
            return 0
        elif bool(re.match('店內點餐', UserMessage)):
            line_bot_api.reply_message(ert, [TextSendMessage(text='取消訂位'), TextSendMessage(text='麻煩拍照或上傳桌面上QRcode照片' )])
            return 0
        elif bool(re.match('預約訂位', UserMessage)):
            doc_ref = firedb.collection('是否訂位').document(UserId)
            doc = doc_ref.get()
            if doc.to_dict() == None: # 無過往紀錄
                UseSeveralTimesMessage = AllMessage.Use_Several_Times_Message(number = 2, UserId = UserId, UserMessage = UserMessage)
                line_bot_api.push_message(UserId, UseSeveralTimesMessage) # 接續step3
                return 0
            elif bool(re.match('訂位', UserMessage)) and doc.to_dict()['status'] == 'free': # 如果有關鍵字以及status為order
                UseSeveralTimesMessage = AllMessage.Use_Several_Times_Message(number = 3, UserId = UserId, UserMessage = UserMessage)
                line_bot_api.push_message(UserId, UseSeveralTimesMessage) # 接續step3
                return 0

    ''' 訂位功能step5 傳送確認訊息 '''
    if doc.to_dict()['status'] == 'order' and doc.to_dict()['step'] == '4' and '訂位管理' not in UserMessage and '店內點餐' not in UserMessage:
        firebase_rec['Num_People'] = UserMessage
        firebase_rec['step'] = '5'
        doc_ref.update(firebase_rec) # 更新db的點餐狀態
        
        rec = []
        rec.append(doc.to_dict()['Name'])
        rec.append(doc.to_dict()['selected_time'])
        rec.append(UserMessage)
        rec.append(UserId)

        line_bot_api.push_message(UserId, TextSendMessage(text = '等候回覆中'))
        ConfirmPostMessage = AllMessage.Confirm_PostMessage(rec, number = 2)
        doc_ref = firedb.collection_group('控制端')
        docs = doc_ref.stream() # generator
        for doc in docs:
            line_bot_api_server.push_message(doc.to_dict()['User_Id'] , ConfirmPostMessage) # 通知Manager端, 讓其確認是否同意

        return 0

    ''' 取消訂位step1 '''
    if bool(re.match('取消預約', UserMessage)):
        stickermessage = AllMessage.Sticker_Message(1)
        CancelMessage = AllMessage.Cancel_Message(UserId)
        line_bot_api.push_message(UserId, [stickermessage, CancelMessage])
        return 0
            

    ''' 店內點餐 '''
    if bool(re.match('店內點餐', UserMessage)):
        line_bot_api.push_message(UserId, TextSendMessage(text='麻煩拍照或上傳桌面上QRcode照片' ))
        return 0
    

    ''' 當日外帶 '''
    if bool(re.match('當日外帶', UserMessage)):
        firebase_rec['status'] = 'oout'
        firebase_rec['step'] = '1'
        doc_ref.update(firebase_rec)
        Menu_Message = AllMessage.Menu_Message()
        line_bot_api.reply_message(ert, Menu_Message)
        return 0

    ''' 等待商家回覆 '''
    if doc.to_dict()['step'] == '5':
        if bool(re.match('訂位管理', UserMessage)):
            firebase_rec['step'] = 'F'
            firebase_rec['status'] = 'free'
            doc_ref.update(firebase_rec)
            ConfirmPostMessage = AllMessage.Confirm_PostMessage(UserMessage, number = 4)
            line_bot_api.push_message(UserId, ConfirmPostMessage)
            return 0
        elif bool(re.match('店內點餐', UserMessage)):
            line_bot_api.push_message(UserId, TextSendMessage(text='麻煩拍照或上傳桌面上QRcode照片' ))
            return 0
        elif bool(re.match('當日外帶', UserMessage)):
            Menu_Message = AllMessage.Menu_Message()
            line_bot_api.push_message(UserId, Menu_Message)
            return 0
        else:
            line_bot_api.reply_message(ert, TextSendMessage(text='正在等待店家同意訂位中,請稍後~') )
        return 0

    else: # 非選單上的功能及不知所云的話會到這
        firebase_rec['step'] = 'F'
        firebase_rec['status'] = 'free'
        doc_ref.update(firebase_rec)
        line_bot_api.push_message(UserId, TextSendMessage(text='麻煩重新操作,感謝您!'))
        return 0


@handler.add(MessageEvent, message=ImageMessage)
def handle_imgmessage(event):
    print(event)
    filepath = './test.jpg'
    UserId = event.source.user_id
    #ert = event.reply_token
    firebase_rec = {}
    doc_ref = firedb.collection('內用購物車').document(UserId)
    doc = doc_ref.get()
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(filepath, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    try:
        m1 = cv2.imread(filepath, 1)
        r = pyzbar.decode(m1)
        msg = ""
        for i,d in enumerate(r):
            msg = d.data.decode("UTF-8")
            print("第",i+1,"個條碼, 類型:",d.type,", 內容:",d.data.decode("UTF-8"))
        
        if bool(re.match('akanar', msg)): # 金鑰認證
            table = msg.split(' ')[1]
            firebase_rec['桌號'] = table
            if doc.to_dict() == None: # 無過往紀錄
                doc_ref.set(firebase_rec)
            else:
                doc_ref.update(firebase_rec) # update 桌號

            doc_ref = firedb.collection('是否訂位').document(UserId)
            firebase_rec = {}
            firebase_rec['status'] = 'oin'
            firebase_rec['step'] = '1'
            doc_ref.update(firebase_rec) # update 狀態

            Menu_Message = AllMessage.Menu_Message()
            line_bot_api.push_message(UserId, Menu_Message)
        else:
            line_bot_api.push_message(UserId, TextSendMessage(text='QRcode的內容為: ' + msg))
    except:
        line_bot_api.push_message(UserId, TextSendMessage(text='圖片不是QRcode,請上傳QRcode圖片'))
    return 0

# 使用者加入Line好友的時候
@handler.add(FollowEvent)
def handle_follow(event):
    UserId = event.source.user_id # 將新加入的(follow)使用者資訊寫入資料庫中
    user_rec = {}
    profile = line_bot_api.get_profile(UserId)
    user_rec['User_Id'] = UserId
    user_rec['User_Name'] = profile.display_name
    user_rec['User_imgurl'] = profile.picture_url
    doc_ref = firedb.collection('客戶端').document(UserId)
    doc_ref.set(user_rec)
    firebase_rec = {}
    firebase_rec['status'] = 'free'
    doc_ref = firedb.collection('是否訂位').document(UserId) # 設定初始狀態為free
    doc_ref.set(firebase_rec)
    # 發送「歡迎加入」給使用者
    line_bot_api.reply_message( event.reply_token, TextSendMessage(text='歡迎使用瑋瑋快易點'))

# 初始化客戶端和控制端的Rich Menu圖文選單
#def init_richmenu():
    #doc_ref = firedb.collection_group('客戶端')
    #docs = doc_ref.stream() # generator
    #for doc in docs:
        #dic = doc.to_dict()
        #line_bot_api.link_rich_menu_to_user(dic['User_Id'], Richmenu_Client_Id)

# 使用者封鎖Line帳號的時候
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    doc_ref = firedb.collection('客戶端').document(event.source.user_id)
    doc_ref.delete()
    doc_ref = firedb.collection('是否訂位').document(event.source.user_id)
    doc_ref.delete()


if __name__ == "__main__":
    #init_richmenu()
    app.run()