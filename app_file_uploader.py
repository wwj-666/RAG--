"""
基于Streamlit的知识库文件上传服务
使用Streamlit构建的Web界面，用于上传TXT文件到知识库
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 设置页面标题
st.title("知识库更新服务")

# 创建文件上传组件
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,
)

# 初始化知识库服务
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 处理文件上传
if uploader_file is not None:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024
    
    # 显示文件信息
    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")
    
    # 读取文件内容
    text = uploader_file.getvalue().decode("utf-8")
    
    # 上传到知识库
    with st.spinner("载入知识库中。。。"):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)
