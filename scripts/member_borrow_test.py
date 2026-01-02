import sqlite3
import requests
from werkzeug.security import generate_password_hash
import uuid

DB=r'd:/Libary Management System/database.db'
BASE='http://127.0.0.1:5000'
con=sqlite3.connect(DB)
con.row_factory=sqlite3.Row
cur=con.cursor()
# create test member
email=f'member_test_{uuid.uuid4().hex[:6]}@example.com'
name='Member Test'
password='TestPass123'
cur.execute('INSERT INTO users (name,email,password,role,is_active) VALUES (?,?,?,?,?)'[:0])
# actual insert
cur.execute('INSERT INTO users (name,email,password,role,is_active) VALUES (?,?,?,?,?)', (name, email, generate_password_hash(password), 'member', 1))
con.commit()
uid=cur.execute('SELECT id FROM users WHERE email=?',(email,)).fetchone()['id']
print('Created member', uid, email)
# pick a book with available>0
b=cur.execute('SELECT id,title,available FROM books WHERE available>0 LIMIT 1').fetchone()
if not b:
    print('No available book')
    con.close()
    raise SystemExit(1)
print('Selected book', b['id'], b['title'], 'avail', b['available'])
con.close()
# login and borrow
s=requests.Session()
print('Logging in...')
r=s.post(BASE+'/login', data={'email':email,'password':password})
print('login status', r.status_code)
r2=s.get(f'{BASE}/borrow/{b["id"]}')
print('borrow GET', r2.status_code)
# since borrow is a GET route, it performs action and redirects
print('final URL', r2.url)
# show resulting book available count
con=sqlite3.connect(DB)
con.row_factory=sqlite3.Row
cur=con.cursor()
nb=cur.execute('SELECT available FROM books WHERE id=?',(b['id'],)).fetchone()
print('new available', nb['available'])
con.close()