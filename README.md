# SlangChat

한국어·영어 비정형 표현을 규칙 기반 정규화, 형태소 분석, 사전 검색 및 벡터 검색으로 탐지하고 문맥에 맞는 답변을 추천하는 포트폴리오 프로젝트입니다.

## 현재 범위

- 5일 MVP
- 한국어/영어 슬랭 사전
- 스키마 및 교차 레코드 품질 검증
- 강조 접두사 정규화 및 표제어·변형 사전 탐지
- Kiwi 형태소 분석 기반 한국어 활용형 탐지
- 하이브리드 슬랭 탐지(시맨틱 검색 구현 예정)
- FastAPI와 Streamlit 데모(구현 예정)
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
