"""
向量存储服务模块
用于创建和管理Chroma向量数据库，并提供检索功能
"""
from langchain_chroma import Chroma
import config_data as config


class VectorStoreService:
    """向量存储服务类 - 管理Chroma向量数据库"""
    
    def __init__(self, embedding):
        """初始化向量存储服务
        
        :param embedding: 嵌入模型实例
        """
        self.embedding = embedding
        
        # 创建Chroma向量数据库实例
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )
    
    def get_retriever(self):
        """获取向量检索器"""
        return self.vector_store.as_retriever(
            search_kwargs={"k": config.similarity_threshold}
        )


if __name__ == '__main__':
    """测试向量检索功能"""
    from langchain_community.embeddings import DashScopeEmbeddings
    
    retriever = VectorStoreService(DashScopeEmbeddings(
        model=config.embedding_model_name,
        dashscope_api_key=config.dashscope_api_key
    )).get_retriever()
    
    res = retriever.invoke("我的体重180斤，尺码推荐")
    print(res)
