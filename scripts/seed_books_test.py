import requests
import sqlite3

BASE='http://127.0.0.1:5000'
try:
    s = requests.Session()
    r = s.post(BASE + '/login', data={'email':'ahmedrazon58@gmail.com','password':'22203142'}, timeout=5)
    print('login status', r.status_code)
    r2 = s.post(BASE + '/admin/seed_books', timeout=10)
    print('seed_books status', r2.status_code)
    # show counts
    con = sqlite3.connect(r'd:/Libary Management System/database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cnt = cur.execute('SELECT COUNT(*) as c FROM books').fetchone()[0]
    print('books_count=', cnt)
    print('sample categories:')
    rows = cur.execute('SELECT category, COUNT(*) as c FROM books GROUP BY category').fetchall()
    for r in rows:
        print('-', r['category'], r['c'])
    print('\nfirst 10 books:')
    for r in cur.execute('SELECT id,title,author,quantity,available,category FROM books ORDER BY id LIMIT 10').fetchall():
        print(r['id'], '-', r['title'], '-', r['author'], '-', r['quantity'], '-', r['category'])
    con.close()
except Exception as e:
    print('ERROR', e)
