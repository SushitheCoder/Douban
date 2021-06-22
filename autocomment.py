# -*- coding: utf-8 -*-
import random
import time
import requests
from lxml import etree
from queue import SimpleQueue

import re
import urllib.parse
import base64
import hmac
from hashlib import sha1

import jqr
import verification
import logger
import crawler

DOUBAN_SITE = "https://www.douban.com/"
DOUBAN_GROUP = DOUBAN_SITE + "group/"
DOUBAN_GROUP_MY = DOUBAN_GROUP + "people/"
DOUBAN_TOPIC = DOUBAN_GROUP + "topic/"

log = logger.LogModule()

if __name__ == "__main__":
    group_id = "694789"
    group_url = DOUBAN_GROUP + group_id
    group = requests.get(group_url, cookies=jqr.getCookies())
    group_topics = etree.HTML(group.text).xpath("//table[@class='olt']/tr/td[@class='title']/a/@href")
    group_topics = group_topics[5:]
    for topic_url in group_topics:
        comment_topic_url = topicUrl + "/add_comment#last"
        comment_str = " "
        comment_dict = comment.writeComment(topicUrl, comment_str)
        comment.sendComment(comment_topic_url, comment_dict)
        random_sleep = random.randint(100, 500)
        time.sleep(random_sleep)


def prepareCaptcha(topicUrl, r=None) -> dict:
    pic_url, pic_id = verification.getCaptchaInfo(topicUrl)
    yzm = ""
    if len(pic_url):
        pic_path = verification.save_pic_to_disk(pic_url)
        log.debug(pic_url, pic_path)
        yzm = verification.getTextFromPic(pic_path)
    return yzm

def writeComment(topicUrl, rv_comment):
    # 组装回帖的参数
    topic_id = topicUrl[35:]
    #topic_id = topic_id[:-1]
    sig = hash_hmac(
        config.client_secret,
        config.sig_code_template.format(topic_id=topic_id, timestamp=str(int(time.time()))),
        sha1,
    )
    comment_format = {
        "ck": jqr.getCKFormCookies(),
        "rv_comment": rv_comment,
        "start": 0,
        "sig": urllib.parse.quote(sig),
        "captcha-solution": prepareCaptcha(topicUrl, r),
        "captcha-id": pic_id,
        "submit_btn": "评论"
    }
    return comment_format

def sendComment(topic_id, comment_dict):
    try:
        # 在一个帖子下发表回复
        topicUrl = group_url + '/' + topic_id
        r = requests.Session().post(topicUrl, cookies=jqr.getCookies(), data=comment_dict)
        with open("topic_dict.txt", "a+") as file:
            file_object.write("\n" + topic_id)
        log.info("in func comment_topic(), " + str(comment_dict) + ", status_code: " + str(r.status_code))
        return r
    except Exception as e:
        log.error("Failed to send comment: " + str(e))
        #proxy.update_proxy()
        return None

def generateResponse(topicUrl, ques: str, userID: str):
    map = {}
    # load responses
    with open('ttl.txt', "r", encoding='utf-8') as file:
        lines = file.readlines().strip()
        for l in lines:
            words = l.split(' ')
            response = []
            if words[0] in map:
                map[words[0]].append(words[1])
            response.append[words[1]]
            map[words[0]] = response
    for keys in map:
        topic-content
    #read post contect to find keywords to match key
    possibles = map[]
    if (rsp is not None):
        chosen = random.randint(0, len(possibles) - 1)
        return rsp[chosen]
    return False
