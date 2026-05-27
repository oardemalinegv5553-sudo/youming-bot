from nonebot import on_command, on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
import os
import random

# 表情包目录
MEME_DIR = "C:/Users/26241/qq-bot/memes"
# 确保目录存在
os.makedirs(MEME_DIR, exist_ok=True)


# ---- /img <文件名> 发送表情包 ----
img_cmd = on_command("img")

@img_cmd.handle()
async def handle_img(bot: Bot, event: Event):
    name = event.get_plaintext().replace("/img", "", 1).strip()

    if name:
        # 找匹配的文件
        for ext in [".png", ".jpg", ".gif", ".jpeg", ".webp"]:
            fpath = os.path.join(MEME_DIR, name + ext)
            if os.path.exists(fpath):
                await img_cmd.finish(MessageSegment.image("file:///" + fpath.replace("\\", "/")))

        await img_cmd.finish(f"没找到表情「{name}」，放到 {MEME_DIR} 目录下就能用了")


# ---- 关键词随机表情包 ----
sticker_kw = on_keyword({"表情包", "来张图", "发张图", "斗图"})

@sticker_kw.handle()
async def handle_sticker(bot: Bot, event: Event):
    memes = []
    for f in os.listdir(MEME_DIR):
        if f.lower().endswith((".png", ".jpg", ".gif", ".jpeg", ".webp")):
            memes.append(os.path.join(MEME_DIR, f))

    if not memes:
        await sticker_kw.finish(f"表情包目录还是空的，把图放到 {MEME_DIR} 下就能斗图了")
        return

    pick = random.choice(memes)
    await sticker_kw.finish(MessageSegment.image("file:///" + pick.replace("\\", "/")))


# ---- 查看表情包列表 ----
list_cmd = on_command("memes", aliases={"表情列表"})

@list_cmd.handle()
async def handle_list(bot: Bot, event: Event):
    memes = []
    for f in os.listdir(MEME_DIR):
        if f.lower().endswith((".png", ".jpg", ".gif", ".jpeg", ".webp")):
            memes.append(os.path.splitext(f)[0])

    if not memes:
        await list_cmd.finish("还没人投喂表情包~")
    else:
        await list_cmd.finish("表情包列表:\n" + "\n".join(memes[:30]))
