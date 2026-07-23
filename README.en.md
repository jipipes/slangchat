<p align="right"><a href="README.md">한국어</a> | English</p>

# SlangChat
 
Slangchat is a multilingual NLP system that combines rule-based normalization, morphological analysis, dictionary matching, and semantic search to detect Korean and English slang and recommend context-appropriate responeses.
 
## Current Scope
 
- Korean/English slang dictionary
- Schema and cross-record quality validation
- Emphasis prefix normalization and headword/variant dictionary detection
- Kiwi morphological analysis-based Korean inflection detection
- Hybrid slang detection (semantic search planned)
- FastAPI and Streamlit demo (planned)
- Precision/Recall/F1 and response-time evaluation (planned)
## Data Validation
 
```bash
python3 -m scripts.validate_data data/slang.json
```
 
The validator checks required fields, types, ID-language consistency, duplicate IDs, duplicate headwords, and surface-form collisions.
 
## Tests
 
```bash
python3 -m unittest discover -s tests -v
```