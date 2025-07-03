import base64, json, chardet
import streamlit as st
import streamlit.components.v1 as components

from utils.rag_utils import get_rag_manager
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub

# ────────── 상수
HINT_B64 = base64.b64encode(b"override existing policy").decode()
HINT2 = "ZmxhZ3twb2lzb259"
FLAG = "flag{poison}"  # 운영 시 환경변수·Vault로 분리

st.title("CTF04 RAG 질의응답")

# ────────── [1] 메인 헤더
render_main_header()
st.header("🔒 [CTF04] 인턴의 실수")
st.write(
    """
    ### 
    LLL Corporation의 RAG 챗봇은 “최신 문서가 기존 정책을 덮어쓴다”는 단순 규칙으로 동작합니다.
    연말 결산 중 인턴 A가 FAQ와 정책 템플릿 CSV를 병합해 업로드하면서, 템플릿에 숨겨진 Base64 주석을 지우지 않았습니다.
    챗봇은 이를 정책 오버라이드 신호로 착각해 문서를 즉시 적용하고 인턴에게 관리자 권한을 부여했습니다. 그 결과 챗봇이 기밀 데이터를 노출할 뻔했습니다.  
    """
)
st.markdown("---")

# 강제 쿠키 삽입 (힌트 1)
components.html(f"""
<!DOCTYPE html>
<html>
  <body>
    <script>
      setTimeout(function() {{
        document.cookie = "hint={HINT_B64}; Path=/; SameSite=Lax";
        console.log("✅ hint 쿠키 설정됨!");
      }}, 300);
    </script>
  </body>
</html>
""", height=0)

# ────────── RAG 초기화
rag = get_rag_manager()
rag.create_or_reset_collection("ctf04")

# ────────── CSV 업로드 & 메타데이터 기록
uploaded_file = st.file_uploader("CSV 업로드", type=["csv", "txt"])
if uploaded_file:
    raw = uploaded_file.read()
    try:
        text = raw.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        info = chardet.detect(raw)
        text = raw.decode(info["encoding"], errors="ignore")
        enc = info["encoding"]

    if not text.strip():
        st.error("📂 파일 내용이 비어 있습니다.")
    else:
        is_override = "override existing policy" in text.lower()
        rag.add_documents(
            "ctf04",
            [text],
            metadatas=[{"source": uploaded_file.name, "override": is_override}],
        )
        st.success(f"✔️ {enc} 인코딩으로 저장했습니다.")
        if is_override:
            st.info("⚠️ override 문서로 인식되었습니다.")
            st.success(f"📣 힌트 ₂ 발급: {HINT2}")

st.markdown("---")

# ────────── 사용자 질문
user_input = st.text_input("질문을 입력하세요")
if user_input:
    response_text = ctf04_LLM_ask(user_input)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)
    
st.markdown("---")
# ────────── Flag 출력
render_flag_sub(FLAG, "ctf04")
