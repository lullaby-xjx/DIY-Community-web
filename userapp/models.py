from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """用户扩展资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    points = models.IntegerField(default=0, verbose_name='积分')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return self.user.username