from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer
)

def group_flex_menu(group_id: str):
    bubble_string = f'''{{
        "type": "bubble",
        "hero": {{
            "type": "image",
            "url": "https://scontent.ftpe7-3.fna.fbcdn.net/v/t39.30808-6/240730368_4456213274434666_4157641106449464359_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=5f2048&_nc_ohc=ysdF2aeebiAAX_lS3pW&_nc_ht=scontent.ftpe7-3.fna&oh=00_AfAJlFEe8frDD54I2cICiTNIdH8J8WUHVQ2oUbb3W-Q4Ng&oe=6539595B",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {{
            "type": "uri",
            "uri": "http://linecorp.com/"
            }}
        }},
        "body": {{
            "type": "box",
            "layout": "vertical",
            "contents": [
            {{
                "type": "text",
                "text": "森森",
                "weight": "bold",
                "size": "xl"
            }},
            {{
                "type": "text",
                "text": "本喵是森森，你可以對我做以下事情"
            }},
            {{
                "type": "text",
                "text": "直接呼叫森森讓本喵幫你管理事項"
            }},
            {{
                "type": "text",
                "text": "喵喵叫：提醒組員完成待辦清單"
            }},
            {{
                "type": "text",
                "text": "悄悄話：讓森森幫你說出心裡話"
            }},
            {{
                "type": "text",
                "text": "懶貓包：統整小組訊息"
            }}
            ]
        }},
        "footer": {{
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
            {{
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {{
                "type": "postback",
                "label": "喵喵叫",
                "data": "action=reminder"
                }}
            }},
            {{
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {{
                "type": "uri",
                "label": "悄悄話",
                "uri": "https://hackathonlinebot.web.app/?id={group_id}"
                }}
            }},
            {{
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {{
                "type": "postback",
                "label": "懶貓包",
                "data": "action=sumerise"
                }}
            }}
            ],
            "flex": 0
        }}
    }}'''

    return bubble_string