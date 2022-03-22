"""ProfRate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
#from ProfRateApp.views import HandleRegisterRequest, HandleLoginRequest, HandleLogoutRequest, ViewModules, ViewProfRatings, ViewAvrgProfModuleRatings, GiveRating
from ProfRateApp.views import *
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/register/', HandleRegisterRequest),
#     path('api/login/', HandleLoginRequest),
#     path('api/logout/', HandleLogoutRequest),
#     path('api/list/', ViewModules),
#     path('api/view/', ViewProfRatings),
#     path('api/average/', ViewAvrgProfModuleRatings),
#     path('api/rate/', GiveRating),
#     ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('list', list.as_view()),
    path('view', view.as_view()),
    path('average', average.as_view()),
    path('register', register.as_view()),
    path('login', login.as_view()),
    path('rate', rate.as_view()),
    path('check_user', check_user.as_view()),
    path('logout_user', logout_user.as_view()),
    # path('check', views.check_login, name='check_login'),
    # path('accounts/', include('django.contrib.auth.urls'))
]