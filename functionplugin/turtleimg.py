import antigravity
import turtle
import json

def turtleimg(function_args):
    direction = function_args["direction"]
    distance = function_args["distance"]
    eval(f"turtle.{direction}({distance})")
    callback_json =  {"request_gpt_again":False,"details":f"已完成绘制。"}
    return json.dumps(callback_json)