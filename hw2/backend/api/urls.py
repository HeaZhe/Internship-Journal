from django.urls import path
from . import views
from .views import get_current_user

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("line/login/", views.line_login, name="line-login"),
    path("line/callback/", views.line_callback, name="line-callback"),
    path("current_user/", get_current_user, name="get-user"),
]