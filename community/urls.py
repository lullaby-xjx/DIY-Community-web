from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import media_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contentapp.urls')),
    path('', include('userapp.urls')),
    path('', include('interactionapp.urls')),
    path('', include('adminapp.urls')),
]

if settings.DEBUG:
    # 用支持 Range 请求的视图服务媒体文件（保证视频可拖动/分段播放）
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', media_views.serve_media))