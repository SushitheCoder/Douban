# -*- coding: utf-8 -*-

import urllib
import json
import base64

import jqr
import logger

log = logger.LogModule()
session = requests.Session

def getCred(fileName='confidentials/pwd.txt'):
    data = {}
    with open(fileName, 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        for li in lines:
            k, v = li.strip().split('=')
            data[k.strip()] = v.strip()
    return data

def getAccessToken():
    host = ''
    cred = getCred('')
    api_key = cred['myid']
    secret_key = cred['mysecret']
    host = host + '&client_id=' + api_key + '&client_secret=' + secret_key

    json = requests.get(host).json()
    # if json.get('error') is None:
    return json['access_token']

def getTextFromPic(pic_path) -> str:
    # 给定图片地址 pic_path，识别图片当中的文字
    img = None
    request_url = ""
    accessToken = getAccessToken()
    request_url = request_url + "?access_token=" + accessToken
    # 二进制方式打开图片文件  # 参数image：图像base64编码
    with open(pic_path, 'rb') as f:
        img = base64.b64encode(f.read())
    params = {"image":img}
    params = urllib.parse.urlencode(params).encode(encoding="utf-8")
    header = {'Content-Type':'application/x-www-form-urlencoded'}
    r = requests.post(request_url, data=params, headers=header)

    # log.info(r.json())
    resp = r.json()
    content = resp.get('words_result')
    if content:
        text = resp['words_result'][0]['words'].lower()
        return re.sub(r"[^a-z]+", '', text)
        #text = resp['words_result'][0]['words'].strip()
        #return text.split(" ")[0]
    else:
        log.error("In getTextFromPic", resp)
        return ""


def getCaptchaInfo(topicUrl, r=None):
    # 获取验证码的图片URL和id
    if r is not None:
        return parseCaptcha(r)
    time.sleep(10)
    r = session.get(topicUrl, cookies=jqr.getCookies())
    #r = requests.get(postUrl, cookies=jqr.getCookies())
    if r.status_code == 200:
    # error handling
        pic_url, pic_id = parseCaptcha(r.text)
        log.info(str(pic_url))
        return pic_url, pic_id
    else:
        log.warning(str(url) + ", status_code: " + str(r.status_code))
        return "", ""

def parseCaptcha(r):
    # 通过html提取验证码图片URL和id
    html = etree.HTML(r.text)
    pic_url = html.xpath("//img[@class='captcha_image']/@src")
    pic_id = html.xpath("//input[@name='captcha-id']/@value")

    if len(pic_url) and len(pic_id):
        return pic_url[0], pic_id[0]
    else:
        return "", ""


def save_pic_to_disk(pic_url):
    # 将链接中的图片保存到本地，并返回文件名
    try:
        if not os.path.exists(filepath.image_path):
            os.mkdir(filepath.image_path)
        res = session.get(pic_url)
        #res = requests.get(pic_url)
        if res.status_code == 200:
            # 求取图片的md5值，作为文件名，以防存储重复的图片
            md5_obj = hashlib.md5()
            md5_obj.update(res.content)
            md5_code = md5_obj.hexdigest()
            file_name = myConfig.imgPath + str(md5_code) + ".jpg"
            # 如果图片不存在，则保存
            if not os.path.exists(file_name):
                with open(file_name, "wb") as f:
                    f.write(res.content)
            return file_name
        else:
            log.warning("in func save_pic_to_disk(), fail to save pic. pic_url: " + pic_url + ", res.status_code: " + str(res.status_code))
            raise Exception
    except Exception as e:
        log.error(e.message)
