"""
RAG（检索增强生成）服务模块
负责构建和管理RAG系统的核心流程
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi


def print_prompt(prompt):
    """打印提示词内容，用于调试"""
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt


class RagService:
    """RAG服务类 - 构建和管理RAG系统的完整流程"""
    
    def __init__(self):
        """初始化RAG服务：创建向量服务、提示词模板和聊天模型"""
        
        # 1. 初始化向量存储服务
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(
                model=config.embedding_model_name,
                dashscope_api_key=config.dashscope_api_key
            )
        )
        
        # 2. 创建提示词模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
            ("system", "并且我提供用户的对话历史记录，如下："),
            MessagesPlaceholder("history"),
            ("user", "请回答用户提问：{input}")
        ])
        
        # 3. 初始化聊天模型
        self.chat_model = ChatTongyi(
            model=config.chat_model_name,
            dashscope_api_key=config.dashscope_api_key
        )
        
        # 4. 构建执行链
        self.chain = self.__get_chain()
    
    def __get_chain(self):
        """构建完整的RAG执行链
        
        流程：输入 → 检索 → 构建提示词 → LLM生成 → 输出
        """
        # 获取检索器
        retriever = self.vector_service.get_retriever()
        
        # 定义格式化函数
        def format_document(docs: list[Document]) -> str:
            """将检索到的文档列表格式化为字符串"""
            if not docs:
                return "无相关参考资料"
            
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str
        
        def format_for_retriever(value: dict) -> str:
            """从输入字典中提取用户问题"""
            return value["input"]
        
        def format_for_prompt_template(value: dict) -> dict:
            """重新组织数据结构，适配提示词模板"""
            return {
                "input": value["input"]["input"],
                "context": value["context"],
                "history": value["input"]["history"]
            }
        
        # 构建基础执行链
        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriever | format_document
            } 
            | RunnableLambda(format_for_prompt_template) 
            | self.prompt_template 
            | print_prompt 
            | self.chat_model 
            | StrOutputParser()
        )
        
        # 包装为带消息历史的对话链
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        return conversation_chain


if __name__ == '__main__':
    """测试RAG服务"""
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    
    res = RagService().chain.invoke({"input": "针织毛衣如何保养？"}, session_config)
    print(res)
