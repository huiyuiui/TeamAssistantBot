# LINE Bot v3 with LangChain

## 概述

看到一個不知道是什麼的餐廳或食物時是不是覺得困擾？老師講的東西聽不懂？朋友在聊股票聽不懂？

此專案結合 LangChain+OpenAI，幫助你快速把一句不確定的文字，透過 LINE Bot 介面提供給你答案

## 環境變數

你需要設置以下環境變數：

- API_ENV: 應用程式的運行環境，可以是 'production' 或 'develop'，預設 develop。
- LOG: 紀錄的等級，例如 'WARNING'、'INFO'、'DEBUG' 等。
- LINE_CHANNEL_ACCESS_TOKEN: LINE Channel 的 Access Token。
- LINE_CHANNEL_SECRET: LINE Channel 的 Secret。
- OPENAI_API_KEY: OpenAI 的 API Key。
- PORT: 預設 8080

## 開發方法

```
git clone https://github.com/louis70109/linebot-find-some
cd linebot-find-some/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
如果使用conda建立虛擬環境
```
conda create --name ENV_NAME python==3.11.4
conda activate ENV_NAME
pip install -r requirements.txt
python main.py
```

透過 ngrok 建立暫時含有 https 的網址，並設定在 LINE Developer Console

```
ngrok http 80
```
需要將.env中PORT要改成80<br>
隨後將.app那個網址加上/webhooks/line，將其複製粘貼到Weebhook URL，若按下verify有出現success代表成功

運用 `change_bot_url.sh` 來替換 LINE Bot webhook URL

```
sh change_bot_url.sh LINE_ACCESS_TOKEN https://YOUR_DOMAIN/webhooks/line
```



將 Domain 設定於 LINE Developer Console

1. 前往 LINE Developer Console 網站：https://developers.line.biz/console/
2. 點選右上角的「Log in」按鈕，登入您的 LINE 帳號。如果您還沒有 LINE 帳號，您需要先建立一個。
3. 在網頁上方的選單中，選擇「Provider」，然後選擇「Create」。
4. 在彈出的視窗中，輸入一個 Provider 名稱，然後點擊「Create」。
5. 建立之後，您將被導向該 Provider 的頁面。在這裡，選擇「Create Channel」。
6. 您需要選擇您要創建的 Channel 類型，對於 bot，請選擇「Messaging API」。
7. 填寫 Channel 的資訊，包括 Channel 名稱、Channel 說明、區域、大頭貼等等，然後點選「Create」。
8. Channel 建立後，您將被導向 Channel 的設定頁面。在這裡，您可以看到您的 Channel ID、Channel Secret、以及 Channel Access Token，這些資訊將被用於設定 bot。
9. 還有一個重要的設定是「Use webhooks」。如果您希望您的 bot 可以接收來自 LINE 的訊息，您需要打開這個設定，並輸入您的 webhook URL。您的 webhook URL 是一個可以接收 POST 請求的伺服器網址。
10. 之後，您可以在 LINE app 中加入您剛剛建立的 bot 為好友，並開始測試。

## Google Cloud Platform 佈署

### 一鍵佈署

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

Clone 此專案

```
git clone https://github.com/louis70109/linebot-find-some
cd linebot-find-some/
```

### gcloud 基礎設定

- `gcloud init`：初始化 gcloud CLI，該指令會提示登錄 Google 帳戶，並選擇您要使用的 GCP 項目。
- `gcloud config set project PROJECT_ID`：設定 GCP Project ID，以便 gcloud CLI 與該項目交互使用。
- `gcloud auth login`：登錄 Google 帳戶。

透過 [gcloud](https://cloud.google.com/sdk/docs/install?hl=zh-cn) 指令佈署

```
gcloud run deploy calendar-linebot-1 --source .
```

> 佈署參考: [【GCP】將 FastAPI 佈署上 Cloud Run](https://nijialin.com/2023/03/19/gcp-why-need-cloudrun-as-serverless/#5-%E4%BD%88%E7%BD%B2%E5%88%B0-Google-Cloud-Run)

## 參與貢獻

如果你有任何問題或建議，歡迎開 issue 或 pull request。

## LICENSE

請見 LICENSE 文件。
