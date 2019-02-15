"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.contrib import admin

app_name = 'movie'

urlpatterns = [ path('', views.list, name="list") ,
				path('login/', views.login_user, name="login"),
				path('logout/', views.logout_user, name="logout"),
				path('register/', views.reg_user, name="register"),
				path('session/',views.session,name="session"),
				path('session/<int:id>/explore/',views.explore,name="explore"),
				path('session/recommend/',views.recommend,name="recommend")   
]