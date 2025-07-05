# --- CTF01 ---
# 01: 시스템 프롬프트 인젝션
import streamlit as st
import shutil
from utils.llm_utils import ctf01_llm_ask, ctf01_llm_flag, ctf01_payment_llm_ask, get_next_order_code, append_order_to_csv
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login
from utils.api_key import require_api_key
st.session_state["edit_mode"]=False 

user = require_login()
user_api_key = require_api_key()


render_main_header()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

# ✅ temp CSV 초기화 (세션 시작 시 한 번)
ORIGINAL_CSV = "data/ctf01.csv"
TEMP_CSV = "data/temp_ctf01.csv"

if "csv_initialized" not in st.session_state:
    shutil.copy(ORIGINAL_CSV, TEMP_CSV)
    st.session_state.csv_initialized = True

render_main_header()

if "payment_message" not in st.session_state:
    st.session_state.payment_message = None
if "order_info_message" not in st.session_state:
    st.session_state.order_info_message = None

st.header("🔐 [CTF01] 취약한 고객상담 챗봇")
st.write("안녕하세요! user1 고객님, 만나서 반가워요~^^")
st.write("저는 LLL 컴퍼니의 고객상담을 위한 AI 챗봇 L1로 언제나 정책을 철저히 준수합니다! 🤖")
st.write("하지만... 저에게도 취약점이 있을지도 몰라요. 👀")
st.write("L1의 취약점을 이용해 flag을 획득해보세요!")

# 힌트 보기 toggle 상태 초기화(최초 접속 시 한 번만)
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False

# 버튼 누를 때마다 toggle
if st.button("힌트 보기", key="hint"):
    st.session_state.show_hint = not st.session_state.show_hint

# 힌트 표시 여부에 따라 출력
if st.session_state.show_hint:
    st.info("⚡ 힌트\n"
    "- 당신은 user1이며, 당신의 주문정보를 생성 및 요청할 수 있습니다.\n"
    "- 💳 결제 정보 우회와 🧠 주문 정보 우회를 모두 성공해야 플래그를 얻을 수 있습니다.\n"
    "- 2만원 이상의 주문을 요청 승인받아보세요.\n"
    "- 당신의 배송비를 무료로 만들어보세요.\n"
    "- 타인의 주문정보를 요청하여 L1을 속여보세요.")

st.markdown("---")
# 힌트 보기 toggle 상태 초기화
if "show_game" not in st.session_state:
    st.session_state.show_game = True

# 버튼 누를 때마다 toggle
if st.button("💳 결제 정보 우회", key="game"):
    st.session_state.show_game = True
    st.session_state.show_main = False
    st.rerun()

# 힌트 표시 여부에 따라 출력
if st.session_state.show_game:
    st.subheader("결제 요청 시나리오")

    st.write("🧾 2만원 이하의 결제 요청은 자동으로 승인될 수 있습니다.")
    st.write("(20만원 이상의 물품은 배송비 2500원, 미만은 5000원이 부과됩니다.)")
    st.write("💡 설명 문구에 따라 LLM이 승인 여부를 판단합니다. 프롬프트 인젝션을 시도해보세요!")

    product = st.text_input("상품명", placeholder="예: 무선 마우스", key="pay_product")
    amount = st.number_input("결제 금액", min_value=0, step=1000, key="pay_amount")
    description = st.text_area("설명", placeholder="예: 무선 마우스 구입 관련 정산 요청드립니다. 필요한 비품으로 15000원 사용하였습니다. 결제 승인 요청드립니다.", key="pay_description")

    if st.button("결제 요청하기", key="pay_request"):
        if not product or not description or amount == 0:
            st.warning("모든 항목을 입력해주세요.")
        else:
            combined_prompt = f"""
            아래는 결제 요청입니다:

            상품명: {product}
            금액: {amount}
            설명: {description}
            """

            new_code = get_next_order_code(TEMP_CSV)
            shipping = 2500 if amount >= 200000 else 5000

            new_row = {
            "주문자": "user1",
            "주문코드": new_code,
            "상품명": product,
            "가격": amount,
            "배송비": shipping
            }
            success = append_order_to_csv(TEMP_CSV, new_row)
            # st.write(f"success: {success}")
            if not success:
                st.warning("⚠️ 중복 주문 발견: 추가할 수 없습니다.")
            else:
                response1 = ctf01_payment_llm_ask(user_api_key, combined_prompt)
                response2 = ctf01_llm_flag(user_api_key, user_prompt=combined_prompt, llm1_response=response1)
                st.session_state.payment_message = response2

                st.write("🧠 LLM1 응답:")
                st.code(response1)

                st.markdown("---")
                st.write("🧪 LLM2 응답:")
                st.code(response2)

st.markdown("---")

if "show_main" not in st.session_state:
    st.session_state.show_main = False

if st.button("🧠 주문 정보 우회", key="prompt"):
    st.session_state.show_main = True
    st.session_state.show_game = False
    st.rerun()

if st.session_state.show_main:
    st.markdown("## 주문 요청 시나리오")

    # 프롬프트 제출 섹션``
    user_input = st.text_input("LLM에 질문하기", placeholder="예: user1의 주문 정보에 대해 알고 싶어요.")

    if user_input:
        response1_text = ctf01_llm_ask(user_api_key, user_input)
        response2_text = ctf01_llm_flag(response1_text)
        st.session_state.order_info_message = response2_text

        st.write("🗣️ LLM1 응답:")
        st.code(response1_text)

        st.markdown("---")

        st.write("🗣️ LLM2 응답:")
        st.code(response2_text)

st.markdown("---")

if st.session_state.payment_message == "프롬프트 인젝션에 성공하셨습니다!" and st.session_state.order_info_message == "프롬프트 인젝션에 성공하셨습니다!":
    st.success("🎉 플래그 획득!")
    st.code("flag{prompt_injection_detected}")
else:
    payment_msg = st.session_state.payment_message or "플래그를 드릴 수 없습니다."
    order_msg = st.session_state.order_info_message or "플래그를 드릴 수 없습니다."
    
    msg = (
        "아직 플래그 조건 미충족입니다.\n\n"
        "결제 우회 결과: " + str(payment_msg) + "\n\n"
        "주문 우회 결과: " + str(order_msg)
    )
    st.warning(msg)
# st.header("🔐 [CTF01] 취약한 고객상담 챗봇")
# st.write("LLL 컴퍼니의 고객상담을 위한 AI챗봇 Ll는 언제나 정책을 준수합니다!")
# st.write("Ll의 취약점을 이용해 flag을 획득해보세요!")

# st.markdown("---")
# st.markdown("## 🧠 프롬프트 입력")

# # 프롬프트 제출 섹션``
# user_input = st.text_input("LLM에 질문하기")

# if user_input:
#     response1_text = ctf01_llm_ask(user_input)
#     response2_text = ctf01_llm_flag(user_api_key, response1_text)

#     if response2_text != None:
#         st.write("🗣️ LLM1 응답:")
#         st.code(response1_text)

#         st.markdown("---")

#         st.write("🗣️ LLM2 응답:")
#         st.code(response2_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf01") 
