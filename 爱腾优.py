import re

import requests

pa = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
# 全部采集：全网资源（爱腾优）
url = 'http://e61cf922-861f-7823-2c1e-a30a9e898996.openfrp.cc:62233/api.php/timming/index.html?enforce=1&name=c35e48b9c28be5e56228ce9a81d0a7b5collect02week'
html_data = requests.get(url = url, params = pa).text
data = re.findall(r"<br>(\d+.*?)<font color='.*?'>(.*?)</font>", html_data)
for a, b in enumerate(data):
    print(a, b)
