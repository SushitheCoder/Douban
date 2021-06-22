import requests
from lxml import etree
import time
import random
from queue import SimpleQueue, Empty

from actions import RespGen
from mySelectors import NewPostSelector

import logger
import jqr
import verification
import autocomment
import requestwrapper

log = logger.LogModule()
session = requests.Session


def getHeaders(fileName=None):
    name = 'headers.txt'
    if (fileName is not None):
        name = fileName
    name = 'resources/' + name
    headers = {}
    with open(name, "r", encoding='utf-8') as f_headers:
        hdrs = f_headers.readlines()
    for line in hdrs:
        key, value = line.split(": ")
        headers[key] = value.strip()
    return headers


def login(url, pwd, userName):
    loginData = {'ck': jqr.getCKFormCookies(), 'name': userName, 'password': pwd, 'remember': 'true'}
    loginHeaders = getHeaders('login_headers.txt')
    l = session.post(url, data=loginData, headers=loginHeaders)

    if l.status_code == requests.codes['ok'] or l.status_code == requests.codes['found']:
        print("Login Successfully")
        return True
    else:
        print("Failed to Login")
        log.error("Failed to Login", l.status_code)
        session.close()
        return False

def selectPost():
    # 找到首页最早发出的0回复的帖子，如果没有返回None
    try:
        r = session.get(topicUrl, proxies=proxy.proxy, timeout=5)
        if r.status_code != 200:
            log.error("Failed to retrieve group topics: " + str(r.status_code))
            #proxy.update_proxy()
            return None
        group_json = json.loads(r.text)
        for topic in reversed(group_json["topics"]):
            if topic["comments_count"] <= 1:
                topic_id = re.findall("\d+", topic["url"])[0]
                file = open("topic_dict.txt", 'w+')
                topic_dict = file.readlines().strip()
                    if topic_id not in topic_dict:
                        return topic_id
        return None
    except Exception as e:
        log.error("Failed to send request: " + str(e))
        #proxy.update_proxy()
        return None



def main():
    q = SimpleQueue()
    cred = verification.getCred()
    pwd = cred['pwd']
    username = cred['userName']
    login("https://accounts.douban.com/passport/login", pwd, username)
    loginReqUrl = ''

    refresh_count = 0
    reply_count = 0
    continuous_count = 0

    reqWrapper = requestwrapper.ReqWrapper()
    s = reqWrapper._session
    s.headers.update({
        'Host': 'www.douban.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    s.cookies.update(jqr.getCookies())

    while True:
        if q.qsize() == 0:
            log.debug("Empty queue, sleep")
            time.sleep(5)
        log.info("****Queue size: ", q.qsize(), "Sleep time: " + str(timeToSleep) + "****")
        try:
            while q.qsize() > 0:
                topicUrl = group_url + '/' + selectPost()
                refresh_count += 1
                if autocomment.generateResponse() == False:
                    continuous_count = 0
                    continue
                else:
                    autocomment.sendComment(topicUrl, autocomment.writeComment(topicUrl, autocomment.generateResponse()))
                    reply_count += 1
                    continuous_count += 1
                    if continuous_count > 4:
                        continuous_count = 0

                # 为了避免豆瓣反爬虫机制，连续回复的次数越多，sleep的时间越长
                random_sleep = random.randint(15, 25) + continuous_count * 3
                log.info("Sleep for " + str(random_sleep) + " seconds")
                time.sleep(random_sleep)

        except Empty:
            log.info("Emptied queue, one round finished")
        finally:
            jqr.flushCookies(s)


if __name__ == '__main__':
    main()
