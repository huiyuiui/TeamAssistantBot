import logging
import os
import sys

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    StickerMessage,
    FlexMessage,
    FlexContainer
)

from flex_menu import group_flex_menu

from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from mood_tool import MoodAnalyzerTool

from random_reminder import Random_textandsticker


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
tools = []
system_message = SystemMessage(content=""" 如果回答裡出現中文，你傾向使用繁體中文回答問題。 """)
open_ai_agent = initialize_agent(
    tools,
    model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=False,
    agent_kwargs={"system_message": system_message},)

mood_tool_agent = initialize_agent(
    tools = [MoodAnalyzerTool() ],
    llm = model,
    agent = AgentType.OPENAI_FUNCTIONS,
    verbose=False,
)
# collect previous message
message_list = []
received_data = []
@app.post("/webhooks/line")
async def handle_callback(request: Request):
    global message_list
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
        # join event
        if(event.type == 'join'):
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='在這裡輸入歡迎訊息')]
                )
            )
            continue
        if(event.type == 'message' and event.message.text == '森森'):
            groupId = event.source.group_id
            flex_menu = FlexMessage(alt_text="flex_menu", contents=FlexContainer.from_json(group_flex_menu(groupId)))
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages = [flex_menu]
                )
            )
            continue
        if(event.type == 'postback' and event.postback.data == 'action=reminder'):
            Rtext, Rpackage_id, Rsticker_id = Random_textandsticker()
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=Rtext), StickerMessage(package_id=Rpackage_id, sticker_id=Rsticker_id)]
                    )
                )
            continue
        if(event.type == 'postback' and event.postback.data == 'action=sumerise'):
            Rtext, Rpackage_id, Rsticker_id = Random_textandsticker()
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text='陳家輝的code接到這裡')]
                    )
                )
            continue
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        # collect previous message
        message_list.append(HumanMessage(content=event.message.text))
    
        # tool_result = open_ai_agent.run(event.message.text)
        tool_result = open_ai_agent.run(message_list)

        # collect ai reply message
        message_list.append(AIMessage(content=tool_result))

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=tool_result)]
            )
        )

    return 'OK'

# get web data
@app.post("/submit")
async def submit(request: Request):
    global received_data
    data = await request.form()
    print(f"raw data: {data}")
    received_data.append(data["data"])
    groupId = data["groupId"]
    print(f'id: {groupId}')
    print("Received message: ", received_data)
    # send a push message to the group
    # run with mood_tool only
    tool_result = mood_tool_agent.run(received_data)
    from mood_tool import _output
    print(f"mood result: {_output['mood']}")
    print(f"packageId: {_output['packageId']}, stickerId: {_output['stickerId']}")
    if _output["packageId"] == "" or _output["stickerId"] == "":
        await line_bot_api.push_message(PushMessageRequest(
            to=groupId,
            messages=[TextMessage(text=received_data[0])]
        ))
    else:
        await line_bot_api.push_message(PushMessageRequest(
            to=groupId,
            messages=[TextMessage(text=received_data[0]), StickerMessage(package_id=_output["packageId"], sticker_id=_output["stickerId"])]
        ))
    received_data = received_data[1:]
    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f1f1f1;
                padding: 20px;
                text-align: center;
            }

            p {
                font-weight: bold;
                font-size: 4vw; 
            }
        </style>
        </head>
        <body>
            <p>成功送出！</p>
            <p>請回到LINE聊天室點擊匿名發言，讓機器人幫你告訴大家！</p>
        </body>
        </html>

    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', default=8080))
    debug = True if os.environ.get(
        'API_ENV', default='develop') == 'develop' else False
    logging.info('Application will start...')
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)