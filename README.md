<p align="right"><a href="README.en.md">English</a> | 한국어</p>

# SlangChat

Slangchat은 규칙 기반 정규화, 형태소 분석, 사전 매칭 및 시맨틱 검색을 결합하여 한국어, 영어 슬랭을 탐지하고 문맥에 적합한 응답을 추천하는 다국어 자연어 처리 프로젝트입니다.

## 현재 범위

- 한국어/영어 슬랭 사전
- 스키마 및 교차 레코드 품질 검증
- 강조 접두사 정규화 및 표제어·변형 사전 탐지
- Kiwi 형태소 분석 기반 한국어 활용형 탐지
- 하이브리드 슬랭 탐지(시맨틱 검색 구현 예정)
- FastAPI 기반 `/detect` API
- Streamlit 데모(구현 예정)
- Precision/Recall/F1 및 응답시간 평가(구현 예정)

## 데이터 검증

```bash
python3 -m scripts.validate_data data/slang.json
```

검증기는 필수 필드, 타입, ID-언어 일치, 중복 ID, 중복 표제어 및 표면형 충돌을 검사합니다.

## 테스트

```bash
python3 -m unittest discover -s tests -v
```

## API 실행

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