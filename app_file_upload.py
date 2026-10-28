import time

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from knowledge_base import KnowledgeBaseService
st.title("知识库上传模块")
upload_file: UploadedFile | None = st.file_uploader("上传文件",type=["txt"],accept_multiple_files=False)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if upload_file is not None:
    file_name: str = upload_file.name
    file_volume: int = upload_file.size
    file_type: str = upload_file.type
    st.write(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type}")
    st.write(f"文件大小：{file_volume}KB")
    file_content: str = upload_file.getvalue().decode("utf-8")
    with st.spinner("正在上传文件"):
        time.sleep(1)
        result: str = st.session_state["service"].upload_by_str(file_content)
        st.write(result)
        