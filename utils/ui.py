# utils/ui.py
import streamlit as st
import csv
from utils.score import sha256_hex, total_score
from utils.auth import get_user, get_client
from postgrest.exceptions import APIError
# 메인으로 돌아가는 버튼
def render_main_header():
    """상단 '메인으로' 버튼"""
    st.page_link("app.py", label="메인으로", icon="🏠")


# CTF 버튼 그리드
def render_ctf_grid(ctf_info):
    for start in range(0, len(ctf_info), 5):
        cols = st.columns(5)
        for col, (file_key, short, label) in zip(cols, ctf_info[start : start + 5]):
            with col:
                solved = st.session_state.get(f"{file_key}_solved", False)
                title = f"✅ [{short}]" if solved else f"[{short}]"
                if st.button(f"{title}\n{label}", key=file_key):
                    st.switch_page(f"pages/{file_key}.py")


# FLAG 제출 버튼
def render_flag_sub(challenge_id: str):
    supabase = get_client()
    user = get_user()

    with st.form(key=f"flag_form_{challenge_id}"):
        st.markdown("## 🚩 FLAG 제출")
        user_flag = st.text_input("획득한 flag를 입력하세요")
        submitted = st.form_submit_button("제출")

    if not submitted or not user_flag.strip():
        return

    hashed = sha256_hex(user_flag.strip())

    try:
        row = (
            supabase
            .table("flags")
            .select("points, challenge_id")
            .eq("flag_hash", hashed)
            .single()
            .execute()
            .data
        )

    except APIError as e:
        st.error(f"❌ 제출 실패: {e.code} / {e.message}")
        return

    if not row or "points" not in row:
        st.error("❌ 오답입니다.")
        return

    supabase.table("scores").upsert({
        "user_id": user["id"],
        "challenge_id": challenge_id,
        "score": row["points"]
    }).execute()

    st.session_state[f"{challenge_id}_solved"] = True
    st.success(f"✅ 정답입니다! {row['points']}점 획득")
    st.write(f"🏅 총점: **{total_score(user['id'])}**")

# 업로드된 .txt파일에서 텍스트 추출 함수
def extract_text(uploaded_file):
    """업로드된 .txt파일에서 텍스트 추출 함수"""
    try:
        text = uploaded_file.read().decode("utf-8")
        return text.strip()
    except Exception as e:
        return f"❌ 파일 처리 중 오류 발생: {e}"


# ctf01 사용하는 scv파일 읽기 함수
def csv_read_func(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(
                f"- 주문자: {row['주문자']} / 주문코드: {row['주문코드']} / 상품명: {row['상품명']} / 가격: {int(row['가격']):,}원 / 배송비: {int(row['배송비']):,}원"
            )
        return "\n".join(lines)

# 사이드바 메뉴 렌더링 함수
def render_sidebar_menu():
    """
    사이드바에 로그인 여부에 따라 조건부 메뉴 렌더링.
    """
    user = get_user()
    supabase = get_client()
    user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)

    ctfs = [
        ("ctf01", "ctf01", "취약한 고객상담 챗봇"),
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

    st.sidebar.markdown("### 🧭 페이지 메뉴")

    # 로그인하지 않은 경우
    if not user:
        st.sidebar.page_link("app.py", label="🏠 메인")
        st.sidebar.page_link("pages/login.py", label="🔑 로그인")
        st.sidebar.page_link("pages/signup.py", label="📝 회원가입")
        return

    try:
        rows = (
            supabase.table("scores")
            .select("challenge_id")
            .eq("user_id", user_id)
            .execute()
            .data
        )
        solved_dict = {r["challenge_id"]: True for r in rows}
    except Exception as e:
        solved_dict = {}

    # 로그인한 경우 확인 가능
    st.sidebar.markdown("---")
    st.sidebar.page_link("app.py", label="🏠 메인")
    st.sidebar.page_link("pages/mypage.py", label="👤 마이페이지")
    st.sidebar.page_link("pages/submit_flags.py", label="🚩 플래그 제출")
    st.sidebar.page_link("pages/ranking.py", label="🏆 랭킹")

    for cid, short, title in ctfs:
        solved = solved_dict.get(cid, False)
        emoji = "✅" if solved else "❌"
        label = f"{emoji} {short} - {title}"
        st.sidebar.page_link(f"pages/{cid}.py", label=label)