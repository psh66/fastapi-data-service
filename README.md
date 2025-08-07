```markdown
# FastAPI CRUD Base 项目说明

## 项目介绍
FastAPI CRUD Base 是一个基于 FastAPI 框架构建的基础 CRUD（创建、读取、更新、删除）应用程序模板。它提供了快速搭建 RESTful API 的基础结构，包含用户认证、数据库操作等常用功能，可作为开发各类 Web 应用的起点。

## 环境准备
### 安装 Python
确保你的系统中安装了 Python 3.7 及以上版本。可以从 [Python 官方网站](https://www.python.org/) 下载并安装。

### 创建虚拟环境
在项目目录下打开命令行终端，运行以下命令创建虚拟环境（以 `venv` 为例）：
- **Windows 系统**：
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **Linux/macOS 系统**：
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

## 安装依赖插件
### 依赖说明
项目依赖以下核心工具库，各库的作用如下：
- **FastAPI**：现代、高性能的 Python Web 框架，用于快速构建 API 接口，支持自动生成接口文档。
- **Uvicorn**：轻量级 ASGI 服务器，负责运行 FastAPI 应用，支持异步请求处理。
- **SQLAlchemy**：强大的 SQL 工具包和对象关系映射（ORM）库，简化数据库操作，支持多种数据库（如 MySQL、PostgreSQL、SQLite 等）。
- **Pydantic**：基于类型提示的数据验证库，与 FastAPI 深度集成，确保接口输入输出数据的合法性。
- **Pydantic-Settings**：Pydantic 的扩展库，用于管理应用配置（如环境变量、配置文件），支持类型验证。
- **Email-Validator**：用于验证电子邮件地址格式，在用户注册、密码找回等场景中确保邮箱合法性。
- **Python-Multipart**：处理 HTTP 多部分表单数据，支持文件上传功能，是 FastAPI 处理文件上传的依赖项。

### 安装方式
#### 方式 1：通过 requirements.txt 一键安装（推荐）
项目根目录下需创建 `requirements.txt` 文件，内容如下：
```txt
# 核心框架
fastapi>=0.100.0
# 运行服务器
uvicorn>=0.23.0
# 数据库 ORM
sqlalchemy>=2.0.0
# 数据验证
pydantic>=2.0.0
# 配置管理
pydantic-settings>=2.0.0
# 邮箱验证
email-validator>=2.0.0
# 文件上传支持
python-multipart>=0.0.6
```
创建完成后，运行以下命令安装所有依赖：
```bash
pip install -r requirements.txt
```

#### 方式 2：单独安装（按需选择）
若需单独安装某个依赖，可使用以下命令：
```bash
# 安装 FastAPI
pip install fastapi

# 安装 Uvicorn
pip install uvicorn

# 安装 SQLAlchemy
pip install sqlalchemy

# 安装 Pydantic
pip install pydantic

# 安装 Pydantic-Settings
pip install pydantic-settings

# 安装 Email-Validator
pip install email-validator

# 安装 Python-Multipart
pip install python-multipart

# 1. 处理 JWT 等加密逻辑（报错提示缺少 `jose`）  
pip install python-jose  

# 2. 处理密码哈希/验证（报错提示缺少 `passlib`）  
pip install passlib  
```

是！Python 版本差异会导致 **依赖包兼容性问题**（如某些包对 Python 3.11 支持不全，或语法适配问题）。  

### 解决步骤（极简版）：  
1. **确认项目要求的 Python 版本**（看文档/`README`，若没写，尝试 `Python 3.10` 通用兼容版）。  
2. **新建对应版本的虚拟环境**（假设项目需要 `Python 3.10`）：  
   ```bash
   # 先退出当前虚拟环境
   deactivate  
   # 用 Python 3.10 创建新虚拟环境（路径按需改）
   C:\Python310\python.exe -m venv venv_py310  
   # 激活（Windows PowerShell）
   .\venv_py310\Scripts\activate  
   ```  
3. **强制重装依赖**（用新版 `pip` + 清缓存）：  
   ```bash
   pip install --upgrade pip  
   pip cache purge  
   pip install -r requirements.txt  
   ```  


### 关键逻辑：  
- 若原项目基于 `Python 3.10` 开发，`3.11` 可能触发包的**语法/API 兼容问题**（如 `pydantic` 旧版对 `3.11` 支持不足）。  
- 换环境后仍报错 → 逐个替换 `requirements.txt` 里的包为**兼容版本**（比如 `pydantic==2.0.0` 改 `pydantic==1.10.12` 适配旧 Python）。  

（本质：Python 大版本迭代会引发依赖适配问题，“切版本+清环境”是最快验证方式 ）

## 配置环境变量
### 必要环境变量说明
项目运行需配置以下关键环境变量（建议在项目根目录的 `.env` 文件中配置，配合 `pydantic-settings` 读取）：
- `DATABASE_URL`：数据库连接地址（如 `sqlite:///./test.db` 或 `postgresql://user:password@localhost/dbname`）
- `SECRET_KEY`：用于加密认证信息的密钥（可通过 `openssl rand -hex 32` 生成）
- `ALGORITHM`：加密算法（如 `HS256`）
- `ACCESS_TOKEN_EXPIRE_MINUTES`：访问令牌过期时间（单位：分钟）

