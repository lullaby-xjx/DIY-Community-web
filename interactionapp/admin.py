from django.contrib import admin
from .models import WorkComment, ForumTopic, ForumReply, LikeRecord


@admin.register(WorkComment)
class WorkCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'work', 'user', 'create_time', 'reply')
    search_fields = ('content',)


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'views', 'status', 'create_time')
    list_filter = ('status',)
    search_fields = ('title', 'content')
    list_editable = ('status',)


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'author', 'create_time')
    search_fields = ('content',)


@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'work', 'user', 'create_time')