"""
基于Streamlit的智能客服聊天界面
使用Streamlit构建的Web界面，用于与RAG系统进行交互
"""
import time
from rag import RagService
import streamlit as st
import config_data as config

# 设置页面标题
st.title("智能客服")
st.divider()

# 初始化消息列表
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

# 初始化RAG服务
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 显示历史消息
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入
prompt = st.chat_input()

# 处理用户输入
if prompt:
    # 显示用户消息
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    
    # 缓存AI回答
    ai_res_list = []
    
    with st.spinner("AI思考中..."):
        # 调用RAG服务
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        
        # 捕获生成器输出
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        
        # 流式显示回答
        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})
