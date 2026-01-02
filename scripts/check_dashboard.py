import requests
s=requests.Session()
r=s.post('http://127.0.0.1:5000/login', data={'email':'ahmedrazon58@gmail.com','password':'22203142'})
print('login', r.status_code)
r2=s.get('http://127.0.0.1:5000/dashboard')
print('/dashboard', r2.status_code)
print('Manage books present?', 'Manage books' in r2.text)
print('Seed button present?', 'Seed sample books' in r2.text)
