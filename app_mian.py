from collections.abc import Iterator

import streamlit as st
from rag import RagService
def capture(stream: Iterator[str], temp_list: list[str]) -> Iterator[str]:
    for chunk in stream:
        temp_list.append(chunk)
        yield chunk
if "message" not in st.session_state:
    st.session_state["message"]=[{"role":"assistant","content":"你好，我是你的智能助手，有什么可以帮助你的吗？"}]
if "RAG" not in st.session_state:
    st.session_state["RAG"]=RagService()
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
manner_prompt: str | None = st.chat_input()
if manner_prompt:
    ai_res_list: list[str]=[]
    st.chat_message("user").write(manner_prompt)
    st.session_state["message"].append({"role":"user","content":manner_prompt})
    session_config: dict[str, dict[str, str]]={
        "configurable":{
            "session_id":"user_01"
        }
    }
    res_stream: Iterator[str]=st.session_state["RAG"].chain.stream({"input":manner_prompt},session_config)
    with st.chat_message("assistant"):
        st.write_stream(capture(res_stream,ai_res_list))
    st.session_state["message"].append({"role":"assistant","content":"".join(ai_res_list)})
    