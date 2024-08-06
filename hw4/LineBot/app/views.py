from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from .scripts.new import New
from .scripts.stock import stock
from .scripts.ntut_post import ntut_post

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_LONG_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

user_states = {}

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                user_id = event.source.user_id
                user_message = event.message.text

                if user_id not in user_states:
                    user_states[user_id] = 'waiting_for_command'

                if user_states[user_id] == 'waiting_for_command':
                    if '取得新聞' in user_message:
                        try:
                            new_data = New()
                            news_message = (
                                f"News Title: {new_data['title']}\n"
                                f"News Date: {new_data['date']}\n"
                                f"News Context:\n{new_data['context']}"
                            )
                            response_message = TextSendMessage(text=news_message)
                        except Exception as e:
                            response_message = TextSendMessage(text=f"Error: {str(e)}")
                    elif '取得股票' in user_message:
                        response_message = TextSendMessage(text='請輸入股票代碼')
                        user_states[user_id] = 'waiting_for_stock_code'
                    elif '北科' in user_message:
                        try:
                            ntut_post_data = ntut_post()
                            response_message = TextSendMessage(text=ntut_post_data)
                        except Exception as e:
                            response_message = TextSendMessage(text=f"Error: {str(e)}")
                    else:
                        response_message = TextSendMessage(text='請輸入「取得新聞」或「取得股票」')

                elif user_states[user_id] == 'waiting_for_stock_code':
                    try:
                        code = int(user_message)
                        stock_data = stock(code)
                        if stock_data:
                            stock_message = (
                                f"Stock Name: {stock_data['stock_name']}\n"
                                f"Stock Code: {stock_data['stock_code']}\n"
                                f"Stock Price: {stock_data['stock_price']}\n"
                                f"Change: {stock_data['stock_change']}\n"
                                f"Change Rate: {stock_data['stock_change_rate']}"
                            )
                            response_message = TextSendMessage(text=stock_message)
                        else:
                            response_message = TextSendMessage(text='No data found for the stock code.')
                    except ValueError:
                        response_message = TextSendMessage(text='Invalid stock code format. Please enter a valid stock code.')
                    except Exception as e:
                        response_message = TextSendMessage(text=f"Error: {str(e)}")

                    user_states[user_id] = 'waiting_for_command'
                    
                line_bot_api.reply_message(event.reply_token, response_message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()