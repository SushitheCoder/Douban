# -*- coding: utf-8 -*-
import os
import time
import requests
from lxml import etree

import base64
import hashlib
from PIL import Image
import re


import logger
import verification

log = logger.LogModule()


def getCookies():
    # 获取豆瓣登录Cookie信息
    #cookie = requests.cookies.get_dict()
    cookies = {}
    with open('cookie.txt', "r", encoding='utf-8') as f_cookie:
#   with open('resources/cookies.txt', "r", encoding='utf-8') as f_cookie:
        biscuit = f_cookie.readlines()[0].split("; ")
        for line in biscuit:
            key, value = line.split("=", 1)
            cookies[key] = value
        return cookies

def flushCookies(session: requests.Session):
    cookies = session.cookies.get_dict()
    line = ""
    with open('cookies.txt', "w", encoding='utf-8') as f_cookie:
        for k, v in cookies.items():
            line  +=  k + '=' + v + '; '
        line = line[:len(line)-2]
        f_cookie.write(line)

def getCKFormCookies():
    # 从cookie中获取ck值（ck: post操作表单隐藏字段）
    cookies = getCookies()
    ck = cookies["ck"]
    if (ck is None):
        log.error("No ck found in cookies", cookies)
        raise Exception('No ck found in cookies')
    return ck

def get_value_from_html(html_text, xpath_exp):
    # 在指定的html文本中，提取指定xpath规则的单一元素/属性/值
    try:
        html = etree.HTML(html_text)
        value = html.xpath(xpath_exp)
        if len(value):
            return value[0]
        else:
            return ""
    except Exception as e:
        log.error("in func get_value_from_html();" + str(e.message))


if __name__ == "__main__":
    dict = getCookies()

    path = 'resources/captchas/'
    li = os.listdir(path)
    for entry in li:
        text = getTextFromPic(path+entry)
        print(text)
