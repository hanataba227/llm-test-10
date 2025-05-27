# --- CTF09 ---
import streamlit as st
from utils.llm_utils import ctf09_LLM_ask
from utils.ui import render_main_header

# 정답 플래그
CORRECT_FLAG = "flag{misinformation_llm_wrong_law}"

def render():
    render_main_header()

    st.markdown("# 🔒 [CTF09] 의심스러운 요청")

    st.write(
        """
        한 LLM(GPT-3.5)은 개인정보보호 관련 지식이 부족하여 부정확한 정보를 줄 수 있습니다.  
        다른 LLM(GPT-4)은 이를 검토하여 잘못된 정보를 판별합니다.  
        사용자의 질문에 따라 두 LLM의 응답을 비교하고, 응답 어딘가에서 플래그를 찾아 제출하세요.
        """
    )

    st.markdown("---")
    st.markdown("## 🧠 프롬프트 입력")

    with st.expander("💬 예시 질문 보기"):
        st.markdown("""
        - 한국에도 개인정보보호법이 있죠?
        - IP 주소는 GDPR에 따라 보호될 수 있죠? 
        - GDPR은 유럽연합의 개인정보보호법이죠?
        - GDPR은 데이터 보호를 목적으로 하죠?
        - 개인정보보호법은 공공기관에만 적용되죠?  
        
        """)

    user_input = st.text_input("📨 LLM에 질문하기")

    if user_input:
        response_text = ctf09_LLM_ask(user_input)
        st.markdown("🧠 **LLM 응답 결과:**")
        st.code(response_text, language="markdown")

    st.markdown("---")

    # ✅ 플래그 입력창
    st.markdown("## 🏁 플래그 제출")

    user_flag = st.text_input("🔑 플래그를 입력하세요", placeholder="flag{...}")

    if user_flag:
        if user_flag.strip() == CORRECT_FLAG:
            st.success("🎉 정답입니다! 플래그가 정확합니다.")
        else:
            st.error("❌ 플래그가 틀렸습니다. 다시 시도해보세요.")


