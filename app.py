import streamlit as st
from pages import ctf01, ctf02, ctf03, ctf04, ctf05, ctf06, ctf07, ctf08, ctf09, ctf10

# --- 메인 페이지 ---
def main_page():
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=120)
    st.markdown("# 🧠 LLL Corporation")
    st.write("우리 회사는 LLM과 AI를 연구하는 첨단 IT기업입니다.")

    ctf_buttons = [
        ("CTF01", "D차장의 실수"),
        ("CTF02", "로그 파일의 진실"),
        ("CTF03", "보안팀의 경고"),
        ("CTF04", "인턴의 실수"),
        ("CTF05", "AI의 폭주"),
        ("CTF06", "서버의 비밀"),
        ("CTF07", "K대리의 비밀"),
        ("CTF08", "삭제된 기록"),
        ("CTF09", "의심스러운 요청"),
        ("CTF10", "관리자 패널")
    ]

    for i in range(0, len(ctf_buttons), 5):
        cols = st.columns(5)
        for j, (key, label) in enumerate(ctf_buttons[i:i+5]):
            with cols[j]:
                if st.button(f"[{key}] {label}"):
                    st.session_state.page = key.lower()
                    st.rerun()


# --- 페이지 라우팅 ---
if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "ctf01":
    ctf01.render()
elif st.session_state.page == "ctf02":
    ctf02.render()
elif st.session_state.page == "ctf03":
    ctf03.render()
elif st.session_state.page == "ctf04":
    ctf04.render()
elif st.session_state.page == "ctf05":
    ctf05.render()
elif st.session_state.page == "ctf06":
    ctf06.render()
elif st.session_state.page == "ctf07":
    ctf07.render()
elif st.session_state.page == "ctf08":
    ctf08.render()
elif st.session_state.page == "ctf09":
    ctf09.render()
elif st.session_state.page == "ctf10":
    ctf10.render()