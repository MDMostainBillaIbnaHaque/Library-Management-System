import requests
import sqlite3
import uuid
from werkzeug.security import generate_password_hash

BASE='http://127.0.0.1:5000'
print('Checking /health...')
try:
    r=requests.get(BASE + '/health', timeout=3)
    print('/health', r.status_code, r.text.strip())
except Exception as e:
    print('/health ERROR', e)

print('\nChecking /books...')
try:
    r=requests.get(BASE + '/books', timeout=5)
    print('/books', r.status_code, 'len', len(r.text))
    print('Borrow buttons present?', '/borrow/' in r.text)
except Exception as e:
    print('/books ERROR', e)

print('\nChecking admin dashboard...')
s = requests.Session()
r = s.post(BASE + '/login', data={'email':'ahmedrazon58@gmail.com','password':'22203142'}, timeout=5)
print('/login', r.status_code)
try:
    r2 = s.get(BASE + '/dashboard', timeout=5)
    print('/dashboard', r2.status_code)
    print('Seed sample books present?', 'Seed sample books' in r2.text)
    print('Recent books present?', 'Manage books' in r2.text)
except Exception as e:
    print('/dashboard ERROR', e)

print('\nTest member borrow flow: create temp user, borrow a book, check availability')
try:
    db='d:/Libary Management System/database.db'
    con=sqlite3.connect(db)
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    # create temp user
    email=f'smoke_{uuid.uuid4().hex[:6]}@example.com'
    cur.execute('INSERT INTO users (name,email,password,role,is_active) VALUES (?,?,?,?,?)'[:0])
    cur.execute('INSERT INTO users (name,email,password,role,is_active) VALUES (?,?,?,?,?)', ('Smoke Test', email, generate_password_hash('Test1234'), 'member', 1))
    con.commit()
    uid=cur.execute('SELECT id FROM users WHERE email=?',(email,)).fetchone()['id']
    # pick a book with available > 0
    book = cur.execute('SELECT id, title, available FROM books WHERE available>0 LIMIT 1').fetchone()
    if not book:
        print('No available book to borrow')
    else:
        bid = book['id']
        avail_before = book['available']
        s2 = requests.Session()
        lr = s2.post(BASE + '/login', data={'email': email, 'password': 'Test1234'}, timeout=5)
        print('member login', lr.status_code)
        br = s2.get(f'{BASE}/borrow/{bid}', allow_redirects=True, timeout=5)
        print('borrow request status', br.status_code, 'final_url', br.url)
        # check updated availability
        nb = cur.execute('SELECT available FROM books WHERE id=?', (bid,)).fetchone()['available']
        print('availability before -> after', avail_before, '->', nb)
    # cleanup test user
    cur.execute('DELETE FROM users WHERE id=?', (uid,))
    con.commit()
    con.close()
except Exception as e:
    print('Borrow flow ERROR', e)

print('\nSmoke tests complete')
