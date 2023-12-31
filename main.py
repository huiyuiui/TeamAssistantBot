import logging
import os
import sys
import re
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
    ImageMessage,
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
from wikipedia import WikiTool
from youtube_restaurant import FindYoutubeVideoTool
from google_calendar import CalendarTool
from schedule import ScheduleTool
from search_info import SearchInfoTool
from summarizer import SummarizeTool
from meeting_arangement import MeetingTool

from time import time
from datetime import datetime
from collections import deque
from imgurpython import ImgurClient 
from todo_list import TodoListTool
from mood_tool import MoodAnalyzerTool

from random_reminder import Random_textandsticker
from typing import Dict


import Globals

logging.basicConfig(level=os.getenv('LOG', 'WARNING'))
logger = logging.getLogger(__file__)
Globals.initialize()

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
    SearchInfoTool(), WikiTool(), MeetingTool(),
    SummarizeTool(), FindYoutubeVideoTool(),
    ScheduleTool(), CalendarTool(), TodoListTool()
]
system_message = SystemMessage(content="""
                               你叫做森森，你是一隻貓，你會友善的回覆使用者的任何問題，
                               如果回答裡出現中文，你傾向使用繁體中文回答問題。
                               """)
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
            if(event.source.type=='group'):
                groupId = event.source.group_id
            else:
                groupId = 0
            flex_menu = FlexMessage(alt_text="flex_menu", contents=FlexContainer.from_json(group_flex_menu(groupId)))
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages = [flex_menu]
                )
            )
            continue
        # Flex menu
        if(event.type == 'message' and event.message.text == '森森'):
            if(event.source.type=='group'):
                groupId = event.source.group_id
            else:
                groupId = 0
            flex_menu = FlexMessage(alt_text="flex_menu", contents=FlexContainer.from_json(group_flex_menu(groupId)))
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages = [flex_menu]
                )
            )
            continue
        # Reminder
        if(event.type == 'postback' and event.postback.data == 'action=reminder'):
            if(event.source.type=='group'):
                if os.path.exists(f"todo_lists/todo_list_{event.source.group_id}.json"):
                    Globals.read_todo_from_file(event.source.group_id)
                tool_result = open_ai_agent.run('森森查看目前代辦清單')
            else:
                tool_result = "請在群組中使用此功能喔！"
            Rtext, Rpackage_id, Rsticker_id = Random_textandsticker()
            if(event.source.type=='group'):
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=Rtext), StickerMessage(package_id=Rpackage_id, sticker_id=Rsticker_id), TextMessage(text=tool_result)]
                        )
                    )
            else:
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=Rtext), StickerMessage(package_id=Rpackage_id, sticker_id=Rsticker_id)]
                        )
                    )
            continue
        if(event.type == 'postback' and event.postback.data == 'action=sumerise'):
            if(event.source.type!='group'):
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text="請在群組中使用此功能喔！")]
                        )
                    )
                continue
            root = f"messages/message_content_{event.source.group_id}.txt"
            with open(root, 'r', encoding="utf-8") as f:
                messages = f.readlines()
                print(messages)
                tool_result = open_ai_agent.run(messages)
                with open(root, 'w', encoding="utf-8") as f:
                    f.write("") 
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=tool_result)]
                    )
                )
            continue
        
        # Undefine check
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        # if event.type == "join":
        #     time.sleep(3)
        #     await print_self_introduction(event)
        # elif event.type == "message":
        #     await write_message(event)
        
        # await line_bot_api.push_message(push_message_request=PushMessageRequest(
        #     to=event.source.user_id,
        #     messages=[TextMessage(text=event.message.text,
        #                           quoteToken=event.message.quote_token)],
        # ))

        # Record message(can only be used in group)
        if event.type == "message":
            await write_message(event)

        # Keyword trigger operation
        line_bot_name = "森森"
        if f"{line_bot_name}" in event.message.text:
            if "統整" in event.message.text or "summary" in event.message.text:
                print("SUM")
                root = f"messages/message_content_{event.source.group_id}.txt"
                with open(root, 'r', encoding="utf-8") as f:
                    messages = f.readlines()
                    print(messages)
                    tool_result = open_ai_agent.run(messages)
                    with open(root, 'w', encoding="utf-8") as f:
                        f.write("") 
                    await line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=tool_result)]
                        )
                    )

            elif "什麼時候開會" in event.message.text or "when to meet" in event.message.text:
                print("MEET")
                root = f"messages/message_content_{event.source.group_id}.txt"
                with open(root, 'r', encoding="utf-8") as f:
                    messages = f.readlines()
                    print(messages)
                    tool_result = open_ai_agent.run(messages)
                    with open(root, 'w', encoding="utf-8") as f:
                        f.write("") 
                    print(tool_result)
                    await line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=tool_result)]
                        )
                    )
            else:
                if os.path.exists(f"todo_lists/todo_list_{event.source.group_id}.json"):
                    Globals.read_todo_from_file(event.source.group_id)
                tool_result = open_ai_agent.run(event.message.text)
                # write_sensen_message(event.source.group_id, tool_result)
                
                if ".png" in tool_result:
                    pattern = r'https://.*?\.png'
                    image_url = re.findall(pattern, tool_result)
                    print(image_url)
                    await line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=tool_result), ImageMessage(original_content_url=image_url[0], preview_image_url=image_url[0])]
                        )
                    )
                else :
                    await line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=tool_result)]
                        )
                    )
                    
                Globals.write_todo_to_file(event.source.group_id)
            

    return 'OK'

async def write_message(event):
    if event.type != "message" or event.message.type != "text":
        return
    if "森森" in event.message.text:
        return
    
    root = f"messages/message_content_{event.source.group_id}.txt"
    if os.path.exists(root):
        with open(root, 'r', encoding="utf-8") as f:
            messages = f.readlines()
            message_queue = deque(messages, maxlen=25)
    else:
        message_queue = deque([], maxlen = 25)


    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M")
    profile = await line_bot_api.get_profile(event.source.user_id)

    message_str = str(currentTime) + ' ' + profile.display_name + ':' + event.message.text +'\n'
    message_queue.append(message_str)
    with open(root, 'w', encoding="utf-8") as f:
        f.writelines(message_queue)


def write_sensen_message(group_id: int, text: str):
    print("Writing Sensen message")
    root = f"messages/message_content_{group_id}.txt"
    if os.path.exists(root):
        with open(root, 'r', encoding="utf-8") as f:
            messages = f.readlines()
            message_queue = deque(messages, maxlen=25)
    else:
        message_queue = deque([], maxlen = 25)

    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M")

    message_str = str(currentTime) + ' ' + '森森' + ':' + text +'\n'
    message_queue.append(message_str)
    with open(root, 'w', encoding="utf-8") as f:
        f.writelines(message_queue)

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