# -*- coding: utf-8 -*-
import re
import pytz
import requests
from lxml import html
from datetime import datetime, timezone, timedelta

tz = pytz.timezone('Asia/Shanghai')

cctv_channel = ['cctv1', 'cctv2', 'cctv3', 'cctv4', 'cctv5', 'cctv5plus', 'cctv6','cctv7', 'cctv8', 'cctvjilu', 'cctv10', 'cctv11', 'cctv12', 'cctvchild','cctv15', 'cctv16', 'cctv17', 'cctv4k']
sat_channel = ['cetv1', 'cetv2', 'cetv3', 'cetv4', 'btv1', 'btvjishi', 'dongfang','hunan', 'shandong', 'zhejiang', 'jiangsu', 'guangdong', 'dongnan', 'anhui','gansu', 'liaoning', 'travel', 'neimenggu', 'ningxia', 'qinghai', 'xiamen','yunnan', 'chongqing', 'jiangxi', 'shan1xi', 'shan3xi', 'shenzhen', 'sichuan', 'tianjin','guangxi', 'guizhou', 'hebei', 'henan', 'heilongjiang', 'hubei', 'jilin','yanbian', 'xizang', 'xinjiang', 'bingtuan', 'btvchild', 'gaoerfu', 'sdetv']

def getChannelCNTV(fhandle, channelID):
    # change channelID list to str cids
    cids = ''
    for x in channelID:
        cids = cids + x + ','
    date = '%Y%m%d'
    epgdate = datetime.now(tz).strftime(date)
    session = requests.Session()
    api = f"http://api.cntv.cn/epg/epginfo?c={cids}&d={epgdate}"
    epgdata = session.get(api).json()

    for n in range(len(channelID)):
        # channelName = epgdata[channelID[n]]['channelName']
        fhandle.write(f'\t<channel id="{channelID[n]}">\n')
        fhandle.write(f'\t\t <display-name lang="cn">{epgdata[channelID[n]]["channelName"]}</display-name>\n')
        fhandle.write('\t</channel>\n')


def getChannelEPG(fhandle, channelID):
    date = '%Y%m%d'
    epgdate = [
        (datetime.now(tz) + timedelta(days=-3)).strftime(date),
        (datetime.now(tz) + timedelta(days=-2)).strftime(date),
        (datetime.now(tz) + timedelta(days=-1)).strftime(date),
        datetime.now(tz).strftime(date),
        (datetime.now(tz) + timedelta(days=1)).strftime(date),
        (datetime.now(tz) + timedelta(days=2)).strftime(date),
        (datetime.now(tz) + timedelta(days=3)).strftime(date),

    ];

    cids = ''
    for x in channelID:
        cids = cids + x + ','

    for k in epgdate:
        session = requests.Session()
        api = f"http://api.cntv.cn/epg/epginfo?c={cids}&d={k}"
        epgdata = session.get(api).json()
        for n in range(len(channelID)):
            name = epgdata[channelID[n]]['channelName']
            program = epgdata[channelID[n]]['program']
            for detail in program:
                # write programe
                st = datetime.fromtimestamp(detail['st']).strftime('%Y%m%d%H%M') + '00'
                et = datetime.fromtimestamp(detail['et']).strftime('%Y%m%d%H%M') + '00'

                fhandle.write(f'\t<programme start="{st}" stop="{et}" channel="{channelID[n]}">\n')
                fhandle.write(f'\t\t<title lang="zh">{detail["t"]}</title>\n')
                fhandle.write(f'\t\t<desc lang="zh">{name}</desc>\n')
                fhandle.write('\t</programme>\n')

def getsave():
    # 参数 w 表示覆盖，追加用 at (追加+文本)
    with open('epg.xml', 'w', encoding='utf-8') as fhandle:
        fhandle.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        fhandle.write('<tv generator-info-name="xiaoluoxxx" generator-info-url="https://github.com/xiaoluoxxx/iptv-one">\n')
        getChannelCNTV(fhandle, cctv_channel)
        getChannelCNTV(fhandle, sat_channel)
        getChannelEPG(fhandle, cctv_channel)
        getChannelEPG(fhandle, sat_channel)
        fhandle.write('</tv>')

if __name__ == '__main__':
    getsave()
    print('获取完成！')
