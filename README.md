# LibraryManager - 智慧图书馆管理系统

<div align="center">

![LibraryManager Logo](https://img.shields.io/badge/LibraryManager-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一个现代化的图书馆管理系统，提供完整的图书管理和借阅服务。

[功能特色](#-功能特色) • [快速开始](#-快速开始) • [在线演示](#-在线演示) • [贡献指南](#-贡献指南)

</div>

---

## 📋 项目简介

**LibraryManager** 是一个基于 Python Flask 开发的现代化图书馆管理系统，旨在为图书馆工作人员和读者提供高效、便捷的图书管理解决方案。

### 🎯 设计理念
- **简洁易用** - 直观友好的用户界面
- **功能完整** - 覆盖图书管理全流程
- **轻量部署** - 零配置，开箱即用
- **响应式设计** - 完美适配各种设备

---

## ✨ 功能特色

### � 用户管理
- ✅ 用户注册与登录
- ✅ 角色权限管理（普通用户/管理员）
- ✅ 用户信息维护
- ✅ 密码安全加密

### 📚 图书管理
- ✅ 图书信息录入与编辑
- ✅ 图书分类管理
- ✅ 图书搜索与筛选
- ✅ 图书状态跟踪
- ✅ 批量导入功能

### � 借阅管理
- ✅ 在线借书申请
- ✅ 借阅记录管理
- ✅ 归还处理
- ✅ 逾期提醒
- ✅ 借阅历史查询

### � 管理员功能
- ✅ 系统设置管理
- ✅ 用户权限控制
- ✅ 数据统计分析
- ✅ 图书库存管理
- ✅ 借阅报表生成

### 🎨 界面特色
- ✅ 现代化响应式设计
- ✅ Bootstrap 5 框架
- ✅ 移动端友好界面
- ✅ 直观的操作流程
- ✅ 美观的视觉设计

---

## 🚀 快速开始

### 环境要求
- Python 3.13 或更高版本
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/LibraryManager.git
cd LibraryManager
```

2. **安装依赖**（本项目使用Python内置库，无需额外安装）
```bash
# 本项目零依赖，仅使用Python标准库
# Python 3.13+ 已包含所需的所有模块
```

3. **启动应用**
```bash
python app_simple.py
```

4. **访问系统**
打开浏览器访问：http://127.0.0.1:5000

### 默认账户

| 用户类型 | 用户名 | 密码 | 权限 |
|---------|--------|------|------|
| 管理员 | admin | admin123 | 完整系统权限 |
| 测试用户 | user1 | user123 | 基础借阅功能 |

---

## 🛠️ 技术栈

### 后端技术
- **Python 3.13+** - 现代化编程语言
- **Flask** - 轻量级Web框架
- **SQLite3** - 嵌入式数据库
- **Werkzeug** - 安全密码哈希

### 前端技术
- **HTML5** - 现代网页标准
- **Bootstrap 5** - 响应式UI框架
- **JavaScript (ES6+)** - 交互功能
- **CSS3** - 样式设计

### 特色解决方案
- **零依赖设计** - 使用Python标准库
- **SQLite集成** - 无需额外数据库服务
- **响应式布局** - 移动端完美适配
- **安全认证** - 密码哈希与权限控制

---

## 📁 项目结构

```
LibraryManager/
├── 📄 app_simple.py              # 主应用程序
├── 📄 library.db                 # SQLite数据库文件
├── 📄 database_test.py           # 数据库测试脚本
├── 📄 SQLTools配置指南.md         # 数据库管理指南
├── 📄 SQLTools驱动安装指南.md     # SQLTools安装指南
├── 📁 static/                    # 静态资源目录
│   └── 📁 js/
│       └── 📄 main_simple.js     # 前端脚本
├── 📁 templates/                 # 模板文件目录
│   ├── 📄 base_simple.html       # 基础模板
│   ├── 📄 index_simple.html      # 首页模板
│   ├── 📄 login_simple.html      # 登录页面
│   ├── 📄 register_simple.html   # 注册页面
│   ├── 📄 books_simple.html      # 图书列表
│   ├── 📄 book_detail_simple.html # 图书详情
│   ├── 📄 my_loans_simple.html   # 我的借阅
│   └── 📄 admin_simple.html      # 管理面板
└── 📄 README.md                  # 项目说明文档
```

---

## 🔧 核心功能详解

### 用户认证系统
```python
# 密码安全哈希
from werkzeug.security import generate_password_hash, check_password_hash

# 用户登录验证
def login_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        return create_session(user)
    return None
```

### 数据库设计
```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 图书表
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(50),
    available BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 借阅记录表
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP,
    due_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
);
```

### API 接口设计
```python
# 图书管理API
@app.route('/api/books', methods=['GET'])
def get_books():
    """获取图书列表"""
    books = get_all_books()
    return jsonify(books)

@app.route('/api/books', methods=['POST'])
def create_book():
    """创建新图书"""
    data = request.get_json()
    book_id = add_book(data)
    return jsonify({"id": book_id, "status": "created"})

# 借阅管理API
@app.route('/api/loans', methods=['POST'])
def create_loan():
    """创建借阅记录"""
    data = request.get_json()
    loan_id = add_loan(data)
    return jsonify({"id": loan_id, "status": "active"})
```

---

## 📊 数据库管理

### 使用SQLTools连接
1. 安装SQLTools插件（VS Code）
2. 安装SQLite驱动程序
3. 添加连接：
   - **连接名称**: LibraryManager Database
   - **数据库路径**: `./library.db`
   - **驱动类型**: SQLite

### 常用查询语句
```sql
-- 查看所有图书
SELECT * FROM books ORDER BY created_at DESC;

-- 查看活跃借阅
SELECT l.*, u.username, b.title 
FROM loans l
JOIN users u ON l.user_id = u.id
JOIN books b ON l.book_id = b.id
WHERE l.status = 'active';

-- 统计借阅数据
SELECT 
    COUNT(*) as total_loans,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_loans,
    COUNT(CASE WHEN return_date IS NOT NULL THEN 1 END) as returned_loans
FROM loans;

-- 用户借阅统计
SELECT u.username, COUNT(l.id) as loan_count
FROM users u
LEFT JOIN loans l ON u.id = l.user_id
GROUP BY u.id, u.username
ORDER BY loan_count DESC;
```

---

## 🎯 功能演示

### 用户端功能
1. **注册登录** - 安全的用户认证
2. **浏览图书** - 分类搜索图书信息
3. **借阅申请** - 在线借书申请流程
4. **个人中心** - 查看借阅历史和状态

### 管理员功能
1. **图书管理** - 添加、编辑、删除图书
2. **用户管理** - 用户权限和账户管理
3. **借阅处理** - 审核借阅申请
4. **数据统计** - 借阅报表和分析

### 界面预览
- **响应式设计** - 桌面端和移动端完美适配
- **现代化UI** - Bootstrap 5 带来的美观界面
- **直观操作** - 简化的工作流程

---

## 🧪 测试与验证

### 数据库连接测试
```bash
python database_test.py
```

### 功能验证清单
- [ ] 用户注册登录功能
- [ ] 图书添加和编辑
- [ ] 借阅申请流程
- [ ] 管理员权限控制
- [ ] 响应式界面适配
- [ ] 数据持久化存储

### 性能特点
- **快速启动** - 无需复杂配置
- **轻量运行** - 低内存占用
- **稳定存储** - SQLite事务安全
- **并发支持** - 多用户同时使用

---

## 🤝 贡献指南

### 参与贡献
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范
- 遵循 PEP 8 Python 代码规范
- 添加适当的注释和文档
- 确保新功能包含测试用例
- 更新相关的文档内容

### 问题反馈
如果您遇到问题或有改进建议，请：
1. 查看 [Issues](https://github.com/yourusername/LibraryManager/issues) 页面
2. 创建新的 Issue 详细描述问题
3. 提供错误信息和复现步骤

---

## 📈 路线图

### 近期计划 (v1.1)
- [ ] 添加图书封面图片支持
- [ ] 实现高级搜索功能
- [ ] 添加借阅提醒邮件
- [ ] 优化移动端体验

### 中期计划 (v1.5)
- [ ] 多图书馆支持
- [ ] 图书推荐系统
- [ ] 数据导入导出功能
- [ ] API 接口开放

### 长期愿景 (v2.0)
- [ ] 人工智能推荐
- [ ] 微信小程序支持
- [ ] 云端部署方案
- [ ] 企业级功能扩展

---

## � 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 👨‍💻 作者

**Developer** - *初始开发* - [YourName](https://github.com/yourusername)

---

## 🙏 致谢

- 感谢 Flask 社区提供的优秀框架
- 感谢 Bootstrap 团队的美观UI组件
- 感谢 Python 社区的强大生态系统
- 感谢所有贡献者和用户的支持

---

<div align="center">

### ⭐ 如果这个项目对您有帮助，请给我们一个 Star！

**[📖 详细文档](docs/)** • **[🐛 问题反馈](https://github.com/yourusername/LibraryManager/issues)** • **[💬 讨论交流](https://github.com/yourusername/LibraryManager/discussions)**

Made with ❤️ by LibraryManager Team

</div>