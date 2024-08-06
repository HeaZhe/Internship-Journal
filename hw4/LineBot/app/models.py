from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100)
    Datetime = models.DateField()
    context = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title
    
class Stock(models.Model):
    stock_id = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=10)
    stock_price = models.FloatField()
    stock_change = models.FloatField()
    stock_change_rate = models.FloatField()

    def __str__(self):
        return self.stock_id
    
class NTUTPost(models.Model):
    context = models.TextField()

    def __str__(self):
        return self.title