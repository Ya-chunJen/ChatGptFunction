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
        print("GPT:" + response_content)
        return response_content

def loop():
    while True:
        try:
            prompt =  input("You：")
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
    username_index = input("选择数字进入对应会话，输入0创建新会话：")
    try:
        username_index = int(username_index) 
    except ValueError as e:
        print("ValueError:", e) 

    if username_index<0 or username_index > len(usernamelist):
        # 判断是不是小于现有的长度
        print("输入错误") 
    elif username_index == 0:
        # 创建新会话
        username = input("请输入一个会话名称：")
        system_content = input("请输入这个会话对应的system定义。")
        if system_content == "":
            system_content = "你是一个有用的智能助手。"
    else:
        username = usernamelist[username_index]



if __name__ == '__main__':
    whichusername()
    # system_content =  "你是一个有用的智能助手。"
    # username = input("请输入一个用户名：")
    loop()