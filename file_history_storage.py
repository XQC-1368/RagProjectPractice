import json
import os
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, messages_from_dict, messages_to_dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_history(session_id: str) -> "FileChatMessageHistory":
    return FileChatMessageHistory(storage_path=os.path.join(BASE_DIR, 'history_storage'), session_id=session_id)
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, storage_path: str, session_id: str) -> None:
        self.session_id: str = session_id
        self.storage_path: str = storage_path
        self.file_path: str = os.path.join(storage_path, session_id)
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
    @property
    def messages(self) -> list[BaseMessage]:
        if not os.path.exists(self.file_path):
            return []
        else:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return messages_from_dict(json.load(file))
                 # 整个 dict 列表 → 整个消息对象列表

    def add_message(self, message: BaseMessage) -> None:
        messages: list[BaseMessage] = self.messages
        messages.append(message)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(messages_to_dict(messages), file)
              # 单个消息对象 → 单个 dict

    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
            
# if __name__ == '__main__':
#     storage_path = os.path.join(BASE_DIR, 'history_storage')
#     history = FileChatMessageHistory(storage_path, 'test_session')
#     history.add_message(HumanMessage('你好'))
#     history.add_message(AIMessage('你好！有什么可以帮你的？'))
#     print('写入后:', history.messages)

#     reopened = FileChatMessageHistory(storage_path, 'test_session')
#     print('重新打开:', reopened.messages)

#     reopened.clear()
#     print('清空后:', reopened.messages)
    
        