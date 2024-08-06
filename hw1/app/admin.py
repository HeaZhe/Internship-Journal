from django.contrib import admin

from .models import Context

class ContextAdmin(admin.ModelAdmin):
    list_display = ('id', 'Context_text', 'Created_date','Delete_date')  # 'Add other field names you want to display

admin.site.register(Context, ContextAdmin)