### 配置方式
#### 方式 1：通过 .env 文件配置（推荐）
在项目根目录创建 `.env` 文件，添加以下内容（替换为实际值）：
```env
DATABASE_URL=sqlite:///./fastapi_crud_base.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 方式 2：系统环境变量配置
##### Windows 系统
1. 右键点击“此电脑”→“属性”→“高级系统设置”→“环境变量”；
2. 在“用户变量”或“系统变量”区域点击“新建”；
3. 依次添加以下变量：
   - 变量名：`DATABASE_URL`，变量值：`sqlite:///./fastapi_crud_base.db`（或实际数据库地址）
   - 变量名：`SECRET_KEY`，变量值：你的密钥
   - 变量名：`ALGORITHM`，变量值：`HS256`
   - 变量名：`ACCESS_TOKEN_EXPIRE_MINUTES`，变量值：`30`
   - 变量名：`PYTHONPATH`，变量值：项目路径（如 `D:\project\fastapi-crud-base`）
4. 点击“确定”保存设置。

##### Linux/macOS 系统
1. 打开终端，编辑 `~/.bashrc` 或 `~/.zshrc` 文件（根据使用的 shell）；
2. 添加以下内容（替换为实际值）：
   ```bash
   export DATABASE_URL="sqlite:///./fastapi_crud_base.db"
   export SECRET_KEY="your-secret-key-here"
   export ALGORITHM="HS256"
   export ACCESS_TOKEN_EXPIRE_MINUTES=30
   export PYTHONPATH="/path/to/your/project"
   ```
3. 运行命令使更改生效：
   ```bash
   source ~/.bashrc  # 或 source ~/.zshrc
   ```

## 运行项目
1. 确保 FastAPI 应用主文件（如 `main.py`）已正确编写；
2. 在虚拟环境激活状态下启动应用：
   ```bash
   uvicorn main:app --reload
   ```
   （`main` 为主文件名，`app` 为 FastAPI 实例，`--reload` 实现开发模式自动重启）；
3. 打开浏览器访问 `http://127.0.0.1:8000`（或配置的其他地址端口），看到默认响应即运行成功；
4. 访问 `http://127.0.0.1:8000/docs` 可查看自动生成的接口文档。

## 项目结构说明
```plaintext
fastapi-crud-base/
├── app/
│   ├── __init__.py
│   ├── main.py          # 应用程序入口
│   ├── api/             # API 路由
│   │   ├── __init__.py
│   │   └── v1/          # API 版本 1
│   │       ├── __init__.py
│   │       ├── endpoints/  # 端点定义
│   │       │   ├── __init__.py
│   │       │   └── auth.py # 认证相关端点
│   │       └── router.py   # 路由定义
│   ├── crud/            # CRUD 操作
│   │   ├── __init__.py
│   │   └── user.py      # 用户相关 CRUD
│   ├── models/          # 数据库模型
│   │   ├── __init__.py
│   │   └── user.py      # 用户模型
│   ├── schemas/         # 数据模式
│   │   ├── __init__.py
│   │   └── user.py      # 用户数据模式
│   └── core/            # 核心配置
│       ├── __init__.py
│       └── config.py    # 配置文件（读取环境变量）
├── tests/               # 测试文件
│   └── __init__.py
├── .env                 # 环境变量配置文件（本地开发用）
├── .gitignore           # Git 忽略文件（包含 .env、venv 等）
├── requirements.txt     # 依赖列表（一键安装：pip install -r requirements.txt）
└── README.md            # 项目说明
```

## 
git clone https://github.com/psh66/fastapi-data-service.git

# 检查接口文档：
访问 http://127.0.0.1:8000/docs 查看所有可用的接口文档，确保 demo 模块的接口已正确注册。

# 演示接口地址
获取所有演示项目列表：http://127.0.0.1:8000/api/v1/demo/items/
获取单个演示项目（替换 {item_id} 为具体 ID，如 1）：http://127.0.0.1:8000/api/v1/demo/items/{item_id}
创建新演示项目：http://127.0.0.1:8000/api/v1/demo/items/
更新指定演示项目：http://127.0.0.1:8000/api/v1/demo/items/{item_id}
删除指定演示项目：http://127.0.0.1:8000/api/v1/demo/items/{item_id} 

## 许可证
本项目采用 MIT 许可证 - 详情请查看 LICENSE 文件。
```