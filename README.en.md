<p align="right"><a href="README.md">한국어</a> | English</p>

# SlangChat

SlangChat is a multilingual NLP project that combines rule-based normalization, morphological analysis, dictionary matching, and semantic search to detect Korean and English slang and recommend contextually appropriate responses.

## Current Scope

- Korean/English slang dictionary
- Data collected via a batch-search + LLM-draft + human-verification pipeline (cross-source check, blind meaning test)
- Schema and cross-record quality validation
- Emphasis-prefix normalization and canonical/variant dictionary detection
- Korean inflection detection based on Kiwi morphological analysis
- Hybrid slang detection (semantic search planned)
- FastAPI-based `/detect` API
- Streamlit demo
- Precision/Recall/F1 and latency evaluation

## Data Validation

```bash
python3 -m scripts.validate_data data/slang.json
```
The validator checks required fields, types, ID-language consistency, duplicate IDs, duplicate terms, and surface-form collisions.

Tests
```bash
python3 -m unittest discover -s tests -v
```

Evaluation
```bash
python3 -m scripts.evaluate
```
Uses each dictionary entry's example sentence as ground truth to measure detection accuracy (Precision/Recall/F1) and average response latency.

Running the API
```bash
uvicorn slangchat.api.app:app --reload
```
Send text to POST /detect to get back a list of detected slang matches.

```bash
curl -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "That explanation is SUS!"}'
```
Swagger UI is available at http://127.0.0.1:8000/docs.

Running the Demo
Start the API server first, then in a separate terminal:

```bash
streamlit run slangchat/ui/app.py
```