# Restaurant_Client_Linebot

這是一篇紀錄，有關於製作客製化linebot的相關程式原始碼，裡面包含如何連結firebase來操作firebase的資料庫，以及如何使用ngrok和heroku來架設linebot，並且讓使用者能依照設計者的想法來點餐的一個系統，這是系統的client端部分，也就是客戶訂位點餐。

當初卡最久的還是richmenu(圖文選單)和各式各樣的訊息回覆，前者是在手機上會在下方顯示的部分，後者處理起來麻煩的點是要如何去設計到完美，有點像是寫網頁的css

這兩篇有關linebot的部分，程式碼並沒有辦法複製下來就可以直接用，必須修改其中的token以及secret，還有firebase的金鑰密碼，有關這些部分，我都寫在App_Config.py了，如果要有疑問的話歡迎發issue，有看到的話我都會盡量處理。

程式架構為:
  
1. app.py為主程式  
2. App_Config.py為金鑰密碼及token等等
3. create_and_set_richmenu_body.py為建立及管理rich menu  
4. model/message.py則是各項message的部分，集中管理
  
![架構圖](/LineBot.png)

### 以下是參考的網址
ngrok: https://cleanshadow.blogspot.com/2017/02/ngrokline-botwebhook.html

透過python架設linebot:
1. 官方文件: https://github.com/line/line-bot-sdk-python
2. https://yaoandy107.github.io/line-bot-tutorial/

richmenu: 
1. https://medium.com/enjoy-life-enjoy-coding/%E4%BD%BF%E7%94%A8-python-%E7%82%BA-line-bot-%E5%BB%BA%E7%AB%8B%E7%8D%A8%E4%B8%80%E7%84%A1%E4%BA%8C%E7%9A%84%E5%9C%96%E6%96%87%E9%81%B8%E5%96%AE-rich-menus-7a5f7f40bd1
2. https://medium.com/front-end-augustus-study-notes/line-bot-rich-menu-aa5fa67ac6ae

firebase:
1. firebase連結python: https://medium.com/pyradise/10%E5%88%86%E9%90%98%E8%B3%87%E6%96%99%E5%BA%AB%E6%93%8D%E4%BD%9C-%E6%96%B0%E5%A2%9E%E8%B3%87%E6%96%99-b96db385e1e4
2. firbase資料庫語法: https://mks.tw/2675/%E3%80%8C%E5%AD%B8%E7%BF%92%E6%97%A5%E8%AA%8C%E3%80%8Dcloud-firestore-%E5%9F%BA%E6%9C%AC%E6%96%B0%E5%A2%9E%E3%80%81%E6%9F%A5%E8%A9%A2%E3%80%81%E5%88%AA%E9%99%A4%E5%88%9D%E9%AB%94%E9%A9%97-python

弄最久的 flex message:
1. https://blog.clarence.tw/2019/09/22/2020ironman06/
2. https://ithelp.ithome.com.tw/articles/10198142
3. flex message simulator: https://developers.line.biz/flex-simulator/
