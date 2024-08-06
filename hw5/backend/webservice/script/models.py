from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    datetime = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

class Stocks(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    price = models.FloatField(null=True, blank=True)  # 允许为 null 或 blank
    change = models.FloatField(null=True, blank=True)  # 允许为 null 或 blank
    change_percent = models.CharField(max_length=10, null=True, blank=True)  # 允许为 null 或 blank
    fetch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

class NTUT_Posts(models.Model):
    context = models.TextField()

    def __str__(self):
        return str(self.context)

    class Meta:
        verbose_name = "NTUT Post"
        verbose_name_plural = "NTUT Posts"