import requests
r = requests.get('http://ifconfig.me')
print (r.text)