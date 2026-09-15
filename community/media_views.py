"""支持 HTTP Range 请求的媒体文件服务。

Django 内置的 static() 开发服务器不支持 Range 请求（总是返回 200 完整文件），
导致浏览器无法分段播放视频（拖动进度条 / 边下边播）。此视图补齐 206 Partial Content 支持。
"""
import os
import re
import mimetypes

from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings
from django.utils.http import http_date


def serve_media(request, path):
    """为 MEDIA_ROOT 下的文件提供支持 Range 的下载服务。"""
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    # 规范化并防路径穿越
    full_path = os.path.abspath(os.path.join(media_root, path))
    if not full_path.startswith(media_root) or not os.path.isfile(full_path):
        raise Http404('File not found')

    content_type, _ = mimetypes.guess_type(full_path)
    if not content_type:
        content_type = 'application/octet-stream'

    size = os.path.getsize(full_path)
    range_header = request.META.get('HTTP_RANGE', '')
    match = re.match(r'bytes=(\d*)-(\d*)', range_header.strip())

    if match:
        start_s, end_s = match.groups()
        start = int(start_s) if start_s else None
        end = int(end_s) if end_s else None
        if start is None:  # 后缀范围：bytes=-N 表示最后 N 字节
            start = max(0, size - end)
            end = size - 1
        else:
            if end is None:
                end = size - 1
            end = min(end, size - 1)
        if start > end or start >= size:
            resp = HttpResponse(status=416)
            resp['Content-Range'] = f'bytes */{size}'
            return resp
        length = end - start + 1
        resp = HttpResponse(status=206)
        resp['Content-Range'] = f'bytes {start}-{end}/{size}'
        resp['Accept-Ranges'] = 'bytes'
        resp['Content-Length'] = str(length)
        resp['Content-Type'] = content_type
        resp['Last-Modified'] = http_date(os.path.getmtime(full_path))
        with open(full_path, 'rb') as f:
            f.seek(start)
            resp.content = f.read(length)
        return resp

    # 无 Range 头：返回完整文件
    resp = FileResponse(open(full_path, 'rb'), content_type=content_type)
    resp['Accept-Ranges'] = 'bytes'
    resp['Content-Length'] = str(size)
    resp['Last-Modified'] = http_date(os.path.getmtime(full_path))
    return resp