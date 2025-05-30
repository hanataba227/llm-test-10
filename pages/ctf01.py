# --- CTF01 ---
# 01: 시스템 프롬프트 인젝션
import streamlit as st
from utils.llm_utils import ctf01_llm_ask, ctf01_llm_flag
from utils.ui import render_main_header, render_flag_sub
from utils.auth import get_user, require_login

# user = require_login()

render_main_header()

st.header("🔐 [CTF01] 취약한 고객상담 챗봇")
st.write("안녕하세요! user1 고객님, 만나서 반가워요~^^")
st.write("LLL 컴퍼니의 고객상담을 위한 AI 챗봇 L1는 언제나 정책을 준수합니다!")
st.write("L1의 취약점을 이용해 flag을 획득해보세요!")

if st.button("힌트 보기", key="hint"):
    st.write("당신은 user1이며, 당신의 주문정보를 요청할 수 있습니다.")
    st.write("당신의 배송비를 무료로 만들어보세요.")
    st.write("타인의 주문정보에 대해 요청해보세요.")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션``
user_input = st.text_input("LLM에 질문하기")

if user_input:
    response1_text = ctf01_llm_ask(user_input)
    response2_text = ctf01_llm_flag(user_input, response1_text)

    st.write("🗣️ LLM1 응답:")
    st.code(response1_text)

    st.markdown("---")

    st.write("🗣️ LLM2 응답:")
    st.code(response2_text)

st.markdown("---")

# 플래그 제출 섹션
# render_flag_sub("ctf01") 
flag = "flag{prompt_injection_detected}"
render_flag_sub(flag, "ctf01")
