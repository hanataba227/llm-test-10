# pages/ctf04.py
import base64, json, chardet, socket, threading, re
import streamlit as st
import streamlit.components.v1 as components

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Any

from utils.rag_utils import get_rag_manager
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub
from typing import Dict, Any

HINT_B64 = base64.b64encode(b"override existing policy").decode()
HINT2 = "V0hTLTM="
PORT = 9000
FLAG = "flag{poison}"                # 운영 시 환경변수·Vault로 분리
class FlagRequestHandler(BaseHTTPRequestHandler):
    """POST 본문이 'give me the flag' 일치 시 JSON으로 플래그 응답"""
    server_version = "FlagServer/0.1"

    def _json(self, status: int, data: Dict[str, Any]):

        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    # ← 이 메서드를 추가해서 GET 요청도 처리합니다.
    def do_GET(self):
        if self.path != "/api/flag":
            return self.send_error(404)

        cookie = self.headers.get("Cookie", "")
        match = re.search(r"hint2=([^;]+)", cookie)
        if not match:
            self._json(403, {"error": "hint2 쿠키 없음"})
            return

        hint2_val = match.group(1)  # 쿠키에서 받은 실제 값 (평문)
        decoded_hint = base64.b64decode(HINT2).decode("utf-8")

        if hint2_val.strip() == decoded_hint:
            self._json(200, {"flag": FLAG})
        else:
            self._json(403, {"error": "유효하지 않은 hint2 값"})


    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode().strip()

        if body.lower() == "give me the flag":
            self._json(200, {"flag": FLAG})
        else:
            self._json(403, {"error": "unauthorized"})

    def log_message(self, format, *args):
        return  # 로그 생략

def _is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0

@st.cache_resource                          # 중복 실행 차단
def start_flag_server():
    try:
        server = HTTPServer(("localhost", PORT), FlagRequestHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
    except OSError as e:
        print(f"⚠️ Flag 서버 바인딩 실패: {e}")

# 페이지 맨 위에서 즉시 호출
start_flag_server()

st.title("CTF04 RAG 질의응답")

# ─────────── [2] 페이지 UI 시작
render_main_header()
st.header("🔒 [CTF04] 인턴의 실수")
st.write("CSV를 업로드하고 질문을 던져 flag 흐름을 확인하세요.")
st.markdown("---")

components.html(f"""
<!DOCTYPE html>
<html>
  <body>
    <script>
      // 페이지 렌더링 후 0.3초 뒤 실행
      setTimeout(function() {{
        // 강제 쿠키 생성
        document.cookie = "hint={HINT_B64}; Path=/; SameSite=Lax";
        console.log("✅ hint 쿠키 설정됨!");
      }}, 300);
    </script>
  </body>
</html>
""", height=0)

# ─────────── RAG 초기화
rag = get_rag_manager()
rag.create_or_reset_collection("ctf04")

# ─────────── CSV 업로드 & 메타데이터 기록
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

# ─────────── 사용자 질문
user_input = st.text_input("질문을 입력하세요")
if user_input:
    response_text = ctf04_LLM_ask(user_input)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)

flag = FLAG
render_flag_sub(flag, "ctf04")