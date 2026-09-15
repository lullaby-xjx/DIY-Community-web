from django.db import models
from django.contrib.auth.models import User
from contentapp.models import DiyWork


class WorkComment(models.Model):
    """作品评论"""
    work = models.ForeignKey(DiyWork, on_delete=models.CASCADE, related_name='comments', verbose_name='作品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_comments', verbose_name='评论人')
    content = models.TextField(verbose_name='评论内容')
    reply = models.TextField(blank=True, null=True, verbose_name='管理员回复')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    reply_time = models.DateTimeField(blank=True, null=True, verbose_name='回复时间')

    class Meta:
        verbose_name = '作品评论'
        verbose_name_plural = '作品评论'
        ordering = ['-create_time']

    def __str__(self):
        return self.content[:30]


class ForumTopic(models.Model):
    """论坛帖子"""
    title = models.CharField(max_length=200, verbose_name='帖子标题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_topics', verbose_name='作者')
    content = models.TextField(verbose_name='内容')
    views = models.IntegerField(default=0, verbose_name='浏览数')
    status = models.IntegerField(default=1, verbose_name='状态')  # 1=正常 0=屏蔽
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发帖时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '论坛帖子'
        verbose_name_plural = '论坛帖子'
        ordering = ['-create_time']

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    """论坛回复"""
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies', verbose_name='帖子')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies', verbose_name='回复人')
    content = models.TextField(verbose_name='回复内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')

    class Meta:
        verbose_name = '论坛回复'
        verbose_name_plural = '论坛回复'
        ordering = ['create_time']

    def __str__(self):
        return self.content[:30]


class LikeRecord(models.Model):
    """点赞记录（防止重复点赞）"""
    work = models.ForeignKey(DiyWork, on_delete=models.CASCADE, related_name='like_records', verbose_name='作品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_records', verbose_name='用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = '点赞记录'
        constraints = [
            models.UniqueConstraint(fields=['work', 'user'], name='unique_work_user_like')
        ]

    def __str__(self):
        return f'{self.user.username} 赞 {self.work.title}'