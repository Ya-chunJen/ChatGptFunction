# -*- coding: utf-8 -*-
import oss2
import os
import sys
import configparser
import json

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), "config.ini"),encoding="UTF-8")
configsection = config['aliyun']

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth(configsection["key1"], configsection["key2"])

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'pubdz')

# 必须以二进制的方式打开文件。
# 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。

def aliyunossup(function_args):
    file_path = function_args["file_path"]
    file_dir = function_args["file_dir"]

    with open(file_path, 'rb') as fileobj:
        # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
        fileobj.seek(0, os.SEEK_SET)
        # Tell方法用于返回当前位置。
        current = fileobj.tell()
        file_name = file_path.split("/", )[-1]  #根据文件路径获取文件名和后缀，仅适用于Mac
        # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
        bucket.put_object(file_dir+'/'+file_name,fileobj)
        fileurl = 'https://pubdz.paperol.cn/'+file_dir+'/'+file_name
    callback_json =  {"request_gpt_again":False,"details":f"已将该文件上传到{file_dir}目录，文件地址：{fileurl}"}
    return json.dumps(callback_json)

if __name__ == '__main__':
    file_path = input("请输入文件路径：")
    file_dir = input("请输入要上传的目录：")
    function_args = {"file_path":file_path,"file_dir":file_dir}
    print(aliyunossup(function_args))