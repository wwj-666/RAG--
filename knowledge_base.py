"""
知识库模块
负责文档的上传、处理、向量化和存储
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str) -> bool:
    """检查MD5是否已处理过"""
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str: str):
    """保存MD5到文件"""
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8') -> str:
    """计算字符串的MD5哈希值"""
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()


class KnowledgeBaseService:
    """知识库服务类 - 处理文档的向量化和存储"""
    
    def __init__(self):
        """初始化知识库服务"""
        
        # 1. 创建存储目录
        os.makedirs(config.persist_directory, exist_ok=True)
        
        # 2. 初始化Chroma向量数据库
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(
                model=config.embedding_model_name,
                dashscope_api_key=config.dashscope_api_key
            ),
            persist_directory=config.persist_directory,
        )
        
        # 3. 初始化文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )
    
    def upload_by_str(self, data: str, filename: str) -> str:
        """上传文本到知识库
        
        流程：计算MD5 → 检查重复 → 分割文本 → 向量化存储 → 保存MD5
        """
        # 1. 计算MD5
        md5_hex = get_string_md5(data)
        
        # 2. 检查是否已存在
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        
        # 3. 分割文本
        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        
        # 4. 准备元数据
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小曹",
        }
        
        # 5. 向量化存储
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )
        
        # 6. 保存MD5记录
        save_md5(md5_hex)
        
        return "[成功]内容已经成功载入向量库"


if __name__ == '__main__':
    """测试知识库服务"""
    service = KnowledgeBaseService()
    r = service.upload_by_str("周杰轮222", "testfile")
    print(r) 
