import requests
import os
import streamlit as st

def recommend_problems(user_id_list, tier, category_num):
    payload = {
        "user_id_list": user_id_list,
        "tier": tier,
        "category_num": category_num
    }

    response = requests.post(os.environ["GROUP_REC_API"], json=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"API 호출 중 오류 발생: {response.status_code}")
        return None
