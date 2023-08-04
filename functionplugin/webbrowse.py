import os
import json
from bs4 import BeautifulSoup
import requests
from html2markdown import convert

def webbrowse(function_args):
    url = function_args["url"]
    if "https://mp.weixin.qq.com/s" in url:
        # 公众号内容读取
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find("div", {"class": "rich_media_wrp"})
        text = content.text
        print(len(text))
        if len(text) > 1000:
            text = text[:1000]
        # markdown = convert(content)
        print(len(text))
        # print(text)
        callback_json = {"request_gpt_again":True,"details":text} 
        return json.dumps(callback_json)

    else:
        os.system(f'open {url}')    
        callback_json = {"request_gpt_again":False,"details":"WebBrowse插件已经打开该网站，请检查。"} 
        return json.dumps(callback_json)


if __name__ == '__main__':
    url = input("请输入一个网址：")
    function_args = {"url":url}
    print(webbrowse(function_args))