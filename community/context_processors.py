from contentapp.models import Category, Announcement


def site_context(request):
    """全局上下文：主导航分类、最新公告"""
    return {
        'nav_categories': Category.objects.order_by('sort', 'id'),
        'latest_news': Announcement.objects.order_by('-create_time')[:5],
    }