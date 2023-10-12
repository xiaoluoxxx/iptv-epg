
import re

import requests

# url = input('请输入URL：')
url = 'https://7877c04i73.yicp.fun/api.php/timming/index.html?enforce=1&name=992ae5cbb1c5c2b16e7d2858d94a9384collect02'

headers = {
        "Cookie":     "PHPSESSID=glo3p0nfsmntoar9gj4a9q6kvn; mx_style=white; showBtn=true; tips=ok; closeclick=closeclick",
        "Referer":    "http: //127.0.0.7/admin.php/admin/type/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",

}

html_data = requests.get(url = url, headers = headers).text
da = re.findall('采集地址&nbsp;(.*?)<br>', html_data)
dd = re.findall(r'<br>(\d+.*?) <font color=\'.*?\'>(.*?)</font>', html_data)
w = ''
s = ''
for b, a in enumerate(dd):
    w = w + f'({b + 1})_{a[0]}\t<====>\t{a[1]}' + '\n'
with open('result.txt', 'w', encoding = 'utf-8') as result:
    result.write(w)
for i in da:
    s = s + i + '\n'
with open('result_2.txt', 'w', encoding = 'utf-8') as result:
    result.write(s)
print(s)
print(w)
