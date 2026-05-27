from nonebot import on_command, on_message, logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent
import random


def has_any(msg: str, keywords: set) -> bool:
    for kw in keywords:
        if kw in msg:
            return True
    return False


log_msg = on_message()

@log_msg.handle()
async def handle_log(bot: Bot, event: Event):
    text = event.get_plaintext().strip()
    if not text or text.startswith("/"):
        return
    logger.info(f"[MSG] {event.sender.card or event.sender.nickname or event.user_id}: {text[:100]}")


ping = on_command("ping")

@ping.handle()
async def handle_ping(bot: Bot, event: Event):
    await ping.finish("pong!")


echo = on_command("echo")

@echo.handle()
async def handle_echo(bot: Bot, event: Event):
    msg = event.get_plaintext()
    text = msg.replace("/echo", "", 1).strip()
    if text:
        await echo.finish(text)
    else:
        await echo.finish("说点什么让我复读呀~")


HELLO_KW = {"你好", "hello", "hi", "在吗", "在不在", "说话", "说话呀", "吱一声"}

hello = on_message()

@hello.handle()
async def handle_hello(bot: Bot, event: Event):
    if has_any(event.get_plaintext(), HELLO_KW):
        replies = ["你好呀！", "Hello!", "嗨~有什么可以帮你的？", "嘿嘿，你好~", "在的！有什么需要？"]
        await hello.finish(random.choice(replies))


# ---- /help ----
helper = on_command("help", aliases={"帮助", "菜单"})

@helper.handle()
async def handle_help(bot: Bot, event: Event):
    help_text = (
        "命令列表:\n"
        "/ping - 测试在线\n"
        "/echo <文字> - 复读\n"
        "/roll - 掷骰子\n"
        "/ai <问题> - AI问答\n"
        "/help - 帮助\n"
        "/clear - 清除AI记忆\n"
        "喊「有明」- AI聊天\n"
        "@我 - AI聊天\n"
        "说「你好」- 打招呼\n"
        "说「晚安」- 晚安回复\n"
        "说「吃了吗」- 随机回复\n"
        "说「几点了」- 报时\n"
        "说「打卡」- 打卡\n"
        "群聊中偶尔自动插话（5%概率）\n"
    )
    await helper.finish(help_text)


# ---- /roll ----
roll = on_command("roll")

@roll.handle()
async def handle_roll(bot: Bot, event: Event):
    result = random.randint(1, 100)
    await roll.finish(f"骰子点数: {result}")
