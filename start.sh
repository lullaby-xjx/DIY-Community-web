#!/usr/bin/env bash
# ============================================================
# 手作 DIY 社区 —— 一键启动脚本
# 自动检查依赖、数据库、迁移与 seed（幂等），最后启动服务器
# 用法：
#   ./start.sh            # 前台启动开发服务器
#   ./start.sh --tunnel   # 额外开启 pinggy 短暂内网穿透（公网 URL）
# ============================================================

set -e

# 定位项目根目录（脚本所在目录）
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 是否开启内网穿透
TUNNEL=0
case "$1" in
  --tunnel|-t) TUNNEL=1 ;;
esac

PY="$PROJECT_DIR/venv/bin/python"
PIP="$PROJECT_DIR/venv/bin/pip"

echo "==> 项目目录: $PROJECT_DIR"

# ---------- 1. 检查 venv ----------
if [ ! -x "$PY" ]; then
    echo "[错误] 未找到虚拟环境 $PY" >&2
    echo "       请先创建 venv：python3 -m venv venv" >&2
    exit 1
fi

# ---------- 2. 检查/补齐 Python 依赖 ----------
if ! "$PY" -c "import django" >/dev/null 2>&1; then
    echo "==> 未检测到 Django，正在安装依赖..."
    "$PIP" install django mysqlclient Pillow
fi

# ---------- 3. 检查数据库 ----------
if ! systemctl is-active mariadb >/dev/null 2>&1 && ! systemctl is-active mysql >/dev/null 2>&1; then
    echo "[提示] MariaDB/MySQL 未运行，请先启动："
    echo "       sudo systemctl enable --now mariadb"
    exit 1
fi

# ---------- 4. 迁移与初始化（幂等） ----------
echo "==> 执行数据库迁移..."
"$PY" manage.py migrate

if ! "$PY" manage.py shell -c \
    "from django.contrib.auth.models import User; \
import sys; sys.exit(0 if User.objects.filter(username='admin').exists() else 1)" \
    >/dev/null 2>&1; then
    echo "==> 未找到 admin 账号，执行 seed 初始化..."
    "$PY" manage.py seed
else
    echo "==> admin 账号已存在，跳过 seed。"
fi

# ---------- 5. 启动开发服务器 ----------
echo "==> 启动开发服务器：http://127.0.0.1:8000/"

if [ "$TUNNEL" = "1" ]; then
    # ---- 内网穿透模式 ----
    # 后台启动 Django，前台保持 ssh 隧道（用户可见公网 URL，Ctrl+C 一并退出）
    "$PY" manage.py runserver 0.0.0.0:8000 > /tmp/diy_django.log 2>&1 &
    DJANGO_PID=$!

    cleanup() {
        echo ""
        echo "==> 正在关闭开发服务器..."
        kill "$DJANGO_PID" 2>/dev/null || true
        wait "$DJANGO_PID" 2>/dev/null || true
    }
    trap cleanup INT TERM EXIT

    if ! command -v ssh >/dev/null 2>&1; then
        echo "[错误] 未找到 ssh 命令，无法建立内网穿透。" >&2
        exit 1
    fi

    echo "==> 正在通过 pinggy 建立内网穿透（免费通道）..."
    echo "==> 若提示输入密码，直接按回车即可（空密码）。"
    echo "==> 连接成功后上方会出现类似 https://xxxx.run.pinggy-free.link 的公网地址。"
    echo "==> Django 服务器日志：/tmp/diy_django.log"
    echo "    按 Ctrl+C 可一并关闭服务器并断开隧道。"
    echo ""

    # -R0:localhost:8000 把 pinggy 公网请求转发到本机 8000 端口
    ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=30 \
        -o ServerAliveCountMax=3 \
        -p 443 -R0:localhost:8000 \
        free.pinggy.io
else
    # ---- 默认前台模式 ----
    exec "$PY" manage.py runserver 0.0.0.0:8000
fi