# 简化版图书馆管理系统

## 🚀 项目简介

这是一个基于Flask和Python内置sqlite3的图书馆管理系统，完全解决了SQLAlchemy版本兼容性问题，确保在Python 3.13环境下稳定运行。

## ✨ 核心功能

### 👤 用户管理
- 用户注册与登录
- 密码安全验证
- 角色权限管理（管理员/普通用户）

### 📚 图书管理
- 图书信息录入（标题、作者、ISBN、分类等）
- 图书搜索与筛选
- 图书详情查看
- 库存状态管理

### 🔄 借阅管理
- 图书借阅/归还
- 借阅历史记录
- 逾期提醒
- 借阅状态跟踪

### 🛠️ 管理员功能
- 图书信息增删改查
- 用户管理
- 借阅记录统计
- 系统数据概览

## 🛠️ 技术栈

- **后端**：Flask + Python 3.13
- **数据库**：SQLite3（Python内置）
- **前端**：Bootstrap 5 + Vanilla JavaScript
- **样式**：自定义CSS + Bootstrap组件

## 🚀 快速开始

### 1. 环境要求
- Python 3.13+
- Flask（已包含在requirements中）

### 2. 启动系统
```bash
cd library_management_system_simple
python app_simple.py
```

### 3. 访问系统
- 打开浏览器访问：http://127.0.0.1:5000
- 默认管理员账户：admin / admin123

## 📁 项目结构

```
library_management_system_simple/
├── app_simple.py                 # 主应用文件
├── requirements.txt              # 依赖包列表
├── README.md                     # 项目说明
├── templates/                    # HTML模板
│   ├── base_simple.html         # 基础模板
│   ├── index_simple.html        # 首页
│   ├── login_simple.html        # 登录页
│   ├── register_simple.html     # 注册页
│   ├── books_simple.html        # 图书列表
│   ├── book_detail_simple.html  # 图书详情
│   ├── my_loans_simple.html     # 我的借阅
│   └── admin_simple.html        # 管理员面板
└── static/                      # 静态文件
    ├── css/
    │   └── style_simple.css    # 自定义样式
    └── js/
        └── main_simple.js       # JavaScript功能
```

## 🎯 解决的问题

### ❌ 原问题
- SQLAlchemy版本兼容性问题
- Python 3.13环境下AssertionError
- 复杂依赖管理

### ✅ 解决方案
- 使用Python内置sqlite3数据库
- 简化依赖，避免版本冲突
- 保持完整功能体验

## 🔧 核心特性

### 💾 数据库设计
- **用户表**：用户信息、角色权限
- **图书表**：图书基本信息、库存状态
- **借阅表**：借阅记录、状态跟踪

### 🔐 安全特性
- 密码哈希存储
- 会话管理
- 表单验证
- SQL注入防护

### 📱 响应式设计
- 移动端友好
- 现代化界面
- 交互式组件
- 实时反馈

## 🏃‍♂️ 使用指南

### 管理员操作
1. 使用admin/admin123登录
2. 在管理员面板管理图书
3. 查看借阅统计
4. 管理用户账户

### 普通用户操作
1. 注册新账户或使用示例账户
2. 浏览图书列表
3. 搜索感兴趣图书
4. 申请借阅图书
5. 查看个人借阅历史

## 🎨 界面预览

- **首页**：系统介绍和功能概览
- **登录页**：简洁的登录表单
- **图书页**：网格布局的图书展示
- **借阅页**：个人借阅记录管理
- **管理页**：数据统计和管理操作

## 🔄 升级说明

相比原版本，此简化版：
- ✅ 解决了兼容性问题
- ✅ 保持了核心功能
- ✅ 优化了性能表现
- ✅ 简化了部署流程

## 📞 技术支持

如有问题，请检查：
1. Python版本是否≥3.13
2. Flask是否正确安装
3. 防火墙是否阻止5000端口
4. 数据库文件权限是否正确

---

**开发完成时间**：2024年
**Python版本**：3.13.5
**Flask版本**：最新稳定版