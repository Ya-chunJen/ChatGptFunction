import sys
import os
import json
import os
import copy
import azureopenaifunctionplugin

class ChatGptMult:
    def __init__(self):
        pass

    def chatmult(self,username,prompt,system_content="You are a helpful assistant"):
        # 用户ID文件路径
        username_fpath = f"{username}.json"
        username_fpath = os.path.join(os.getcwd(),"log",username_fpath)
        # 判断用户ID文件是不是存在，存在就读取，不存在就建立
        if os.path.exists(username_fpath):
            with open(username_fpath) as f:
                message = json.load(f) 
        else:
            message = []
            system_dict = {"role":"system","content": system_content}
            message.append(system_dict)

        # 构造本次问答的问题
        prompt_dict = {"role":"user","content": prompt}
        
        # 将本次的提问和历史记录整合
        message.append(prompt_dict)

        # 如果聊天记录很长，只选取system和最近两轮的会话
        messages_thistime = copy.deepcopy(message)
        if len(messages_thistime)>=5:
            messages_thistime = [messages_thistime[0]] + messages_thistime[-4:]
            # print(messages_thistime)

        # 调用单轮会话的模块获取结果
        response_dit = azureopenaifunctionplugin.chatGPT_with_plugin(messages_thistime) #使用Azure的接口
        # response_dit = azureopenaifunctionplugin.chatGPT(messages_thistime) #使用Azure的接口
        # print(response_dit)
        
        # 将本次的回答和历史记录整合
        message.append(response_dit)

        with open(username_fpath, "w",encoding='utf-8') as file:
            json.dump(message, file)

        # 单独获取结果并打印，并作为函数返回结果
        response_content = response_dit["content"]
        print("ChatGPT:" + response_content)
        return response_content

def loop(username,system_content="You are a helpful assistant"):
    # 从文件中读取已有的函数插件列表
    funnctionpluginlist_file_path = os.path.join(os.getcwd(),"functionpluginlist.json")
    with open(funnctionpluginlist_file_path, 'r' ,encoding="UTF-8") as f:
        functions = json.load(f)  
        function_name_list = [function['name'] for function in functions] # 读取所有的函数插件的名称，形成一个列表。
        function_description_list = [function['description'] for function in functions]  #读取所有函数的使用功能描述，形成一个列表。
        function_keyword_list = [function['keyword'] for function in functions]

    function_available = "当前可用插件有：\n"    
    for i in range(len(functions)):
        function_available = function_available +"\n"+ f"{str(i+1)}、{function_name_list[i]}:{function_description_list[i]}"

    while True:
        try:
            prompt =  input(f"{username}(回车选用插件)：")
            if prompt != "":
                chatgptmult = ChatGptMult()
                chatgptmult.chatmult(username,prompt,system_content)
            else:
                print(function_available)
                while True:
                    try:
                        function_index = int(input("请输入插件序号："))
                        if function_index < 0 or function_index > len(functions)+1:
                            print("输入不在范围内，请重新输入。")
                        else:
                            break
                    except ValueError:
                        print("输入不合法，请重新输入。")
                prompt =  input(f"{username}({function_name_list[function_index-1]})：")
                prompt = function_keyword_list[function_index-1] + prompt
                # print(prompt)
                chatgptmult = ChatGptMult()
                chatgptmult.chatmult(username,prompt,system_content)
        except KeyboardInterrupt:
            break

def whichusername():
    usernamelist = []
    usernamelist_str = ""
    i = 1
    for filename in os.listdir(os.path.join(os.getcwd(),"log")):
        filename = filename.replace(".json","")
        usernamelist.append(filename)
        usernamelist_str = usernamelist_str + str(i) + "、" + filename + ";"
        i = i + 1
    print(usernamelist_str)
    
    while True:
        try:
            username_index = int(input("选择会话序号(输入0创建新会话)："))
            if username_index == 0:
                username = input("请输入新会话名称：")
                system_content = input("请输入会话的system内容：")
                if system_content == "":
                    system_content = "你是一个有用的智能助手。"
                loop(username,system_content)
                break
            elif username_index < 0 or username_index > len(usernamelist):
                print("输入不在范围内，请重新输入。")
            else:
                username = usernamelist[username_index-1]
                loop(username)
                break    # 如果输入数字且在范围内，退出循环
        except ValueError:
            print("输入不合法，请重新输入。")          

if __name__ == '__main__':
    whichusername()
    loop()