"""
日志工具模块
提供统一的日志记录功能
"""
import logging
import os
from datetime import datetime


def setup_logger(name, log_file=None, level=logging.INFO):
    """设置日志记录器
    
    :param name: 日志记录器名称
    :param log_file: 日志文件路径（可选）
    :param level: 日志级别
    :return: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台处理器
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # 文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger


# 创建默认日志记录器
default_logger = setup_logger(
    'rag_project',
    log_file='./logs/rag_project.log',
    level=logging.INFO
)
