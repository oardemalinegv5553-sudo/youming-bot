from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
import random
import re


def has_any(msg: str, keywords: set) -> bool:
    for kw in keywords:
        if kw in msg:
            return True
    return False


KEYWORD_REPLIES = {
    "晚安": ["晚安~好梦！", "早点休息！", "晚安呀"],
    "睡了": ["晚安~好梦！", "早点休息！"],
    "晚安啦": ["晚安~好梦！", "早点休息！"],
    "早上好": ["早上好！新的一天加油~", "早！"],
    "早安": ["早安！", "早上好呀~"],
    "早啊": ["早！今天天气不错！"],
    "吃了吗": ["吃了！你呢？", "还没呢，你呢？", "正在吃瓜"],
    "吃饭": ["吃啥好呢？", "干饭人干饭魂！"],
    "午饭": ["中午吃啥？", "干饭时间到！"],
    "晚饭": ["晚上吃点啥好呢？", "干饭！"],
    "笑死": ["什么事这么好笑？", "hhhh"],
    "哭了": ["摸摸头，怎么了？", "抱抱，都会好起来的"],
    "emo": ["别emo了，来首开心点的歌！", "都会过去的~"],
    "难过": ["摸摸头", "没事的，明天会更好"],
    "牛逼": ["确实！", "太强了"],
    "厉害了": ["一般一般~", "基操勿6"],
    "谢谢": ["不客气！", "客气啦~"],
    "打卡": ["滴！打卡成功", "收到！"],
    "签到": ["滴！签到成功", "来了来了"],
    "有人吗": ["在在在！", "有人！"],
    "没人吗": ["在在在！", "有人！"],
}

kws = on_message()

@kws.handle()
async def handle_kws(bot: Bot, event: Event):
    msg = event.get_plaintext().strip()
    for kw, replies in KEYWORD_REPLIES.items():
        if kw in msg:
            await kws.finish(random.choice(replies))


# ---- 问天气/时间 ----
wt = on_message()

@wt.handle()
async def handle_wt(bot: Bot, event: Event):
    from datetime import datetime
    msg = event.get_plaintext().strip()
    if has_any(msg, {"天气"}):
        await wt.finish("我暂时还不会看天气呢~ 问问天气App吧！")
    elif has_any(msg, {"几点了", "几点"}):
        now = datetime.now()
        await wt.finish(f"现在是 {now.hour}:{now.minute:02d}")
    elif has_any(msg, {"日期", "今天几号"}):
        now = datetime.now()
        await wt.finish(f"今天是 {now.year}年{now.month}月{now.day}日")
