from django.contrib import admin

from .models import News, Stocks, NTUT_Posts

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime')

@admin.register(Stocks)
class StocksAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'change', 'change_percent', 'fetch_at')

@admin.register(NTUT_Posts)
class NTUT_PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'context')