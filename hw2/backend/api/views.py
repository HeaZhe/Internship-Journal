from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NotesSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note
import requests
from django.conf import settings
from django.shortcuts import redirect
from jose import jwt
from urllib.parse import urlencode
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({'username': user.username})    

def line_login(request):
    line_auth_url = "https://access.line.me/oauth2/v2.1/authorize"
    state = "random_string"  # 生成一個隨機字符串
    params = {
        "response_type": "code",
        "client_id": settings.LINE_CHANNEL_ID,
        "redirect_uri": settings.LINE_REDIRECT_URI,
        "state": state,
        "scope": "profile openid email",
    }
    auth_url = f"{line_auth_url}?{requests.compat.urlencode(params)}"
    return redirect(auth_url)

def line_callback(request):
    code = request.GET.get('code')
    token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LINE_REDIRECT_URI,
        "client_id": settings.LINE_CHANNEL_ID,
        "client_secret": settings.LINE_CHANNEL_SECRET,
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()
    id_token = token_data.get('id_token')

    # 解碼 ID 令牌以獲取用戶信息
    user_info = jwt.decode(id_token, settings.LINE_CHANNEL_SECRET, algorithms=['HS256'], audience=settings.LINE_CHANNEL_ID)
    line_user_id = user_info['sub']
    name = user_info.get('name', 'Line User')
    picture = user_info.get('picture', '')

    # 創建或更新用戶
    user, created = User.objects.get_or_create(username=line_user_id)
    if created:
        user.first_name = name
        user.save()

    # 生成 JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # 重定向到前端並攜帶 token
    frontend_url = "http://localhost:5173/line/callback"
    params = urlencode({
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    redirect_url = f"{frontend_url}?{params}"
    return redirect(redirect_url)