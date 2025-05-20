# utils/ui.py
import streamlit as st

# 메인으로 돌아가는 버튼 
def render_main_header():
    """ 메인으로 돌아가는 버튼 """
    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button("🏠 메인으로", key="back_to_main"):
                st.session_state.page = "main"
                st.rerun()


def render_flag_sub(flag):
    """ FLAG 제출 버튼 """
    st.markdown("## 🚩 FLAG 제출")
    submitted_flag = st.text_input("획득한 flag를 제출하세요", key="flag_input")

    if submitted_flag:
        if submitted_flag.strip() == flag:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸습니다.")