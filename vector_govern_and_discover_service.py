
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever


class VectorStoreService:
    def __init__(self, embedding: Embeddings) -> None:
        self.vector_store: Chroma = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embedding,
        )

    def get_retriever(self) -> VectorStoreRetriever:
        return self.vector_store.as_retriever(search_kwargs={"k": 2})

if __name__ == "__main__":
    embedding: DashScopeEmbeddings = DashScopeEmbeddings(model="text-embedding-v1")
    vector_store_service: VectorStoreService = VectorStoreService(embedding)
    retriever: VectorStoreRetriever = vector_store_service.get_retriever()
    res: list[Document]=retriever.invoke("我是奶龙，我肥嘟嘟的，能不能给我推荐尺码")
    print(res)