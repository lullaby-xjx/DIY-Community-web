from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """作品分类"""
    name = models.CharField(max_length=50, verbose_name='分类名称')
    sort = models.IntegerField(default=0, verbose_name='排序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '作品分类'
        verbose_name_plural = '作品分类'
        ordering = ['sort', 'id']

    def __str__(self):
        return self.name


class DiyWork(models.Model):
    """DIY 作品/文章"""
    TYPE_ARTICLE = 'article'
    TYPE_VIDEO = 'video'
    TYPE_CHOICES = [
        (TYPE_ARTICLE, '图文'),
        (TYPE_VIDEO, '视频'),
    ]
    title = models.CharField(max_length=200, verbose_name='标题')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='封面图')
    work_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_ARTICLE, verbose_name='作品类型')
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name='视频文件')
    summary = models.CharField(max_length=300, blank=True, default='', verbose_name='简介')
    content = models.TextField(verbose_name='正文')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='works', verbose_name='分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='works', verbose_name='作者')
    views = models.IntegerField(default=0, verbose_name='浏览数')
    likes = models.IntegerField(default=0, verbose_name='点赞数')
    status = models.IntegerField(default=1, verbose_name='状态')  # 1=发布 0=下架
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '作品'
        verbose_name_plural = '作品'
        ordering = ['-create_time']

    def __str__(self):
        return self.title

    @property
    def video_url(self):
        return self.video.url if self.video else ''

    @property
    def is_video(self):
        return self.work_type == self.TYPE_VIDEO


class WorkAttachment(models.Model):
    """作品附件（压缩包/文件）"""
    work = models.ForeignKey(DiyWork, on_delete=models.CASCADE, related_name='attachments', verbose_name='作品')
    name = models.CharField(max_length=200, verbose_name='文件名')
    file = models.FileField(upload_to='attachments/', verbose_name='文件')
    size = models.BigIntegerField(default=0, verbose_name='大小(字节)')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '作品附件'
        verbose_name_plural = '作品附件'
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """公告"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-create_time']

    def __str__(self):
        return self.title