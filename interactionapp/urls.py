from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/create/', views.forum_create, name='forum_create'),
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:pk>/reply/', views.forum_reply, name='forum_reply'),
    path('works/<int:work_pk>/comment/', views.add_comment, name='add_comment'),
    path('works/<int:work_pk>/like/', views.toggle_like, name='toggle_like'),
]