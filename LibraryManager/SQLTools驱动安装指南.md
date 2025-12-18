# SQLTools SQLite驱动程序安装指南

## 🔧 问题解决

您看到的 "Couldn't find any installed drivers" 错误是因为SQLTools需要安装SQLite驱动程序。

## 📥 驱动安装步骤

### 方法一：通过SQLTools命令安装（推荐）

1. **打开VS Code命令面板**
   - 按 `Ctrl+Shift+P`

2. **安装SQLite驱动**
   - 输入 "SQLTools: Install Driver"
   - 选择 "SQLite" 选项
   - 等待安装完成

### 方法二：自动提示安装

1. **在SQLTools连接界面**
   - 点击 "Search VS Code Marketplace"
   - 找到SQLTools SQLite Driver
   - 点击安装

### 方法三：手动安装驱动

1. **按 `Ctrl+Shift+P`**
2. **输入 "SQLTools: Add New Connection"**
3. **选择 "SQLite"**
4. **系统会自动提示安装驱动**

## 🗄️ 连接配置步骤

### 第一步：确保驱动已安装
安装完成后，您应该能看到：
```
✅ SQLite Driver installed successfully
```

### 第二步：添加数据库连接

#### 详细步骤：
1. **按 `Ctrl+Shift+P`**
2. **输入 "SQLTools: Add New Connection"**
3. **选择 "SQLite"**
4. **输入/选择数据库文件路径**：
   ```
   c:\Users\27970\Documents\trae_projects\demo\LibraryManager\library.db
   ```
5. **输入连接名称**：
   ```
   图书馆管理系统
   ```
6. **点击 "Connect"**

### 第三步：验证连接

连接成功后，您应该看到：
```
✅ Connected to 图书馆管理系统
```

## 🎯 快速验证查询

连接成功后，尝试运行以下查询来验证：

```sql
-- 查看所有表
.tables

-- 查看用户统计
SELECT COUNT(*) as 用户总数 FROM users;

-- 查看图书统计
SELECT COUNT(*) as 图书总数 FROM books;

-- 查看图书分类
SELECT category, COUNT(*) as 数量 FROM books GROUP BY category;
```

## ❗ 常见问题解决

### 问题1：找不到数据库文件
**错误信息**：`Database file not found`

**解决方案**：
- 检查文件路径是否正确
- 确保路径中没有中文字符或特殊符号
- 使用绝对路径：`C:\Users\27970\Documents\trae_projects\demo\LibraryManager\library.db`

### 问题2：权限不足
**错误信息**：`Permission denied`

**解决方案**：
- 右键点击数据库文件
- 选择"属性" → "安全"
- 确保VS Code有读取权限

### 问题3：驱动安装失败
**错误信息**：`Driver installation failed`

**解决方案**：
1. 重启VS Code
2. 重新安装SQLTools插件
3. 检查网络连接（驱动从npm下载）

### 问题4：连接超时
**错误信息**：`Connection timeout`

**解决方案**：
1. 确保数据库文件没有被其他程序锁定
2. 重启VS Code
3. 检查文件路径是否正确

## 🔍 验证安装成功

### 检查驱动状态
1. 打开VS Code输出面板（`Ctrl+Shift+U`）
2. 选择"SQLTools"输出源
3. 应该看到：
   ```
   SQLite driver loaded successfully
   ```

### 测试连接
在SQLTools查询窗口中运行：
```sql
SELECT 'Hello SQLTools!' as 消息;
```

如果返回结果，说明安装成功！

## 📞 技术支持

如果仍然遇到问题：

1. **检查VS Code版本**
   - 确保使用最新版本

2. **重置SQLTools**
   - `Ctrl+Shift+P` → "Developer: Reload Window"

3. **清理缓存**
   - 删除VS Code缓存文件夹

4. **重新安装**
   - 卸载SQLTools插件
   - 重启VS Code
   - 重新安装

---

**预期安装时间**：2-3分钟
**网络要求**：需要互联网连接下载驱动
**兼容性**：Windows 10/11 + VS Code 最新版本