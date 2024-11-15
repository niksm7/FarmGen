"""
URL configuration for FarmGen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from farmapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.handleLogin, name='login'),
    path('signupuser/', views.handleSignUpUser, name='signupuser'),
    path('logout/', views.handleLogout, name='logout'),
    path('chatbot/', views.chatBotDisplay, name="chatBotDisplay"),
    path('detectdisease/', views.detectDisease, name="detectDisease"),
    path('uploadimagedisease/', views.uploadImageDisease, name="uploadImageDisease"),
    path('getbedrockresponse/', views.getBedrockResponse, name="getBedrockResponse"),
    path('getchatbotresponse/', views.getChatbotResponse, name="getChatbotResponse")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
