from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer
)

def group_flex_menu(group_id: str):
    bubble_string = f"""{{
    "type": "bubble",
    "body": {{
        "type": "box",
        "layout": "horizontal",
        "contents": [
        {{
            "type": "button",
            "action": {{
            "type": "postback",
            "label": "進度提醒",
            "data": "action=reminder"
            }}
        }},
        {{
            "type": "button",
            "action": {{
            "type": "uri",
            "label": "匿名發言",
            "uri": "https://mc-hackathon-20231021.web.app/?id={group_id}"
            }}
        }}
        ]
    }}    
    }}"""

    return bubble_string

