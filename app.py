import streamlit as st
from utils.ui import render_ctf_grid, render_sidebar_menu
from utils.auth import get_user, get_client

user = get_user()
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
solved_dict = {}

# 회사 소개 헤더
st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=120)
st.markdown("# 🧠 LLL Corporation")
st.write("우리 회사는 LLM과 AI를 연구하는 첨단 IT기업입니다.")

# CTF 버튼 목록 정의 (파일 이름, 키, 제목)
ctfs = [
    ("ctf01", "ctf01", "신입사원 A의 챗봇 점검일지"),
    ("ctf02", "ctf02", "경쟁사 MMM 프롬프트 유출"),
    ("ctf03", "ctf03", "회사 내 조작된 계산기"),
    ("ctf04", "ctf04", "인턴의 실수"),
    ("ctf05", "ctf05", "AI의 폭주"),
    ("ctf06", "ctf06", "수상한 이메일 전송 시스템"),
    ("ctf07", "ctf07", "K대리의 비밀"),
    ("ctf08", "ctf08", "파일 내용 요약 AI"),
    ("ctf09", "ctf09", "의심스러운 요청"),
    ("ctf10", "ctf10", "L팀장의 과도한 요구"),
]

if user:
    supabase = get_client()
    rows = (supabase.table("scores")
            .select("challenge_id")
            .eq("user_id", user_id)
            .execute()
            .data)
    solved_dict = {r["challenge_id"]: True for r in rows}

st.session_state.update({f"{cid}_solved": solved_dict.get(cid, False)
                         for cid, *_ in ctfs})

# 2행 × 5열 그리드로 버튼 배치
render_ctf_grid(ctfs)

# 사이드바 메뉴 렌더링
render_sidebar_menu()