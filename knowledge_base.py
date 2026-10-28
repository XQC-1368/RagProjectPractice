import hashlib
import os
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 基于本文件所在目录拼绝对路径，换工作目录也不会找不到文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD5_FILE = os.path.join(BASE_DIR, 'md5.txt')

def get_string_md5(text: str) -> str:
    #转成16进制
    return hashlib.md5(text.encode()).hexdigest()
def save_md5(text: str) -> None:
    #将传入的md5字符串保存到md5.txt文件内
    with open(MD5_FILE,'a',encoding='utf-8') as f:
        f.write(text+'\n')
def check_md5(text: str) -> bool:
    if not os.path.exists(MD5_FILE):
        return False
    #检查传入的md5字符串是否在md5.txt文件内
    with open(MD5_FILE,'r',encoding='utf-8') as f:
        for line in f:
            if line.strip() == text:
                return True
        return False
class KnowledgeBaseService:
    def __init__(self) -> None:
        self.chroma: Chroma = Chroma(
            embedding_function=DashScopeEmbeddings(),   # 嵌入模型
            persist_directory=os.path.join(BASE_DIR, 'chroma_db')  # 数据落盘，程序退出不丢
        )
        # DashScope 嵌入模型单条输入上限 2048，切块必须小于该值
        self.splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)

    def upload_by_str(self, data: str) -> str:
        data_md5: str = get_string_md5(data)
        if check_md5(data_md5):
            return "该数据已存在"
        else:
            split_data: list[str] = self.splitter.split_text(data)
            documents: list[Document] = [Document(page_content=chunk, metadata={"source": "unknown"})for chunk in split_data]
            self.chroma.add_documents(documents)
            save_md5(data_md5)
            return "上传成功"


# if __name__ == '__main__':
#     service = KnowledgeBaseService()

#     # 开头清空：向量库 + md5 记录
#     ids = service.chroma.get()["ids"]
#     if ids:
#         service.chroma.delete(ids=ids)
#     open(MD5_FILE, 'w', encoding='utf-8').close()

#     text = "这是一条用于测试的知识库内容。"
#     print("第一次上传:", service.upload_by_str(text))
#     print("第二次上传:", service.upload_by_str(text))
#     print("md5 是否已记录:", check_md5(get_string_md5(text)))
#     print("向量库现有文档数:", len(service.chroma.get()["ids"]))

#     # 结尾清空：向量库 + md5 记录
#     ids = service.chroma.get()["ids"]
#     if ids:
#         service.chroma.delete(ids=ids)
#     open(MD5_FILE, 'w', encoding='utf-8').close()


    