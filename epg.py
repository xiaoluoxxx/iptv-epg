# -*- coding: utf-8 -*-
"""
@Create Time ： 2023/5/11/011 20:14
@Auth ： xiaoluoxxx
@File ：epg.py
@IDE ：PyCharm
"""
import pprint
import re
import pytz
import requests
from lxml import html
from datetime import datetime, timezone, timedelta

# import url

tz = pytz.timezone('Asia/Shanghai')
date = '%Y%m%d'
epgdate = datetime.now(tz).strftime(date)
epgtime = [
    (datetime.now(tz) + timedelta(days=-1)).strftime(date),
    datetime.now(tz).strftime(date),
    (datetime.now(tz) + timedelta(days=1)).strftime(date),

];

cctv_channel = ['cctv1','cctv2','cctv3','cctv4','cctv5','cctv5plus','cctv6','cctv7','cctv8','cctvjilu','cctv10','cctv11','cctv12',
                'cctvchild','cctv15','cctv16','cctv17','cctv4k','cetv1','cetv2','cetv3','cetv4','btv1','btvjishi','dongfang','hunan',
                'shandong','zhejiang','jiangsu','guangdong','dongnan','anhui','gansu','liaoning','travel','neimenggu','ningxia','qinghai',
                'xiamen','yunnan','chongqing','jiangxi','shan1xi','shan3xi','shenzhen','sichuan','tianjin','guangxi','guizhou','hebei','henan',
                'heilongjiang','hubei','jilin','yanbian','xizang','xinjiang','bingtuan','btvchild','gaoerfu','sdetv'
               ]


def get_epg(fhandle, cctv_channel):
    cids = ''
    for x in cctv_channel:
        cids = cids + x + ','

    url = f'https://api.cntv.cn/epg/getEpgInfoByChannelNew?c={cids}&serviceId=tvcctv&d={epgdate}'
    epgdata = requests.get(url).json()
    for i in cctv_channel:
        print(i)
        data = epgdata['data'][i]
        try:
            # lists = data['list']
            channelName = data['channelName']
            fhandle.write(f'\t<channel id="{i}">\n')
            fhandle.write(f'\t\t<display-name lang="cn">{channelName}</display-name>\n')
            fhandle.write('\t</channel>\n')
            for xxx in epgtime:
                url = f'https://api.cntv.cn/epg/getEpgInfoByChannelNew?c={cids}&serviceId=tvcctv&d={xxx}'
                epgdatas = requests.get(url).json()
                data_a=epgdatas['data']
                lists = data_a[i]['list']
                for detail in lists:
                    st = datetime.fromtimestamp(detail['startTime']).strftime('%Y%m%d%H%M') + '00'
                    et = datetime.fromtimestamp(detail['endTime']).strftime('%Y%m%d%H%M') + '00'
                    fhandle.write(f'\t<programme  channel="{i}" start="{st} +0800" stop="{et} +0800">\n')
                    fhandle.write(f'\t\t<title lang="zh">{detail["title"]}</title>\n')
                    fhandle.write(f'\t\t<desc lang="zh"></desc>\n')
                    fhandle.write('\t</programme>\n')
        except:
            pass


def get_save():
    with open('get_epg.xml', 'w', encoding='utf-8') as fhandle:
        fhandle.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
        fhandle.write('<tv info-name="xiaoluoxxx " info-url="https://github.com/xiaoluoxxx/iptv-one">\n')
        get_epg(fhandle, cctv_channel)
        fhandle.write('</tv>')


if __name__ == '__main__':
    get_save()
    print('完成')

'''
<?xml version="1.0" encoding="UTF-8"?>
<tv info-name="xiaoluoxxx " info-url="https://github.com/xiaoluoxxx/iptv-one">
    <channel id="cctv1">
        <display-name lang="cn">CCTV-1 综合</display-name>
    </channel>
    <programme channel="BBC地平线系列展播" start="20230511000000 +0800" stop="20230511011400 +0800">
		<title lang="zh">闺蜜的战争</title>
	</programme>
</tv>
    
'''
