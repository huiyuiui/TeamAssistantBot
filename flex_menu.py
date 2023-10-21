from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer
)
bubble_string = """{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "進度提醒",
          "data": "action=reminder"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "匿名發言",
          "uri": "http://linecorp.com/"
        }
      }
    ]
  },
  "styles": {
    "body": {
      "separator": true
    }
  }
}"""
flex_menu = FlexMessage(alt_text="hello", contents=FlexContainer.from_json(bubble_string))