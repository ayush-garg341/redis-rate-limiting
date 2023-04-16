"""rate_limiting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from algos.views.fixed_window import index, GetPongView
from algos.views.sliding_window import GetSlidingWindow

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/ping/", GetPongView.as_view()),
    path("fixed-window/", index, name="index"),
    path("sliding_window/", GetSlidingWindow.as_view()),
]
