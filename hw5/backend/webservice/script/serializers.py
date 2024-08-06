from rest_framework import serializers
from .models import News, Stocks, NTUT_Posts


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'datetime']

class StocksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stocks
        fields = ['id', 'name', 'code', 'price', 'change', 'change_percent', 'fetch_at']

class NTUT_PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NTUT_Posts
        fields = ['context']
