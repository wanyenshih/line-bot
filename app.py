from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('WOeSg/fNMg5/3elpSqkyHt+NhbhdDWGqsLFgkbagRdx1EBqV1cPKa9r8623uXBJDncrSNFViK7pi+0Q+jYmlqWYIk3jsMtrtw5r7fBkYuSBvlYq1nGcvoobIHnUj0sHMP6NvHL1hMl/Jsers/7cciwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('29d0cf3b8c25fb6d2c83beca83065596')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()