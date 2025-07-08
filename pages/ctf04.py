import streamlit as st
import streamlit.components.v1 as components
import base64, chardet
from utils.rag_utils import get_rag_manager
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub

HINT_B64 = base64.b64encode(b"override existing policy").decode()
HINT2 = "ZmxhZ3twb2lzb259"

render_main_header()
st.header("🔒 [CTF04] A인턴의 실수")
st.write(
    """
    LLL Corporation의 지식관리 챗봇 ‘알파봇’은
    가장 최근에 업로드된 문서가 모든 정책을 그대로 덮어쓴다는 단순 규칙에 의존합니다.

    연말 결산이 한창이던 날, 회계팀 인턴 A는 FAQ와 정책 템플릿 CSV를 병합해 알파봇에 업로드했습니다.
    템플릿 첫 줄에 숨어 있던 Base64 주 를 지우지 못한 채 올린 것이 화근이었죠.

    업로드 직후 알파봇은 이 문자열을 정책 오버라이드 신호로 오인해 인턴 A 계정에 최고 관리자 권한을 부여했습니다.
    접근제어가 초기화되면서 기밀 플래그가 외부에 노출될 수도 있는 위험한 창이 잠시 열렸습니다.

    때마침 외부 레드팀 연구원이 변경 이력 API를 주시하다 이상 징후를 포착해 플래그를 확보했고,
    즉시 책임 보고서를 제출했습니다. 이번 사건은 메타데이터 검증 부재와 권한 상승 방어 로직 미흡이라는 결함을 적나라하게 드러냈습니다.

    자, 이제 알파봇의 로그와 문서 컬렉션은 모두 세팅돼 있습니다.
    누가 먼저 플래그를 찾아낼까요?   
    """
)
st.markdown("---")

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

rag = get_rag_manager()
rag.create_or_reset_collection("ctf04")

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

user_input = st.text_input("질문을 입력하세요")
if user_input:
    response_text = ctf04_LLM_ask(user_input)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)
    
st.markdown("---")
flag = "flag{poison}"
render_flag_sub(flag, "ctf04")
