import logging
import os
import sys

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from stock_peformace import StockPercentageChangeTool, StockGetBestPerformingTool
from stock_price import StockPriceTool
from langchain.schema import HumanMessage
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from wikipedia import WikiTool
from youtube_restaurant import FindYoutubeVideoTool
from search_info import SearchInfoTool
from summarizer import SummarizeTool

import csv
from datetime import datetime
from collections import deque

logging.basicConfig(level=os.getenv('LOG', 'WARNING'))
logger = logging.getLogger(__file__)


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=channel_access_token
)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)


# Langchain (you must use 0613 model to use OpenAI functions.)
model = ChatOpenAI(model="gpt-3.5-turbo-0613")
tools = [
    SummarizeTool(), SearchInfoTool()
]#  WikiTool(), StockPriceTool(), StockPercentageChangeTool(),
 #   StockGetBestPerformingTool(), FindYoutubeVideoTool(),
open_ai_agent = initialize_agent(
    tools,
    model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=False)


@app.post("/webhooks/line")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        print(event)
        await write_message(event)
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        # await line_bot_api.push_message(push_message_request=PushMessageRequest(
        #     to=event.source.user_id,
        #     messages=[TextMessage(text=event.message.text,
        #                           quoteToken=event.message.quote_token)],
        # ))

        line_bot_name = "森森"
        if f"{line_bot_name}" in event.message.text:
            if event.message.text.find("summary") != -1:
                print("SUM")
                root = f"messages/message_content_{event.source.group_id}.txt"
                with open(root, 'r', encoding="utf-8") as f:
                    messages = f.readlines()
                    print(messages)
                    tool_result = open_ai_agent.run(messages)
            
            else:
                tool_result = open_ai_agent.run(event.message.text)

            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=tool_result)]
                )
            )

    return 'OK'

async def write_message(event):
    root = f"messages/message_content_{event.source.group_id}.txt"
    with open(root, 'r', encoding="utf-8") as f:
        messages = f.readlines()
        message_queue = deque(messages, maxlen=25)

    if event.message.type != "text":
        return
    elif event.message.text.find("森森") != -1:
        return


    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M")
    profile = await line_bot_api.get_profile(event.source.user_id)

    message_str = str(currentTime) + ' ' + profile.display_name + ':' + event.message.text +'\n'
    message_queue.append(message_str)
    with open(root, 'w', encoding="utf-8") as f:
        f.writelines(message_queue)

    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', default=8080))
    debug = True if os.environ.get(
        'API_ENV', default='develop') == 'develop' else False
    logging.info('Application will start...')
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
