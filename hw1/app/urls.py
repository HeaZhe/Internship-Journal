from django.urls import path

from . import views
from .views import DeleteContextView, EditContextView

app_name = "app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add_context/", views.AddContextView.as_view(), name="add_context"),
    path('delete_context/<int:context_id>/', DeleteContextView.as_view(), name='delete_context'),
    path('edit_context/<int:context_id>/', EditContextView.as_view(), name='edit_context'),
    #path('delete_context/', DeleteContextView.as_view(), name='delete_context'),
    #path('edit_context/', EditContextView.as_view(), name='edit_context'),
]