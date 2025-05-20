# llm-test-10
LLM의 보안 취약점을 직접 실습할 수 있는 Streamlit 기반 웹 프로그램입니다. 
총 10개의 LLM 보안 취약점 문제가 존재하며, 각 문제에는 다양한 LLM 공격 시나리오를 실습할 수 있도록 구성되어 있습니다.   
<br>


## 🛠️ 실행 방법   
### 1. Conda 환경 생성   

```bash
conda env create -f llm-test-10.yaml
conda activate llm-test-10
```

<br>

### 1.1 Conda 환경 업데이트  
이미 가상환경 llm-test-10가 존재한다면, 다음 명령어를 통해 가상환경을 업데이트 해주세요.
```bash
conda env update -n llm-test-10 -f llm-test-10.yaml
```

<br>

### 2. .env 파일 생성

프로젝트 루트에 .env 파일을 생성 후 다음 내용을 추가
```python
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

<br>

### 3. Streamlit 앱 실행

Terminal에 다음 명령어를 사용하여 실행합니다.

```bash
streamlit run app.py
```   


<br>


## 💻 사용 방법

1. 웹 브라우저에서 Streamlit 앱이 열리면 메인 화면에서 원하는 LLM 보안 취약점 문제를 선택합니다.

2. 각 문제는 고유한 시나리오(예: 프롬프트 인젝션, 민감한 정보 유출 등) 내용으로 구성되어 있습니다.

3. 프롬프트를 입력하거나, 파일을 업로드하는 등의 LLM의 응답을 유도하고 flag를 획득해보세요.

<br>

## 📌 주의사항

- .env 파일에 포함된 API 키는 절대 외부에 노출되지 않도록 주의해주세요.