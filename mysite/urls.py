"""mysite URL Configuration

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
from django.urls import path, include

from django.conf import settings                # settings.py 파일에 설정한 추가 경로를 사용할 수 있도록 import
from django.conf.urls.static import static      # static 경로를 사용할 수 있도록 import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("single_pages.urls")),
    path('blog/', include("blog.urls")),
    path('data/', include("data.urls")),
    path('markdownx/', include('markdownx.urls')),      # markdownx가 적용된 <textarea>의 미리보기 영역 사용을 위해 path 추가
                                                        # (path 추가를 하지 않으면 양식 작성시 미리보기 영역 부분이 404 에러남)
    path('accounts/', include('allauth.urls')),         # 별도의 인증 관련 URL 및 뷰를 직접 구현할 필요 없이, django-allauth 가 제공하는 가눙울 쉽게 통합
]

urlpatterns += static(                          # image 파일을 이용하기 위한 기본 경로 재설정.
    settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
)
