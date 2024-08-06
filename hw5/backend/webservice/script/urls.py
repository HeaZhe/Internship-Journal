from django.urls import path
from . import views
from .views import start_scraper

urlpatterns = [
    path("news/", views.Newslist.as_view(), name="news-list"),
    path('start_scraper/', start_scraper, name='start_scraper'),
    path("stocks_latest/", views.Stocks_latest_list.as_view(), name="stocks-latest"),
    path("stocks_history/", views.Stocks_history_list.as_view(), name="stocks-history"),
    path("ntut_posts/", views.NTUTPostslist.as_view(), name="ntut-posts_list"),
]