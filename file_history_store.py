"""
聊天历史存储模块
负责管理和持久化用户与系统的对话历史
"""
import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id: str) -> "FileChatMessageHistory":
    """获取指定会话ID的聊天历史对象"""
    return FileChatMessageHistory(session_id, "./chat_history")


class FileChatMessageHistory(BaseChatMessageHistory):
    """基于文件的聊天历史存储类"""
    
    def __init__(self, session_id: str, storage_path: str):
        """初始化文件聊天历史存储"""
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        
        # 确保存储文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """添加消息到聊天历史"""
        all_messages = list(self.messages)
        all_messages.extend(messages)
        
        # 转换为字典并写入文件
        new_messages = [message_to_dict(message) for message in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)
    
    @property
    def messages(self) -> list[BaseMessage]:
        """获取聊天历史消息"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
    
    def clear(self) -> None:
        """清空聊天历史"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
