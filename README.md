# 手作 DIY 社区（基于 WEB 的通用内容社区系统）

> 毕业设计·产品设计 —— 信息安全技术应用专业

一个以「手工 DIY 内容分享」为主题的前后台分离式内容社区网站。用户可发布作品、浏览点赞、评论交流、参与论坛；管理员可在定制后台对作品、分类、公告、用户、评论、论坛进行统一管理。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | HTML5 / CSS3 / 原生 JavaScript（CDN：Bootstrap Icons、Particles.js） |
| 后端 | Python 3.13 / Django 6.1 |
| 数据库 | MySQL（MariaDB 11.8） |
| 环境 | 项目内 venv 虚拟环境 |

## 功能模块

**前台（普通用户）**
- 注册 / 登录 / 退出
- 作品广场：按分类浏览、关键词搜索、查看详情
- 作品点赞、发布作品、作品评论
- 交流论坛：发帖、浏览、回复
- 社区公告浏览
- 个人中心：资料编辑、我的作品、我的帖子

**后台（管理员）**
- 仪表盘数据概览
- 作品管理（增删改查、上下架）
- 分类管理 / 公告管理
- 用户管理（启用/禁用）
- 评论管理（回复评论）
- 论坛管理（增删改查、屏蔽）

## 主题与粒子背景

- 右上角按钮可在 **深色/浅色** 主题间切换，选择持久化到 `localStorage`
- 首页背景使用 Particles.js 实现方形粒子自左向右如海浪流动的效果：
  - 深色模式：黑色背景 + 浅灰色粒子
  - 浅色模式：白色背景 + 浅蓝色粒子
  - 粒子密度适中（70 个）、方形、速度缓慢右移

## 管理员账号

- 用户名：`admin`
- 密码：`admin123`

## 环境准备与启动

### 1. 数据库（MySQL / MariaDB）

本项目使用 MySQL 兼容实现 **MariaDB 11.8.8**（Debian/Parrot 上 MySQL 的稳定替代版本）。数据库 `diy_community` 与专用账号 `diyuser` 已配置完成；root 密码为 `parrot`。

```bash
# 启动并设为开机自启（MariaDB）
printf 'parrot\n' | sudo -S -p '' systemctl enable --now mariadb

# root 密码为 parrot（若尚未设置）
printf 'parrot\n' | sudo -S -p '' mariadb -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'parrot'; FLUSH PRIVILEGES;"

# 创建数据库与专用账号（已创建过可跳过，脚本幂等可重复执行）
cat > /tmp/dbinit.sql <<'EOF'
CREATE DATABASE IF NOT EXISTS diy_community DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'diyuser'@'localhost' IDENTIFIED BY 'Diy@123456';
GRANT ALL PRIVILEGES ON diy_community.* TO 'diyuser'@'localhost';
FLUSH PRIVILEGES;
EOF
printf 'parrot\n' | sudo -S -p '' mysql < /tmp/dbinit.sql
```

### 2. Python 依赖

```bash
cd /home/parrot/Documents/web-diy-community
./venv/bin/pip install django mysqlclient Pillow
```

### 3. 初始化数据

```bash
./venv/bin/python manage.py migrate          # 建表
./venv/bin/python manage.py seed             # 创建 admin 账号 + 示例数据
```

### 4. 启动开发服务器

```bash
./venv/bin/python manage.py runserver 0.0.0.0:8000
```

访问：`http://127.0.0.1:8000/`

> 注意：MariaDB 服务已设为开机自启（`systemctl enable mariadb`），无需每次手动启动。

通过pinggy开启内网穿透 --tunnel

## 目录结构

```
web-diy-community/
├── community/          # 项目配置（settings、urls、context_processors）
├── userapp/            # 用户：注册/登录/个人中心
├── contentapp/         # 内容：作品/分类/公告
├── interactionapp/     # 交互：评论/点赞/论坛
├── adminapp/           # 管理后台 + 通用 CRUD + templatetags
├── templates/          # 前端模板（含主题切换与粒子背景）
└── static/             # CSS
```

## 测试

使用 Django 测试客户端对前台与后台主流程做了端到端验证（`/tmp/flow_test.py`），覆盖：注册、登录、评论、点赞、发帖、回帖、编辑资料、管理员登录、后台作品列表、分类/公告/评论的增删改查与回复，全部通过。

## 验收对照（毕业设计成果文档）

- 数据库表：用户、作品、分类、评论、点赞、论坛帖子、论坛回复、公告、管理员（对应成果文档 4.1–4.8 各表）
- 前台/后台功能：与成果文档 2.2「功能模块设计」一致
- 安全：密码经 Django 哈希存储，登录使用 session + CSRF 防护
