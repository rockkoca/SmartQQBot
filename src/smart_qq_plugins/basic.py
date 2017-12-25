# -*- coding: utf-8 -*-
import random
import datetime

from smart_qq_bot.logger import logger
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_discuss_message,
)

from .database import Database

# =====唤出插件=====

# 机器人连续回复相同消息时可能会出现
# 服务器响应成功,但实际并没有发送成功的现象
# 所以尝试通过随机后缀来尽量避免这一问题
REPLY_SUFFIX = (
    '~',
    '!',
    '?',
    '||',
)


def msg_2_dict(msg):
    # remove = {'bot', 'font', 'meta', 'to_uin'}
    keep = {
        'content',
        'src_sender_card',
        'src_group_id',
        'src_sender_id',
        'src_sender_name',
        'time'
    }
    d = {}
    # d = {key: getattr(msg, key) for key in dir(msg) if key in keep}
    for key in dir(msg):
        try:
            d[key] = getattr(msg, key)
        except Exception as e:
            print(e)

    if d['src_sender_name'] == '水云间':
        d['src_sender_id'] = '375085690'

    d['time'] = datetime.datetime.fromtimestamp(d.get('time', datetime.datetime.now().timestamp()))
    print(d)
    return d


# @on_all_message(name='basic[callout]')
# def callout(msg, bot):
#     # if "智障机器人" in msg.content:
#     #     reply = bot.reply_msg(msg, return_function=True)
#     #     logger.info("RUNTIMELOG " + str(msg.from_uin) + " calling me out, trying to reply....")
#     #     reply_content = "干嘛（‘·д·）" + random.choice(REPLY_SUFFIX)
#     #     reply(reply_content)
#     print(msg)
#     print(dir(msg))
#     coll = Database.client['qq']['msgs']
#     print(coll.insert_one(msg_2_dict(msg)))
#     for k, v in msg_2_dict(msg).items():
#         print(k, v)


# =====复读插件=====
class Recorder(object):
    def __init__(self):
        self.msg_list = list()
        self.last_reply = ""


recorder = Recorder()


#
# @on_group_message(name='basic[repeat]')
# def repeat(msg, bot):
#     global recorder
#     reply = bot.reply_msg(msg, return_function=True)
#
#     if len(recorder.msg_list) > 0 and recorder.msg_list[-1].content == msg.content and recorder.last_reply != msg.content:
#         if str(msg.content).strip() not in ("", " ", "[图片]", "[表情]"):
#             logger.info("RUNTIMELOG " + str(msg.group_code) + " repeating, trying to reply " + str(msg.content))
#             reply(msg.content)
#             recorder.last_reply = msg.content
#     recorder.msg_list.append(msg)
#
#
# @on_group_message(name='basic[三个问题]')
# def nick_call(msg, bot):
#     if "我是谁" == msg.content:
#         bot.reply_msg(msg, "你是{}({})!".format(msg.src_sender_card or msg.src_sender_name, msg.src_sender_id))
#
#     elif "我在哪" == msg.content:
#         bot.reply_msg(msg, "你在{name}({id})!".format(name=msg.src_group_name, id=msg.src_group_id))
#
#     elif msg.content in ("我在干什么", "我在做什么"):
#         bot.reply_msg(msg, "你在调戏我!!")

@on_group_message(name='basic[存储美股聊天记录]')
def store_meigu_group_message(msg, bot):
    coll = Database.client['qq']['group_465723845']
    d = msg_2_dict(msg)
    print(d['src_group_id'], '465723845')
    if str(d['src_group_id']).strip() == '465723845' and d['content']:
        print(coll.insert_one(d))

    for k, v in d.items():
        print(k, v)

# @on_discuss_message(name='basic[讨论组三个问题]')
# def discuss_three_questions(msg, bot):
#     if "我是谁" == msg.content:
#         bot.reply_msg(msg, "你是{}!".format(msg.src_sender_name))
#
#     elif "我在哪" == msg.content:
#         bot.reply_msg(msg, "你在{name}!".format(name=msg.src_discuss_name))
#
#     elif msg.content in ("我在干什么", "我在做什么"):
#         bot.reply_msg(msg, "你在调戏我!!")
