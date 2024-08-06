### 後端

## 建立虛擬環境

python3 -m venv env

## 啟動虛擬環境

.\env\Scripts\Activate

## 建立requirements.txt一鍵安裝需要的package

## 建立Django project and app

django-admin startproject "project-name"

python manage.py startapp "app-name" or django-admin startapp "app-name"

## 重要指令
python manage.py migrate
python manage.py makemigrations
python manage.py runserver

## 定時任務celery
celery是什麼
一種讓異步處理任務的工具
主要應用情境為以下:
任務調度 (例如: 寄信這種會比較需要等待的事情)
定時任務

需安裝redis服務
執行
redis-server
啟動redis伺服器

先啟動Django > worker > beat
celery -A webservice worker -l info
celery -A webservice worker -l info -P eventlet
celery -A webservice beat -l info
celery -A webservice beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
目錄結構
    |   manage.py
    \---ProjectName
            asgi.py
            settings.py
            urls.py
            wsgi.py
            __init__.py
            ★ celery.py
    \---AppName
        tasks.py (名稱tasks為預設)

### 前端

npm create vite@latest frontend -- --template react

# JSON Web Token (JWT)

何謂JWT?

JWT是一種開放標準(RFC 7519)，用於在各方之間以JSON物件的形式安全地傳輸資訊
JWT可以使用HMAC演算法、RSA或ECDSA的公鑰/私鑰對進行簽署

JWT驗證成功後發出的憑證包含以下三部分：

- Header    - 標記token的類型與雜湊函示名稱
- Payload   - 要攜帶的資料，例如user_id與時間，也可以指定token的過期時間
- Signature - 根據Header和Payload，加上密鑰進行雜湊，產生一組不可反解的亂數，當成簽章，用來驗證JWT是否經過竄改。

Header及Payload採用的是Base64URL編碼機制，此編碼機制是可以反解的

# OAuth 2.0 && OIDC

何謂OAuth 2.0

OAuth 是第三方的認證協議

何謂OIDC(OpenID Connect)

OIDC 是基於OAuth 2.0的一種身分認證協議

### Git 

何謂Git

Git 是一種版本控制工具

# 配置Git

設置用戶名稱
git config --global user.name "Name"
設置電子郵件
git config --global user.email "example@example.com"

初始化項目
git init

# 克隆Public倉庫
git clone "https://github.com/{user.name}/{repository.name}.git"

# 克隆Private倉庫

First need to use cmd to Create a ssh-key

ssh-keygen -t rsa -b 4096 -C "example@example.com"
Go to Copy ~/.ssh/id_rsa.pub
Go to the Github > Settings > SSH and GPG keys
Click New SSH key and Paste to Key

last
git clone git@github.com:{user.name}/{repository.name}.git


### 基本指令
添加文件
git add "filename"

添加當前目錄所有文件
git add .

提交更改
git commit -m "提交訊息"

還原提交
git rever commit-hash

查看狀態
git status

查看日誌
git log

### 分支管理

創建新分支
git branch new-branch

切換到新分支
git checkout new-branch

創建並切換到新分支
git checkout -b new-branch

合併分支
git merge branch-name

刪除分支
git branch -d branch-name

刪除遠程分支
git push origin --delete branch-name

### 遠程倉庫

添加遠程倉庫
git remote add origin https://github.com/{user.name}/{repository.name}.git

查看當前遠程倉庫
git remote -v

推送更改到遠程倉庫
git push origin branch-name

從遠程倉庫拉取更改
git pull origin branch-name

推送標籤到遠程倉庫
git push origin --tags

# 標籤

創建標籤
git tag -a v1.0 -m "版本1.0"

### 儲存變更

臨時保存更改
git stash

應用儲藏的更改
git stash apply

### 查看差異

提交之間的變更
git diff commit commit2

查看工作目錄的變更
git diff

### Git Work Flow

clone repository
