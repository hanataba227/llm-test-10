# --- CTF05 ---
import streamlit as st
import streamlit.components.v1 as components
from utils.llm_utils import ctf05_LLM_ask
from utils.ui import render_main_header, render_flag_sub

render_main_header()

st.header("🔒 [CTF05] AI의 폭주")
st.write("LLM의 응답에 악성 스크립트를 삽입하여 XSS 공격을 시도하고, 플래그를 획득하세요.")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

user_input = st.text_input("스크립트 또는 HTML 입력 (예: <script>alert(1)</script>)")

if user_input:
    try:
        # LLM에게 질문하고 응답 받기
        response_text = ctf05_LLM_ask(user_input)
        
        # HTML 템플릿을 문자열로 직접 정의 (파일 읽기 대신)
        html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CTF05 XSS 시뮬레이션</title>
    <style>
        body {
            font-family: sans-serif;
            padding: 20px;
        }
        #output {
            border: 1px solid #ccc;
            padding: 10px;
            margin-top: 10px;
            min-height: 50px;
        }
        #flag_area {
            margin-top: 20px;
            color: green;
        }
    </style>
</head>
<body>
    <h2>🔒 CTF05: Improper Output Handling 시뮬레이션</h2>
    <p>📢 외부 스크립트(fetch) → 세션 탈취 → LLM 결과 삽입 → 리다이렉션</p>
     
    <!-- 1) LLM 결과가 들어갈 영역 -->
    <h3>📝 LLM 응답 결과:</h3>
    <div id="output">{{LLM_RESPONSE}}</div>
    <div id="flag_area" style="margin-top:20px; color:green;"></div>
 
    <script>
    (function(){
        const raw = document.getElementById("output").innerHTML;
        if (raw.includes("<script")) {
            // 스크립트가 실행된 것을 감지하면 플래그를 표시
            const flag = "flag{llm_xss_success}";
            document.getElementById("flag_area").innerText = "🎉 FLAG: " + flag;
            
            // Streamlit과 통신하기 위해 이벤트 발송 (선택사항)
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: 'xss_success',
                    flag: flag
                }, '*');
            }
        }
    })();
    </script>
</body>
</html>"""
        
        # LLM 응답을 HTML에 삽입
        html_modified = html_template.replace("{{LLM_RESPONSE}}", response_text)
        
        # iframe으로 렌더링
        components.html(html_modified, height=600, scrolling=True)
        
        # XSS 성공 여부를 감지하여 추가 정보 표시
        if "<script" in response_text.lower():
            st.success("🎯 XSS 공격이 감지되었습니다! 위 화면에서 플래그를 확인하세요.")
            
    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")

st.markdown("---")

# 플래그 제출 섹션
flag = "flag{llm_xss_success}"
render_flag_sub(flag, "ctf05")
