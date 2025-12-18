# SQLTools 连接图书馆系统SQLite数据库配置指南

## 📋 数据库信息

- **数据库文件位置**：`c:\Users\27970\Documents\trae_projects\demo\library_management_system_simple\library.db`
- **数据库类型**：SQLite 3
- **文件大小**：24.5 KB
- **创建时间**：2025/12/18 22:28

## 🔧 SQLTools 配置步骤

### 步骤1：安装SQLTools插件
1. 打开VS Code
2. 按 `Ctrl+Shift+X` 打开扩展市场
3. 搜索 "SQLTools"
4. 安装 **SQLTools** 插件（作者：mtxr）

### 步骤2：安装SQLite驱动
1. 安装完成后，SQLTools会提示安装SQLite驱动
2. 或者按 `Ctrl+Shift+P`，输入 "SQLTools: Add New Connection"
3. 选择 "SQLite" 作为数据库类型
4. 插件会自动下载SQLite驱动

### 步骤3：添加数据库连接

#### 方法一：通过命令面板
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "SQLTools: Add New Connection"
3. 选择 "SQLite"
4. 选择数据库文件：`c:\Users\27970\Documents\trae_projects\demo\library_management_system_simple\library.db`
5. 输入连接名称：`图书馆管理系统`

#### 方法二：通过SQLTools侧边栏
1. 点击左侧SQLTools图标（数据库图标）
2. 点击 "Add New Connection" 按钮
3. 选择 "SQLite"
4. 浏览选择数据库文件
5. 命名连接

### 步骤4：连接配置详细参数

在SQLTools连接配置中，使用以下信息：

```
连接类型：SQLite
数据库文件：c:\Users\27970\Documents\trae_projects\demo\library_management_system_simple\library.db
连接名称：图书馆管理系统
描述：图书馆管理系统数据存储
```

## 📊 数据库结构概览

连接成功后，您可以查看以下数据表：

### 1. **users** - 用户表
```sql
-- 查看用户表结构
SELECT sql FROM sqlite_master WHERE type='table' AND name='users';

-- 查看所有用户
SELECT * FROM users;

-- 查看管理员用户
SELECT * FROM users WHERE is_admin = 1;
```

### 2. **books** - 图书表
```sql
-- 查看图书表结构
SELECT sql FROM sqlite_master WHERE type='table' AND name='books';

-- 查看所有图书
SELECT * FROM books;

-- 按分类查看图书
SELECT * FROM books ORDER BY category;
```

### 3. **loans** - 借阅记录表
```sql
-- 查看借阅表结构
SELECT sql FROM sqlite_master WHERE type='table' AND name='loans';

-- 查看当前借阅
SELECT * FROM loans WHERE is_returned = 0;

-- 查看借阅历史
SELECT * FROM loans WHERE is_returned = 1;
```

## 🎯 常用查询语句

### 用户管理查询
```sql
-- 查看用户统计
SELECT 
    COUNT(*) as 总用户数,
    SUM(CASE WHEN is_admin = 1 THEN 1 ELSE 0 END) as 管理员数量,
    SUM(CASE WHEN is_admin = 0 THEN 1 ELSE 0 END) as 普通用户数量
FROM users;

-- 查看活跃用户（最近注册）
SELECT username, email, created_at 
FROM users 
ORDER BY created_at DESC 
LIMIT 10;
```

### 图书管理查询
```sql
-- 图书库存统计
SELECT 
    category as 分类,
    COUNT(*) as 图书数量,
    SUM(total_copies) as 总册数,
    SUM(available_copies) as 可借册数
FROM books 
GROUP BY category;

-- 热门图书（按借阅次数）
SELECT b.title, b.author, COUNT(l.id) as 借阅次数
FROM books b
LEFT JOIN loans l ON b.id = l.book_id
GROUP BY b.id
ORDER BY 借阅次数 DESC
LIMIT 10;
```

### 借阅管理查询
```sql
-- 当前借阅状态
SELECT 
    u.username,
    b.title,
    l.loan_date,
    l.due_date,
    CASE 
        WHEN date(l.due_date) < date('now') THEN '已逾期'
        WHEN date(l.due_date) = date('now') THEN '今日到期'
        ELSE '正常'
    END as 状态
FROM loans l
JOIN users u ON l.user_id = u.id
JOIN books b ON l.book_id = b.id
WHERE l.is_returned = 0
ORDER BY l.due_date;

-- 借阅统计
SELECT 
    COUNT(*) as 总借阅次数,
    COUNT(CASE WHEN is_returned = 0 THEN 1 END) as 当前借阅,
    COUNT(CASE WHEN is_returned = 1 THEN 1 END) as 已归还,
    AVG(CASE WHEN is_returned = 1 THEN julianday(return_date) - julianday(loan_date) END) as 平均借阅天数
FROM loans;
```

## 🔍 数据探索查询

### 查看数据库基本信息
```sql
-- 查看所有表
SELECT name FROM sqlite_master WHERE type='table';

-- 查看表结构
.schema

-- 查看数据库版本
SELECT sqlite_version();
```

### 数据完整性检查
```sql
-- 检查用户表完整性
SELECT COUNT(*) as 用户总数 FROM users;

-- 检查图书表完整性
SELECT COUNT(*) as 图书总数 FROM books;

-- 检查借阅记录完整性
SELECT COUNT(*) as 借阅记录总数 FROM loans;

-- 检查孤儿记录（用户已删除但仍有借阅记录）
SELECT COUNT(*) as 孤儿借阅记录 
FROM loans l 
LEFT JOIN users u ON l.user_id = u.id 
WHERE u.id IS NULL;
```

## 📱 SQLTools 快捷操作

### 常用快捷键
- `Ctrl+Shift+P` + "SQLTools: Run Query" - 运行查询
- `Ctrl+Shift+E` - 执行选中的SQL
- `F5` - 刷新连接
- `Ctrl+Shift+R` - 重新连接

### 实用功能
1. **自动补全**：输入表名或列名时会有智能提示
2. **查询历史**：SQLTools会保存您的查询历史
3. **结果导出**：右键点击查询结果可导出为CSV
4. **书签保存**：保存常用查询为书签

## ⚠️ 注意事项

### 数据安全
1. **备份数据库**：在进行任何修改前，先备份 `library.db` 文件
2. **只读查询**：建议先使用SELECT查询熟悉数据结构
3. **权限管理**：普通用户只能查看，管理员可以进行修改

### 性能优化
1. **索引优化**：大数据量时考虑为常用查询字段添加索引
2. **查询优化**：避免SELECT *，只查询需要的字段
3. **分页查询**：大数据集使用LIMIT和OFFSET

## 🆘 故障排除

### 连接问题
- 确保数据库文件路径正确
- 检查文件权限（确保VS Code有读取权限）
- 重启VS Code后重新连接

### 查询错误
- 检查SQL语法
- 确保表名和列名正确
- 查看SQLTools输出面板的错误信息

### 性能问题
- 关闭其他不必要的数据库连接
- 重启SQLTools服务
- 检查系统资源使用情况

## 📞 技术支持

如遇到问题：
1. 查看SQLTools官方文档
2. 检查VS Code输出面板
3. 重启VS Code和SQLTools服务
4. 联系系统管理员

---

**配置完成时间**：2025年12月18日
**适用系统**：Windows 10/11
**VS Code版本**：最新版本
**SQLTools版本**：最新版本