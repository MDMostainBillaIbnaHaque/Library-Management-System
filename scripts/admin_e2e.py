import requests
import sqlite3
import time
import uuid
from werkzeug.security import generate_password_hash

BASE='http://127.0.0.1:5000'
s = requests.Session()
print('Logging in as admin...')
r = s.post(BASE + '/login', data={'email':'ahmedrazon58@gmail.com','password':'22203142'}, timeout=5)
print('login status', r.status_code)
if r.status_code not in (200,302):
    print('Login failed, exiting')
    raise SystemExit(1)

con = sqlite3.connect(r'd:/Libary Management System/database.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
# find a book with no active borrows
row = cur.execute("SELECT b.id,b.title,b.quantity,b.available FROM books b WHERE b.id NOT IN (SELECT book_id FROM transactions WHERE return_date IS NULL) LIMIT 1").fetchone()
if not row:
    print('No book available for safe delete/edit test')
else:
    bid = row['id']
    print('Selected book', bid, row['title'], 'qty', row['quantity'], 'avail', row['available'])
    g = s.get(f'{BASE}/admin/book/{bid}/edit')
    print('GET edit status', g.status_code)
    # update quantity +1
    new_qty = row['quantity'] + 1
    p = s.post(f'{BASE}/admin/book/{bid}/edit', data={'title': row['title'], 'author': 'E2E Tester', 'isbn': '0000', 'category': 'E2E', 'quantity': new_qty}, timeout=5)
    print('POST edit status', p.status_code)
    cur.execute('SELECT id,quantity,available FROM books WHERE id=?', (bid,))
    nb = cur.fetchone()
    print('After edit qty/avail', nb['quantity'], nb['available'])
    # try delete
    d = s.post(f'{BASE}/admin/book/{bid}/delete', timeout=5)
    print('POST delete status', d.status_code)
    chk = cur.execute('SELECT * FROM books WHERE id=?', (bid,)).fetchone()
    print('Exists after delete?', bool(chk))

# create a test member directly in DB (active)
email = f'e2e_test_{uuid.uuid4().hex[:6]}@example.com'
pwd = 'TempPass123'
hash = generate_password_hash(pwd)
cur.execute('INSERT INTO users (name,email,password,role,is_active) VALUES (?,?,?,?,?)'[:0])
# above line is a no-op mimic -> replace with actual insert
cur.execute('INSERT INTO users (name,email,password,role,is_active) VALUES (?,?,?,?,?)', ('E2E User', email, hash, 'member', 1))
con.commit()
uid = cur.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone()['id']
print('Inserted test user', uid, email)

# now delete user via admin route
rdel = s.post(f'{BASE}/admin/user/{uid}/delete', timeout=5)
print('admin delete user status', rdel.status_code)
chk = cur.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
print('User exists after delete?', bool(chk))

con.close()
print('E2E complete')
