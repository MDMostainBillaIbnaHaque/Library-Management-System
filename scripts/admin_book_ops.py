import requests
import sqlite3

BASE='http://127.0.0.1:5000'
with requests.Session() as s:
    r=s.post(BASE+'/login', data={'email':'ahmedrazon58@gmail.com','password':'22203142'})
    print('login', r.status_code)
    # pick first non-admin book
    con=sqlite3.connect(r'd:/Libary Management System/database.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    b=cur.execute('SELECT id,title,quantity,available FROM books ORDER BY id LIMIT 1').fetchone()
    if not b:
        print('no books in db')
    else:
        bid=b['id']
        print('book', bid, b['title'], 'qty', b['quantity'], 'avail', b['available'])
        # GET edit page
        g=s.get(f'{BASE}/admin/book/{bid}/edit')
        print('GET edit', g.status_code)
        # POST update: change quantity by +1
        new_qty = b['quantity'] + 1
        p=s.post(f'{BASE}/admin/book/{bid}/edit', data={'title': b['title'], 'author': 'Test Author', 'isbn': '0001', 'category': 'Test', 'quantity': new_qty})
        print('POST edit', p.status_code)
        # fetch refreshed book
        nb=cur.execute('SELECT id,title,quantity,available FROM books WHERE id=?', (bid,)).fetchone()
        print('after update qty', nb['quantity'], 'avail', nb['available'])
        # attempt delete (should succeed if no active borrows)
        d=s.post(f'{BASE}/admin/book/{bid}/delete')
        print('delete status', d.status_code)
        # verify deletion
        chk=cur.execute('SELECT * FROM books WHERE id=?', (bid,)).fetchone()
        print('exists after delete?', bool(chk))
    con.close()