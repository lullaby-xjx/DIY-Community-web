from django.contrib import admin
from .models import Category, DiyWork, Announcement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort', 'create_time')
    search_fields = ('name',)


@admin.register(DiyWork)
class DiyWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'views', 'likes', 'status', 'create_time')
    list_filter = ('category', 'status')
    search_fields = ('title', 'content')
    list_editable = ('status',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_time')
    search_fields = ('title',)