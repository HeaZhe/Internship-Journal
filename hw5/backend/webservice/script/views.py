from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from .serializers import NewsSerializer, StocksSerializer, NTUT_PostsSerializer
from .models import News, Stocks, NTUT_Posts
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from .tasks import fetch_stocks

# Create your views here.
class Newslist(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.all()

@csrf_exempt
def start_scraper(request):
    if request.method == 'POST':
        fetch_stocks.delay()  # 使用 Celery 的 delay() 方法異步執行爬蟲任務
        return JsonResponse({'status': 'Scraper started'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class Stocks_latest_list(generics.ListAPIView):
    serializer_class = StocksSerializer

    def get_queryset(self):
        # 獲取每個代碼最新的 fetch_at 時間
        latest_fetch_at = Stocks.objects.values('code').annotate(latest_fetch=Max('fetch_at')).values('latest_fetch')
        # 根據最新的 fetch_at 過濾股票
        latest_stocks = Stocks.objects.filter(fetch_at__in=latest_fetch_at)
        return latest_stocks

class Stocks_history_list(generics.ListAPIView):
    serializer_class = StocksSerializer

    def get_queryset(self):
        # 獲取每個代碼最新的 fetch_at 時間
        latest_fetch_at = Stocks.objects.values('code').annotate(latest_fetch=Max('fetch_at')).values('latest_fetch')
        # 根據最新的 fetch_at 過濾掉這些記錄，獲取其他的股票歷史數據
        history_stocks = Stocks.objects.exclude(fetch_at__in=latest_fetch_at)
        return history_stocks

class NTUTPostslist(generics.ListAPIView):
    serializer_class = NTUT_PostsSerializer

    def get_queryset(self):
        return NTUT_Posts.objects.all()