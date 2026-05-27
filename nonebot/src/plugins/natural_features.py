from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
import random
import re


def has_any_keyword(msg: str, keywords: set) -> bool:
    """检查消息是否包含任意关键词"""
    for kw in keywords:
        if kw in msg:
            return True
    return False


# ==================== 今天吃什么 ====================
FOODS = [
    "麻辣烫", "黄焖鸡", "沙县小吃", "兰州拉面", "螺蛳粉", "炸鸡汉堡",
    "酸菜鱼", "火锅", "烤肉", "日料", "韩式拌饭", "煲仔饭",
    "水饺", "馄饨", "煎饼果子", "肉夹馍", "凉皮", "过桥米线",
    "披萨", "寿司", "麻辣香锅", "烤鱼", "牛蛙", "小龙虾",
    "肠粉", "叉烧饭", "担担面", "重庆小面", "冒菜", "串串香",
    "随便吃点", "泡面", "不吃了减肥", "叫外卖吧", "看看冰箱里有啥"
]

EAT_KW = {"今天吃什么", "吃啥", "吃什么呢", "中午吃啥", "晚上吃啥", "推荐个吃的"}

eat = on_message()

@eat.handle()
async def handle_eat(bot: Bot, event: Event):
    if has_any_keyword(event.get_plaintext(), EAT_KW):
        await eat.finish(f"{random.choice(FOODS)}！")


# ==================== 猜拳 ====================
RPS = {"石头": "剪刀", "剪刀": "布", "布": "石头"}
RPS_EMOJI = {"石头": "✊", "剪刀": "✌️", "布": "🖐️"}

rps = on_message()

@rps.handle()
async def handle_rps(bot: Bot, event: Event):
    msg = event.get_plaintext()
    if not has_any_keyword(msg, {"猜拳", "石头剪刀布"}):
        return
    bot_choice = random.choice(list(RPS.keys()))
    user_choice = None
    for c in ["石头", "剪刀", "布"]:
        if c in msg:
            user_choice = c
            break
    if not user_choice:
        await rps.finish(f"我出了{RPS_EMOJI[bot_choice]} {bot_choice}！你也出呀")
        return
    if user_choice == bot_choice:
        await rps.finish(f"你{RPS_EMOJI[user_choice]} vs 我{RPS_EMOJI[bot_choice]}  平局！再来？")
    elif RPS[user_choice] == bot_choice:
        await rps.finish(f"你{RPS_EMOJI[user_choice]} vs 我{RPS_EMOJI[bot_choice]}  你赢了！")
    else:
        await rps.finish(f"你{RPS_EMOJI[user_choice]} vs 我{RPS_EMOJI[bot_choice]}  我赢了！")


# ==================== 答案之书 ====================
ANSWERS = [
    "是的。", "别想了。", "放手去做。", "再等等。",
    "现在不是时候。", "问问你的内心。", "顺其自然。", "毫无疑问。",
    "时机未到。", "换个角度看看。", "保持期待。", "不会后悔的。",
    "你需要更多信息。", "先冷静一下。", "答案就在你心里。",
    "值得一试。", "保守一点更好。", "大胆一点。", "这个我说不准。",
    "别问了，去做吧。", "可能会后悔。", "看起来不错。", "没那么简单。",
]

answer = on_message()

@answer.handle()
async def handle_answer(bot: Bot, event: Event):
    if "答案之书" in event.get_plaintext():
        await answer.finish(f"答案之书说：{random.choice(ANSWERS)}")


# ==================== 彩虹屁 ====================
COMPLIMENTS = [
    "你今天怎么这么好看？是不是偷偷进化了？",
    "你这种级别的存在感，群里少了你就不完整。",
    "上帝把智慧洒满人间的时候，你带了桶是吧？",
    "你的代码要是发朋友圈，马云都给你点赞。",
    "你简直是这个群里唯一的光。",
    "我要是会写诗，你已经被我写成史诗了。",
]
COMPLIMENT_KW = {"夸我", "彩虹屁", "夸夸我", "表扬我", "赞美我"}

compliment = on_message()

@compliment.handle()
async def handle_compliment(bot: Bot, event: Event):
    if has_any_keyword(event.get_plaintext(), COMPLIMENT_KW):
        await compliment.finish(random.choice(COMPLIMENTS))


# ==================== 骂我 ====================
ROASTS = [
    "你的存在本身就是一种行为艺术。",
    "我见你有勇气来找骂，就已经很佩服了。",
    "你这个人吧，怎么说呢，活着就是最大的努力。",
    "我这人嘴笨，不会骂人，你再等等，等我学会了再来。",
]
ROAST_KW = {"骂我", "怼我", "损我"}

roast = on_message()

@roast.handle()
async def handle_roast(bot: Bot, event: Event):
    if has_any_keyword(event.get_plaintext(), ROAST_KW):
        await roast.finish(random.choice(ROASTS))


# ==================== 计算器 ====================
calc = on_message()

@calc.handle()
async def handle_calc(bot: Bot, event: Event):
    msg = event.get_plaintext().strip()
    if not has_any_keyword(msg, {"计算", "算一下"}):
        return
    for p in ["计算", "算一下", "计算：", "算一下："]:
        msg = msg.replace(p, "", 1).strip()
    safe = re.sub(r'[^0-9+\-*/().%\s]', '', msg)
    if not safe or len(safe) > 50:
        return
    try:
        result = eval(safe, {"__builtins__": {}}, {})
        await calc.finish(f"{safe} = {result}")
    except Exception:
        return


# ==================== 讲故事 ====================
STORIES = [
    "从前有一个程序员，他从来不写注释。后来他离职了，没人敢接他的代码。完。",
    "小明面试，面试官：你有什么优点？小明：我很诚实。面试官：你有什么缺点？小明：我不太会说谎。面试官：那你说我长得帅不帅？小明想了想：我不太会说谎。",
    "从前有个人叫小王，他特别能卷。卷到最后，他成了卷王，然后他发现，卷王的卷不读juǎn，读juàn。他原来是春卷。",
]
STORY_KW = {"讲个故事", "来个故事", "讲故事"}

story = on_message()

@story.handle()
async def handle_story(bot: Bot, event: Event):
    if has_any_keyword(event.get_plaintext(), STORY_KW):
        await story.finish(random.choice(STORIES))


# ==================== 抛硬币/做决定 ====================
coin = on_message()

@coin.handle()
async def handle_coin(bot: Bot, event: Event):
    msg = event.get_plaintext()
    if not has_any_keyword(msg, {"抛硬币", "硬币", "二选一"}):
        return
    match = re.search(r'(.+?)还是(.+?)[？?]?$', msg)
    if match:
        a, b = match.group(1).strip(), match.group(2).strip()
        await coin.finish(f"我选「{random.choice([a, b])}」")
    else:
        await coin.finish(f"硬币结果：{random.choice(['正面', '反面'])}")


# ==================== 土味情话 ====================
LOVE_WORDS = [
    "你知道我最大的缺点是什么吗？是缺点你。",
    "你上辈子一定是碳酸饮料吧？一见到你我就开心得冒泡。",
    "你有打火机吗？没有的话你怎么点燃了我的心的。",
    "你属什么的？我属你的。",
    "你是哪里人？你是我的心上人。",
]
LOVE_KW = {"土味情话", "说句情话"}

love = on_message()

@love.handle()
async def handle_love(bot: Bot, event: Event):
    if has_any_keyword(event.get_plaintext(), LOVE_KW):
        await love.finish(random.choice(LOVE_WORDS))
