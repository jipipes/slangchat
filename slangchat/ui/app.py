from __future__ import annotations

import os

import httpx
import streamlit as st

API_BASE_URL = os.environ.get("SLANGCHAT_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="SlangChat", page_icon="🗣️")
st.title("SlangChat 은어 탐지 데모")

text = st.text_area("문장을 입력하세요", placeholder="이거 진짜 킹받네")

if st.button("탐지하기") and text.strip():
    try:
        response = httpx.post(f"{API_BASE_URL}/detect", json={"text": text}, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        st.error(f"API 호출 실패: {exc}")
    else:
        matches = response.json()["matches"]
        if not matches:
            st.info("탐지된 은어가 없습니다.")
        else:
            st.dataframe(
                [
                    {
                        "표현": match["surface"],
                        "뜻": match["meaning"],
                        "표준 표현": match["standard_expression"],
                        "신뢰도": match["confidence"],
                    }
                    for match in matches
                ],
                use_container_width=True,
            )