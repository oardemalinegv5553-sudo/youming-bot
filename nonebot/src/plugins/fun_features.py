from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, MessageSegment
import random
import httpx
import json
from datetime import datetime

# ==================== AI 绘画 ====================
draw_cmd = on_command("draw", aliases={"画图", "画画", "生成图片"})

@draw_cmd.handle()
async def handle_draw(bot: Bot, event: Event):
    prompt = event.get_plaintext().strip()
    for prefix in ["/draw", "/画图", "/画画", "/生成图片"]:
        prompt = prompt.replace(prefix, "", 1).strip()

    if not prompt:
        await draw_cmd.finish("用法: /draw <描述>\n比如: /draw 一只戴墨镜的猫")

    await draw_cmd.send(f"正在画「{prompt}」...")

    try:
        # 使用免费AI绘画API
        url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&nologo=true"
        await draw_cmd.finish(MessageSegment.image(url))
    except Exception as e:
        await draw_cmd.finish(f"画图失败了: {e}")


# ==================== 微博热搜 ====================
hot_cmd = on_command("热搜", aliases={"微博热搜", "hot"})

@hot_cmd.handle()
async def handle_hot(bot: Bot, event: Event):
    try:
        r = httpx.get("https://tenapi.cn/v2/weibohot", timeout=10.0)
        data = r.json()
        if data.get("code") == 200:
            items = data.get("data", [])[:10]
            lines = ["微博热搜 Top10:"]
            for i, item in enumerate(items, 1):
                lines.append(f"{i}. {item['name']} (热度:{item.get('hot', '')})")
            await hot_cmd.finish("\n".join(lines))
        else:
            await hot_cmd.finish("热搜获取失败")
    except Exception as e:
        await hot_cmd.finish(f"获取失败: {e}")


# ==================== 今日运势 ====================
fortune_cmd = on_command("运势", aliases={"运气", "fortune", "抽签", "占卜"})

FORTUNES = [
    ("大吉", "今天运气爆棚！做什么都顺，适合表白、面试、买彩票", "鸿运当头"),
    ("吉", "运势不错，该做的事今天抓紧做", "顺风顺水"),
    ("中吉", "略有小吉，保持平常心", "小有收获"),
    ("小吉", "平淡是真，适合宅家", "知足常乐"),
    ("末吉", "不宜出头，低调行事", "静观其变"),
    ("凶", "今天少做决定，多喝水多睡觉", "韬光养晦"),
    ("大凶", "建议直接回家躺着，明天再说", "以退为进"),
]

@fortune_cmd.handle()
async def handle_fortune(bot: Bot, event: Event):
    user_id = event.user_id
    today = datetime.now().strftime("%Y%m%d")
    random.seed(int(str(user_id)) + int(today))

    level, desc, advice = random.choice(FORTUNES)
    lucky_num = random.randint(1, 99)
    lucky_color = random.choice(["红色", "蓝色", "绿色", "黄色", "黑色", "白色", "紫色", "橙色"])
    lucky_dir = random.choice(["东", "南", "西", "北", "东南", "西北"])

    result = (
        f"今日运势: {level}\n"
        f"解读: {desc}\n"
        f"幸运数字: {lucky_num}\n"
        f"幸运颜色: {lucky_color}\n"
        f"幸运方位: {lucky_dir}\n"
        f"宜: {advice}"
    )
    await fortune_cmd.finish(result)


# ==================== 今日新闻60s ====================
news_cmd = on_command("新闻", aliases={"早报", "日报", "news"})

@news_cmd.handle()
async def handle_news(bot: Bot, event: Event):
    try:
        r = httpx.get("https://tenapi.cn/v2/60s", timeout=10.0)
        data = r.json()
        if data.get("code") == 200:
            news_text = data.get("data", {}).get("news", "")
            if news_text:
                lines = news_text.strip().split("\n")[:15]
                await news_cmd.finish("今日60秒新闻:\n" + "\n".join(lines))
            else:
                await news_cmd.finish("暂时没有新闻数据")
        else:
            await news_cmd.finish("新闻获取失败")
    except Exception as e:
        await news_cmd.finish(f"获取失败: {e}")


# ==================== 随机一言 ====================
yiyan_cmd = on_command("一言", aliases={"yiyan", "名言", "毒鸡汤"})

@yiyan_cmd.handle()
async def handle_yiyan(bot: Bot, event: Event):
    try:
        r = httpx.get("https://tenapi.cn/v2/yiyan", timeout=5.0)
        data = r.json()
        if data.get("code") == 200:
            text = data.get("data", {}).get("hitokoto", "")
            author = data.get("data", {}).get("from", "")
            result = text
            if author:
                result += f"\n—— {author}"
            await yiyan_cmd.finish(result)
    except Exception:
        # 备用本地库
        local_quotes = [
            "生活不止眼前的苟且，还有读不懂的诗和到不了的远方。",
            "世上无难事，只要肯放弃。",
            "有时候你不努力一下，都不知道什么叫绝望。",
            "愿你出走半生，归来仍是少年。",
            "今天不想跑，所以才去跑。",
            "不要因为走得太远，忘了我们为什么出发。",
        ]
        await yiyan_cmd.finish(random.choice(local_quotes))


# ==================== 成语接龙 ====================
idiom_games = {}  # group_id -> {"last_word": "龙", "used": set()}

idiom_cmd = on_command("成语接龙", aliases={"接龙"})

@idiom_cmd.handle()
async def handle_idiom(bot: Bot, event: Event):
    if not isinstance(event, GroupMessageEvent):
        await idiom_cmd.finish("只能在群里玩成语接龙哦")
        return

    gid = str(event.group_id)
    text = event.get_plaintext().strip()
    word = text.replace("/成语接龙", "").replace("/接龙", "").strip()

    if not word:
        # 开始新游戏
        start = random.choice(["一马当先", "龙马精神", "心想事成", "万事如意"])
        idiom_games[gid] = {"last": start[-1], "used": {start}}
        await idiom_cmd.finish(f"成语接龙开始！\n{start}\n下一个请接「{start[-1]}」开头的成语")
        return

    game = idiom_games.get(gid)
    if not game:
        await idiom_cmd.finish("还没有开始的接龙，发 /接龙 开始吧")
        return

    if word[0] != game["last"]:
        await idiom_cmd.finish(f"要以「{game['last']}」开头哦，你接的是「{word[0]}」开头")

    if word in game["used"]:
        await idiom_cmd.finish("这个已经用过了，换个吧")

    if len(word) < 2:
        await idiom_cmd.finish("这不是成语吧...")

    game["used"].add(word)
    game["last"] = word[-1]
    await idiom_cmd.finish(f"接上了！{word}\n下一个请接「{word[-1]}」开头的成语")


# ==================== 骰子加强版 ====================
dice_cmd = on_command("dice", aliases={"骰子", "rd"})

@dice_cmd.handle()
async def handle_dice(bot: Bot, event: Event):
    text = event.get_plaintext().strip()
    for prefix in ["/dice", "/骰子", "/rd"]:
        text = text.replace(prefix, "", 1).strip()

    # 支持 /dice 2d6+3 格式
    import re
    match = re.match(r'(\d+)?d(\d+)([+-]\d+)?', text)
    if match:
        count = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        bonus = int(match.group(3)) if match.group(3) else 0
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls) + bonus
        detail = "+".join(str(r) for r in rolls)
        if bonus:
            detail += f"{bonus:+d}"
        await dice_cmd.finish(f"掷骰 {text}: [{detail}] = {total}")
    else:
        result = random.randint(1, 100)
        await dice_cmd.finish(f"D100: {result}")
