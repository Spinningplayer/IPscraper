from bs4 import BeautifulSoup
import urllib3, base64
import os, sys

url = "http://proxy-list.org/english/index.php?p="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}

page = 0
ips = []
ports = []

if os.geteuid() != 0:
    print "[!]  Run this program as root"
    sys.exit()

if len(sys.argv) != 2:
    print "[!]  Usage: %s <config>" %str(sys.argv[0])
    sys.exit()

http = urllib3.PoolManager()
req = http.request('GET', url, None, headers)

while len(ips) < 6:

    try:
        print "[*] Opening URL " + url + str(page)
        http = urllib3.PoolManager()
        req = http.request('GET', url + str(page), None, headers)
        data = BeautifulSoup(req.data, "html.parser")
    except:
        print "[!] Error opening URL!"
        sys.exit()

    print "[*] Processing body"
    table = data.find('div', {'class': 'table-wrap'})
    for ul in table.findAll('ul'):
        speed = ul.find('li', {'class': 'speed'}).getText().replace("kbit", "")
        if speed == "-":
            continue

        if float(speed) > 1024:
            address = base64.decodestring(ul.find('li', {'class': 'proxy'}).getText()[7:-2])
            ip, port = address.split(':')
            ips.append(ip)
            ports.append(port)
        else:
            continue

    page += 1

print "[*] Writing addresses to file"
f = open(sys.argv[1], "a")
for i in range(0, len(ips)):
    f.write("http\t%s\t%s\n" %(ips[i], ports[i]))

f.close()

print "[*] Done!"