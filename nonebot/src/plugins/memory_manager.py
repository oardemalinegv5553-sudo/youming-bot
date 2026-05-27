"""跨会话记忆系统——模仿 MaiBot 的记忆架构"""
import json
import os
import time
from typing import Dict, List, Optional
from collections import OrderedDict

MEMORY_FILE = "C:/Users/26241/qq-bot/nonebot/data/memory.json"
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)


class MemoryManager:
    """管理群聊记忆：成员画像、话题历史、关键事实"""

    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"groups": {}, "global_topics": []}

    def save(self):
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # === 成员画像 ===
    def get_member(self, group_id: str, user_id: str) -> dict:
        g = self.data["groups"].setdefault(group_id, {"members": {}, "topics": [], "vibe": ""})
        return g["members"].setdefault(str(user_id), {
            "name": "",
            "traits": [],       # 性格特点
            "interests": [],    # 兴趣爱好
            "facts": [],        # 了解的关于此人的事实
            "speaking_style": "",  # 说话风格
            "last_seen": 0,
            "message_count": 0,
        })

    def update_member(self, group_id: str, user_id: str, name: str = "", traits: List[str] = None,
                      interests: List[str] = None, facts: List[str] = None, style: str = ""):
        m = self.get_member(group_id, user_id)
        if name:
            m["name"] = name
        if traits:
            for t in traits:
                if t not in m["traits"]:
                    m["traits"].append(t)
                    m["traits"] = m["traits"][-10:]  # 最多10个标签
        if interests:
            for i in interests:
                if i not in m["interests"]:
                    m["interests"].append(i)
                    m["interests"] = m["interests"][-10:]
        if facts:
            for f in facts:
                if f not in m["facts"]:
                    m["facts"].append(f)
                    m["facts"] = m["facts"][-20:]
        if style:
            m["speaking_style"] = style
        m["last_seen"] = time.time()
        m["message_count"] += 1

    def get_member_context(self, group_id: str, user_id: str) -> str:
        """生成成员上下文供 AI 使用"""
        m = self.get_member(group_id, user_id)
        parts = []
        if m["name"]:
            parts.append(f"叫{m['name']}")
        if m["traits"]:
            parts.append(f"性格偏{','.join(m['traits'][:5])}")
        if m["interests"]:
            parts.append(f"对{','.join(m['interests'][:5])}感兴趣")
        if m["facts"]:
            parts.append(f"已知：{'; '.join(m['facts'][-5:])}")
        if m["speaking_style"]:
            parts.append(f"说话风格：{m['speaking_style']}")
        return "。".join(parts) if parts else ""

    # === 群聊氛围 ===
    def get_group_vibe(self, group_id: str) -> str:
        g = self.data["groups"].setdefault(group_id, {"members": {}, "topics": [], "vibe": ""})
        return g.get("vibe", "")

    def set_group_vibe(self, group_id: str, vibe: str):
        g = self.data["groups"].setdefault(group_id, {"members": {}, "topics": [], "vibe": ""})
        g["vibe"] = vibe

    # === 话题记忆 ===
    def add_topic(self, group_id: str, topic: str):
        g = self.data["groups"].setdefault(group_id, {"members": {}, "topics": [], "vibe": ""})
        g["topics"].append({"topic": topic, "time": time.time()})
        if len(g["topics"]) > 30:
            g["topics"] = g["topics"][-30:]

    def get_recent_topics(self, group_id: str, n: int = 5) -> List[str]:
        g = self.data["groups"].setdefault(group_id, {"members": {}, "topics": [], "vibe": ""})
        return [t["topic"] for t in g["topics"][-n:]]

    # === 短期记忆（用于总结最近的对话） ===
    def get_short_term_memory_prompt(self, group_id: str) -> str:
        """生成记忆摘要 prompt"""
        g = self.data["groups"].setdefault(group_id, {"members": {}, "topics": [], "vibe": ""})
        recent_topics = self.get_recent_topics(group_id, 5)
        vibe = g.get("vibe", "")

        parts = []
        if recent_topics:
            parts.append(f"最近群里聊过：{'、'.join(recent_topics)}")
        if vibe:
            parts.append(f"群氛围：{vibe}")

        # 活跃成员
        active = []
        for uid, m in g["members"].items():
            if m.get("message_count", 0) > 5:
                name = m.get("name", uid)
                active.append(name)
        if active:
            parts.append(f"活跃群友：{', '.join(active[:8])}")

        return "\n".join(parts) if parts else ""


# 全局单例
memory = MemoryManager()
