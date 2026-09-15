from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ForumTopic, ForumReply, WorkComment, LikeRecord
from contentapp.models import DiyWork


def forum_list(request):
    topics = ForumTopic.objects.filter(status=1).order_by('-create_time')
    return render(request, 'forum/list.html', {'topics': topics})


def forum_detail(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    if topic.status == 0 and not (request.user.is_staff):
        messages.error(request, '该帖子已被屏蔽')
        return redirect('forum_list')
    topic.views += 1
    topic.save(update_fields=['views'])
    replies = topic.replies.order_by('create_time')
    return render(request, 'forum/detail.html', {'topic': topic, 'replies': replies})


@login_required
def forum_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if not title or not content:
            messages.error(request, '请填写标题和内容')
            return redirect('forum_create')
        ForumTopic.objects.create(title=title, content=content, author=request.user, status=1)
        messages.success(request, '发帖成功')
        return redirect('forum_list')
    return render(request, 'forum/create.html')


@login_required
def forum_reply(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            ForumReply.objects.create(topic=topic, author=request.user, content=content)
            messages.success(request, '回复成功')
        return redirect('forum_detail', pk=pk)
    return redirect('forum_detail', pk=pk)


@login_required
def add_comment(request, work_pk):
    work = get_object_or_404(DiyWork, pk=work_pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            WorkComment.objects.create(work=work, user=request.user, content=content)
            messages.success(request, '评论成功')
        return redirect('work_detail', pk=work_pk)
    return redirect('work_detail', pk=work_pk)


@login_required
def toggle_like(request, work_pk):
    work = get_object_or_404(DiyWork, pk=work_pk)
    liked = LikeRecord.objects.filter(work=work, user=request.user).exists()
    if liked:
        LikeRecord.objects.filter(work=work, user=request.user).delete()
        work.likes = max(0, work.likes - 1)
    else:
        LikeRecord.objects.create(work=work, user=request.user)
        work.likes += 1
    work.save(update_fields=['likes'])
    return redirect('work_detail', pk=work_pk)