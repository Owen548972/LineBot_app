from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    ImageSendMessage,
    LocationSendMessage,
)
from Crawler.main import get_lottory, get_true_lottory

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def index(request):
    return HttpResponse("This is ChatBot v1.0")


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text

                if text == "1":
                    message = TextSendMessage(text="你好")

                elif text == "2":
                    message = TextSendMessage(text="早安")

                elif "樂透" in text:
                    message = TextSendMessage(text=get_lottory())

                elif "威力彩" in text:
                    message = TextSendMessage(text=get_true_lottory())

                elif "捷運" in text:
                    if "台中" in text:
                        Image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taichung/20201112_zh.png?v=2"

                    elif "高雄" in text:
                        Image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/kaohsiung/202210_zh.png"

                    elif "機場" in text:
                        Image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/airport/map3-tw.png"

                    else:
                        Image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taipei/20230214_zh.png"

                    message = ImageSendMessage(
                        original_content_url=Image_url, preview_image_url=Image_url
                    )

                elif "高鐵" in text:
                    Image_url = (
                        "https://8car.com.tw/uploads/images/articles/1552641550.png"
                    )
                    message = ImageSendMessage(
                        original_content_url=Image_url, preview_image_url=Image_url
                    )

                elif "台北車站" in text:
                    message = LocationSendMessage(
                        title="台北車站",
                        address="100臺北市中正區黎明里北平西路3號",
                        latitude=25.047778,
                        longitude=121.517222,
                    )

                else:
                    message = TextSendMessage(
                        text="I Don't know what are you talking about"
                    )
                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        message,
                    )
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
