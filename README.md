<p align="right"><a href="README.en.md">English</a> | 한국어</p>

# SlangChat

Slangchat은 규칙 기반 정규화, 형태소 분석, 사전 매칭 및 시맨틱 검색을 결합하여 한국어, 영어 슬랭을 탐지하고 문맥에 적합한 응답을 추천하는 다국어 자연어 처리 프로젝트입니다.

## 현재 범위

- 한국어/영어 슬랭 사전
- 데이터는 배치 검색 + LLM 초안 + 사람 검증(교차확인·블라인드 테스트) 파이프라인으로 수집
- 스키마 및 교차 레코드 품질 검증
- 강조 접두사 정규화 및 표제어·변형 사전 탐지
- Kiwi 형태소 분석 기반 한국어 활용형 탐지
- 하이브리드 슬랭 탐지(시맨틱 검색 구현 예정)
- FastAPI 기반 `/detect` API
- Streamlit 데모
- Precision/Recall/F1 및 응답시간 평가

## 데이터 검증

```bash
python3 -m scripts.validate_data data/slang.json
```
검증기는 필수 필드, 타입, ID-언어 일치, 중복 ID, 중복 표제어 및 표면형 충돌을 검사합니다.


테스트
```bash
python3 -m unittest discover -s tests -v
```

평가
```bash
python3 -m scripts.evaluate
```
사전 항목의 예문을 정답으로 삼아 탐지 정확도(Precision/Recall/F1)와 평균 응답 지연시간을 측정합니다.

API 실행
```bash
uvicorn slangchat.api.app:app --reload
```
POST /detect에 텍스트를 보내면 탐지된 은어 목록을 반환합니다.

```bash
curl -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "That explanation is SUS!"}'
```
Swagger UI는 http://127.0.0.1:8000/docs에서 확인할 수 있습니다.

데모 실행
API 서버를 먼저 띄운 뒤, 별도 터미널에서 실행하세요.

```bash
streamlit run slangchat/ui/app.py
```