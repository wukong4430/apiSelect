#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name    : newcoder.py
# Author       : Kicc <kiccshen@whu.edu.cn>
# Create Date  : 2019-09-20 19:28:43
# Last Modified: 2019-09-20 19:28:43

"""
从牛客网上爬取一道题目的多种语言实现(Java & Python3)

"""

import requests
from pyquery import PyQuery
from selenium import webdriver
from time import sleep
import pickle
from removeComment import deal_whole_code


login_url = 'https://www.nowcoder.com/login'


class Newcoder:
    def __init__(self, root_path):
        self.root = root_path
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    def set_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.nowcoder.com',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def getRootHtml(self):
        html = requests.get(self.root, headers=self.headers)
        return html

    def getEachQuestion(self, html):
        doc = PyQuery(html.text)
        table= doc('.module-box table tr').items()

        questions = []
        for tr in table:
            a = tr.find('a')
            href = a.attr('href')
            if href[0]!='/':
                continue
            else:
                questions.append('https://nowcoder.com'+href)
        
        return questions
        print(questions)


    def getAnswerPage(self, ques):
        """
        ques: 每个题目的url
        """
        html = requests.get(ques, headers=self.headers)
        print(html)
        doc = PyQuery(html.text)

        ul = doc('.code-list-box li').items()

        cnt = -1
        for li in ul:
            cnt+=1
            if cnt==2:
                a = li.find('a')
                href = 'https://nowcoder.com'+a.attr('href')
                # questionPage = requests.get(href, headers=self.headers)
                return href
            else:
                continue

        return 0
            
    def soup(self, ques, lang='java'):
        """
        分语言进行
        """
        try:
            if lang=='java':
                ques = ques + '&lang=4'
                codeUrl = self.soupJava(ques)
            elif lang=='python':
                ques = ques + '&lang=11'
                codeUrl = self.soupJava(ques)
            else:
                return '请选择合适的语言'
        except Exception as e:
            return 0

        return codeUrl

        

    def soupJava(self, ques):
        """
        得到题目名称&Java代码
        ques: 每个题目的答案url
        """
        javaPage = requests.get(ques, headers=self.headers)
        doc = PyQuery(javaPage.text)

        table = doc('.module-body tr').items()
        href = None
        # print(table)
        for idx, tr in enumerate(table):
            # print('idx=',idx)
            if idx==0:
                continue
            for index, td in enumerate(tr('td').items()):
                # print('index=',index)
                if index!=6:
                    continue
                else:

                    a = td.find('a')
                    # print(a)
                    href = 'https://nowcoder.com' + a.attr('href') # 这道题的第一个java解释
                    print(href)
                    break
            break

        return href
        doc2 = PyQuery(requests.get(href, headers=self.headers).text)
        # print(doc2)
        code = doc2('.code')
        print(code)

    def soupPython(self, ques):
        """
        得到题目名称和Python代码
        """
        pass


def getLinks(url):
    driver = webdriver.Chrome()
    driver.get(url)
    cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
    try:
        for cookie in cookies:
            print(cookie)
            cookie_dict = {
                'domain': 'www.nowcoder.com',  # 必须有，不然就是假登录
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": "",
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False}
            driver.add_cookie(cookie_dict)
        print('#### 载入cookie ####')
    except Exception as e:
        print(e)
    driver.refresh()
    driver.get(url)
    
def get_cookie():
    driver = webdriver.Chrome()
    driver.get(login_url)
    # self.driver.get(damai_url)
    print("###请点击登录###")

    sleep(20)
    print("###登陆成功###")
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    print("###Cookie保存成功###")

def getAllCodePageUrl(base_path, lang='java'):

    newcoder = Newcoder(base_path)
    html = newcoder.getRootHtml()
    questions = newcoder.getEachQuestion(html=html) # questions 是所有的题目

    allCodeUrls = []
    cnt = 0
    for ques in questions:
        cnt+=1
        # if cnt>2:
            # break
        q_html = newcoder.getAnswerPage(ques)
        # print(q_html)
        codeUrl = newcoder.soup(q_html, lang)
        if codeUrl==None:
            # 这道题可能没有Python解释,此时也改成Java
            codeUrl = newcoder.soup(q_html, 'java')
            # continue
        elif codeUrl==0:
            continue
        allCodeUrls.append(codeUrl)
        # break


    return allCodeUrls

def soupCode(url, lang):
    s = requests.Session()
    c = requests.cookies.RequestsCookieJar()

    cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
    for cookie in cookies:
        c.set(cookie['name'], cookie['value'])
    s.cookies.update(c)
    r = s.get(url)
    doc = PyQuery(r.text)
    title = doc('.crumbs-path span').items()
    timu = '>>>>>>>>>>>>>>>' + ''.join(t.text() for t in title)
    print(doc('title'))
    code = doc('.result-subject-item pre').items()
    json_code = dict()
    with open(lang + '.result', 'a+') as ja:

        for c in code:
            java = c.html()
            # ja.write(timu+'\n')
            # ja.write(java+'\n\r')

            json_code['question'] = timu
            java = deal_whole_code(java, lang)
            json_code[lang] = java

            if lang=='java':
                list_java.append(json_code)
            else:
                list_python.append(json_code)
            break # 第一个是这个人的答案，后面的都是评论
    # print(code)
    return



def func(lang='java'):
    base_path = 'https://www.nowcoder.com/ta/2017test?query=&asc=true&order=&page='
    for i in range(1, 5):
        path = base_path + str(i)

        codeUrl = getAllCodePageUrl(path, lang) # List[url] # 获得的都是类似与上面行的url
        print('codeUrl =', codeUrl)
        for url in codeUrl:
            print('url=',url)
            if url is None:
                continue
            soupCode(url, lang)
        # break


def main():
    url = 'https://www.nowcoder.com/profile/1183597/codeBookDetail?submissionId=23950707'
    
    langs = ['java', 'python']
    for lang in langs:
        func(lang)


import json

if __name__ == '__main__':
    # get_cookie()
    result = [] # List[dict]
    ques_java_python = dict()
    list_java = []
    list_python = []
    # json.dump(result, fp)

    main()


    # print(list_java)
    # print(list_python)

    for j, p in zip(list_java, list_python):
        if j['question']==p['question']:
            tmp = {}
            tmp['question']=j['question']
            tmp['java'] = j['java']
            tmp['python'] = p['python']
            if tmp['java']==tmp['python']:
                continue
            result.append(tmp)
    with open('2018.file', 'a+', encoding='utf-8') as fp:
        json.dump(result, fp, indent=4)
