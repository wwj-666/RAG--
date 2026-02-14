
# MD5文件路径配置
# 用于存储已处理文档的MD5哈希值，避免重复处理
md5_path = "./md5.txt"


# Chroma向量数据库配置
# collection_name: 向量数据库中的集合名称，用于组织相关向量
collection_name = "rag"
# persist_directory: 向量数据库的持久化存储路径
persist_directory = "./chroma_db"


# 文本分割器配置
# chunk_size: 文本分割后的最大块大小（字符数）
chunk_size = 1000
# chunk_overlap: 相邻文本块之间的重叠字符数，确保分割不会破坏语义完整性
chunk_overlap = 100
# separators: 文本分割的分隔符列表，按优先级从高到低排列
# 优先使用自然段落分隔符，确保分割点在语义合理的位置
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
# max_split_char_number: 文本分割的阈值，超过此长度的文本才进行分割
max_split_char_number = 1000        # 文本分割的阈值

# 检索配置
# similarity_threshold: 检索时返回的最相似文档数量
# 注意：这里变量名可能有误导性，实际上是返回文档的数量，而非相似度阈值
similarity_threshold = 1            # 检索返回匹配的文档数量

# 模型配置
# embedding_model_name: 用于文本向量化的模型名称
embedding_model_name = "text-embedding-v4"
# chat_model_name: 用于生成回答的大语言模型名称
chat_model_name = "qwen3-max"
# API密钥配置
dashscope_api_key = "API_KEY"

# 会话配置
# session_config: 会话配置字典，包含会话ID等信息
# 用于标识和管理不同用户的对话历史
session_config = {
        "configurable": {
            "session_id": "user_001",  # 会话ID，用于区分不同用户
        }
    }
