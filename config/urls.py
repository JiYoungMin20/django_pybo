"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include # include 추가
# from pybo import views 
from pybo.views import base_views # 기존의 views.py 파일을 views 폴더를 만들어 분리함

urlpatterns = [
    # path('', views.index, name='index'), # / 페이지에 해당하는 urlpatterns 
    path('admin/', admin.site.urls),
    # path('pybo/', views.index),  
    path('pybo/', include('pybo.urls')), # URL 분리하기
    path('common/', include('common.urls')), # common/urls.py 파일로 유도
    path('', base_views.index, name='index'), # '/'에 해당하는 path. views 대신에 base_views 로 변경
]

handler404 = 'common.views.page_not_found'