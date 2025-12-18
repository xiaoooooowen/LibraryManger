#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibraryManager - 智慧图书馆管理系统
使用Python内置sqlite3数据库，避免版本兼容性问题
"""

import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from functools import wraps

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'library_management_system_secret_key_2024'

# 数据库配置
DATABASE = 'library.db'

def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """初始化数据库"""
    db = get_db()
    
    # 创建用户表
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建图书表
    db.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            description TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建借阅记录表
    db.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP NOT NULL,
            return_date TIMESTAMP,
            is_returned BOOLEAN DEFAULT 0,
            fine_amount REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    db.commit()
    
    # 创建默认管理员账户
    admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        db.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@library.com', admin_password, 1))
        db.commit()
        print("默认管理员账户已创建: admin / admin123")
    except Exception as e:
        print(f"创建管理员账户时出错: {e}")
    
    # 添加示例图书数据
    sample_books = [
        ('978-7-111-12345-6', 'Python编程：从入门到实践', 'Eric Matthes', '编程', '适合初学者的Python编程指南', 5, 5),
        ('978-7-111-23456-3', 'Flask Web开发', 'Miguel Grinberg', 'Web开发', 'Flask框架实战教程', 3, 3),
        ('978-7-111-34567-0', '深入理解计算机系统', 'Randal E. Bryant', '计算机科学', '计算机系统经典教材', 2, 2),
        ('978-7-111-45678-7', '算法导论', 'Thomas H. Cormen', '算法', '算法设计分析的权威教材', 1, 1),
        ('978-7-111-56789-4', '设计模式：可复用面向对象软件的基础', 'Erich Gamma', '软件工程', '经典设计模式书籍', 2, 2),
    ]
    
    for book_data in sample_books:
        try:
            db.execute('''
                INSERT OR IGNORE INTO books (isbn, title, author, category, description, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', book_data)
            db.commit()
        except Exception as e:
            print(f"添加图书时出错: {e}")

def hash_password(password):
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """登录装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """管理员装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        
        if not user or not user['is_admin']:
            flash('您没有权限访问此页面', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def current_user():
    """获取当前用户"""
    if 'user_id' in session:
        db = get_db()
        return db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return None

@app.before_request
def before_request():
    """请求前设置当前用户"""
    g.user = current_user()

# 路由定义
@app.route('/')
def index():
    """首页"""
    db = get_db()
    
    # 统计信息
    total_books = db.execute('SELECT COUNT(*) as count FROM books').fetchone()['count']
    total_users = db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    active_loans = db.execute('SELECT COUNT(*) as count FROM loans WHERE is_returned = 0').fetchone()['count']
    
    # 热门图书
    popular_books = db.execute('''
        SELECT b.*, COUNT(l.id) as loan_count 
        FROM books b 
        LEFT JOIN loans l ON b.id = l.book_id 
        GROUP BY b.id 
        ORDER BY loan_count DESC, b.created_at DESC 
        LIMIT 6
    ''').fetchall()
    
    return render_template('index_simple.html', 
                         total_books=total_books,
                         total_users=total_users,
                         active_loans=active_loans,
                         popular_books=popular_books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('密码不匹配', 'danger')
            return render_template('register_simple.html')
        
        if len(password) < 6:
            flash('密码长度至少6位', 'danger')
            return render_template('register_simple.html')
        
        db = get_db()
        
        # 检查用户名是否已存在
        existing_user = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('用户名已存在', 'danger')
            return render_template('register_simple.html')
        
        # 创建新用户
        password_hash = hash_password(password)
        db.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        db.commit()
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register_simple.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('''
            SELECT * FROM users 
            WHERE username = ? AND is_active = 1
        ''', (username,)).fetchone()
        
        if user and user['password_hash'] == hash_password(password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            flash('登录成功', 'success')
            next_page = request.args.get('next') or url_for('index')
            return redirect(next_page)
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login_simple.html')

@app.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    flash('已成功登出', 'info')
    return redirect(url_for('index'))

@app.route('/books')
def books():
    """图书浏览"""
    db = get_db()
    
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    # 构建查询
    query = 'SELECT * FROM books WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY created_at DESC'
    
    books_list = db.execute(query, params).fetchall()
    
    # 获取所有分类
    categories = db.execute('SELECT DISTINCT category FROM books WHERE category IS NOT NULL').fetchall()
    
    return render_template('books_simple.html', 
                         books=books_list, 
                         categories=categories,
                         search=search,
                         selected_category=category)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """图书详情"""
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if not book:
        flash('图书不存在', 'danger')
        return redirect(url_for('books'))
    
    # 获取借阅历史
    loan_history = db.execute('''
        SELECT l.*, u.username 
        FROM loans l 
        JOIN users u ON l.user_id = u.id 
        WHERE l.book_id = ? 
        ORDER BY l.loan_date DESC 
        LIMIT 10
    ''', (book_id,)).fetchall()
    
    return render_template('book_detail_simple.html', book=book, loan_history=loan_history)

@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    """借阅图书"""
    db = get_db()
    
    # 检查图书是否存在且可借
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if not book:
        flash('图书不存在', 'danger')
        return redirect(url_for('books'))
    
    if book['available_copies'] <= 0:
        flash('该图书暂无库存', 'warning')
        return redirect(url_for('book_detail', book_id=book_id))
    
    # 检查用户是否已借阅该图书且未归还
    existing_loan = db.execute('''
        SELECT * FROM loans 
        WHERE user_id = ? AND book_id = ? AND is_returned = 0
    ''', (session['user_id'], book_id)).fetchone()
    
    if existing_loan:
        flash('您已经借阅了这本书', 'warning')
        return redirect(url_for('book_detail', book_id=book_id))
    
    # 检查用户当前借阅数量
    current_loans = db.execute('''
        SELECT COUNT(*) as count FROM loans 
        WHERE user_id = ? AND is_returned = 0
    ''', (session['user_id'],)).fetchone()['count']
    
    if current_loans >= 5:
        flash('最多只能同时借阅5本书', 'warning')
        return redirect(url_for('book_detail', book_id=book_id))
    
    # 创建借阅记录
    due_date = datetime.now() + timedelta(days=14)
    db.execute('''
        INSERT INTO loans (user_id, book_id, due_date)
        VALUES (?, ?, ?)
    ''', (session['user_id'], book_id, due_date))
    
    # 更新图书库存
    db.execute('''
        UPDATE books 
        SET available_copies = available_copies - 1 
        WHERE id = ?
    ''', (book_id,))
    
    db.commit()
    flash(f'成功借阅《{book["title"]}》，请在14天内归还', 'success')
    return redirect(url_for('book_detail', book_id=book_id))

@app.route('/my_loans')
@login_required
def my_loans():
    """我的借阅"""
    db = get_db()
    
    loans = db.execute('''
        SELECT l.*, b.title, b.author, b.isbn
        FROM loans l 
        JOIN books b ON l.book_id = b.id 
        WHERE l.user_id = ?
        ORDER BY l.loan_date DESC
    ''', (session['user_id'],)).fetchall()
    
    # 计算逾期状态
    current_date = datetime.now()
    loans_with_status = []
    
    for loan in loans:
        loan_dict = dict(loan)
        if loan_dict['due_date']:
            due_date = datetime.strptime(loan_dict['due_date'], '%Y-%m-%d %H:%M:%S')
            loan_dict['is_overdue'] = not loan_dict['is_returned'] and current_date > due_date
        else:
            loan_dict['is_overdue'] = False
        loans_with_status.append(loan_dict)
    
    return render_template('my_loans_simple.html', loans=loans_with_status, current_date=current_date)

@app.route('/return/<int:loan_id>', methods=['POST'])
@login_required
def return_book(loan_id):
    """归还图书"""
    db = get_db()
    
    # 检查借阅记录是否存在且属于当前用户
    loan = db.execute('''
        SELECT l.*, b.id as book_id
        FROM loans l 
        JOIN books b ON l.book_id = b.id 
        WHERE l.id = ? AND l.user_id = ?
    ''', (loan_id, session['user_id'])).fetchone()
    
    if not loan:
        flash('借阅记录不存在', 'danger')
        return redirect(url_for('my_loans'))
    
    if loan['is_returned']:
        flash('该图书已归还', 'warning')
        return redirect(url_for('my_loans'))
    
    # 计算逾期费用
    current_date = datetime.now()
    due_date = datetime.strptime(loan['due_date'], '%Y-%m-%d %H:%M:%S')
    fine_amount = 0
    
    if current_date > due_date:
        days_overdue = (current_date - due_date).days
        fine_amount = days_overdue * 0.5
    
    # 更新借阅记录
    db.execute('''
        UPDATE loans 
        SET is_returned = 1, return_date = ?, fine_amount = ?
        WHERE id = ?
    ''', (current_date, fine_amount, loan_id))
    
    # 更新图书库存
    db.execute('''
        UPDATE books 
        SET available_copies = available_copies + 1 
        WHERE id = ?
    ''', (loan['book_id'],))
    
    db.commit()
    
    if fine_amount > 0:
        flash(f'图书已归还，逾期费用：{fine_amount:.2f}元', 'info')
    else:
        flash('图书已归还', 'success')
    
    return redirect(url_for('my_loans'))

@app.route('/admin')
@admin_required
def admin():
    """管理员面板"""
    db = get_db()
    
    # 统计数据
    total_books = db.execute('SELECT COUNT(*) as count FROM books').fetchone()['count']
    total_users = db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    active_loans = db.execute('SELECT COUNT(*) as count FROM loans WHERE is_returned = 0').fetchone()['count']
    overdue_loans = db.execute('''
        SELECT COUNT(*) as count FROM loans 
        WHERE is_returned = 0 AND due_date < ?
    ''', (datetime.now(),)).fetchone()['count']
    
    # 所有数据
    books = db.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
    users = db.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    loans = db.execute('''
        SELECT l.*, u.username, b.title 
        FROM loans l 
        JOIN users u ON l.user_id = u.id 
        JOIN books b ON l.book_id = b.id 
        ORDER BY l.loan_date DESC
    ''').fetchall()
    
    return render_template('admin_simple.html',
                         total_books=total_books,
                         total_users=total_users,
                         active_loans=active_loans,
                         overdue_loans=overdue_loans,
                         books=books,
                         users=users,
                         loans=loans)

if __name__ == '__main__':
    # 初始化数据库
    with app.app_context():
        init_db()
    
    print("=" * 50)
    print("🎉 图书馆管理系统启动成功！")
    print("🌐 访问地址: http://127.0.0.1:5000")
    print("👤 默认管理员: admin / admin123")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)