# Member Web UI (Django)

开发与使用说明（开发者/运维指导）

先决条件
- Python 3.10+ 已安装
- 在项目根目录（本 README 所在目录）有 `Member/data/MemberList.db`，此为由 `scripts/init.py` 初始化的 SQLite 数据库。

快速开始（开发）

1. 创建并激活虚拟环境：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1  # powershell
```

2. 安装依赖：

```powershell
pip install -r requirements.txt
```

3. 运行开发服务器：

```powershell
python manage.py runserver 0.0.0.0:8000
```

4. 打开浏览器访问： http://localhost:8000/ ，你会看到成员列表页面。

关于数据库
- 项目已配置直接使用仓库中 `Member/data/MemberList.db`（相对路径）。当前示例模型设置为 `managed = False`，不会对原有数据库执行迁移或修改。

管理后台（可选）
- 若需要 Django admin：
  - 在虚拟环境中运行 `python manage.py createsuperuser` 创建管理员账号。
  - 启动服务后访问 `http://localhost:8000/admin/` 登录。

建议部署（生产）
- 将 SQLite 切换为 PostgreSQL 更可靠，使用 Gunicorn + Nginx 或 Docker 部署。可在本 README 后续补充生产化步骤。
