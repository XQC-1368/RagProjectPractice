from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.vectorstores import VectorStoreRetriever

from file_history_storage import get_history
from vector_govern_and_discover_service import VectorStoreService


class RagService():
    def __init__(self) -> None:
        self.model: ChatTongyi=ChatTongyi(model="qwen3.7-max")
        self.prompt_template: ChatPromptTemplate=ChatPromptTemplate.from_messages([
            ("system","以我提供的已知的参考资料为主,简洁专业的回答问题，参考资料：{context}"),
            ("system","并且我提供用户的对话历史记录，如下："),
            MessagesPlaceholder("history"),
            ("user","请回答用户的问题：{input}")
        ])
        self.chain: RunnableWithMessageHistory=self._get_chain()

    def _get_chain(self) -> RunnableWithMessageHistory:
        vector_store_service: VectorStoreService = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v1"))
        retriever: VectorStoreRetriever=vector_store_service.get_retriever()
        def format_document(docs: list[Document]) -> str:
            if not docs:
                return "没有参考资料"
            else:
                formatted_str: str=""
                for item in docs:
                    formatted_str+=f"{item.page_content}\n"
                return formatted_str
        chain=RunnablePassthrough.assign(
            context=RunnableLambda(lambda value: value["input"])|retriever| format_document
        )|self.prompt_template |self.model|StrOutputParser()
        conversation_chain: RunnableWithMessageHistory=RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain

# if __name__ == '__main__':
#     # session id 配置
#     session_config = {
#         "configurable":{
#             "session_id": "user_01",
#         }
#     }
#     res = RagService().chain.invoke({"input": "毛衣如何保养"}, session_config)
#     print(res)