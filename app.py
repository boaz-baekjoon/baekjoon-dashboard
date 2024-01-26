import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import RegularPolygon
import json
import matplotlib.gridspec as gridspec 

from load_data import *
from utils.mapping import *
from utils.request import *
from utils.make_df import *

# 모듈 수준에서 session_state 객체 정의
if "selected_users" not in st.session_state:
    st.session_state["selected_users"] = []

side_help_text = """
How to use❓
1. 왼쪽 사이드바의 **사용자 검색**에 백준 아이디를 입력하고 **Enter**를 눌러 검색 후, 사용자 정보를 확인하세요.
2. 그룹에 등록하고 경우, **사용자 등록** 버튼을 클릭하여 그룹 목록에 사용자 아이디를 추가하세요.
3. 그룹에서 특정 사용자를 제외하고 싶을 때, **등록된 사용자 목록**에서 해당 사용자 아이디를 **두 번** 클릭하세요.
"""

# 사용자 검색창을 사이드바에 추가
user_search = st.sidebar.text_input("### **사용자 검색**", key="user_search", help=side_help_text)

# 사용자가 검색어를 입력한 경우
if user_search:
    exact_match = user_df['user_id'].str.lower() == user_search.lower()

    # 정확히 일치하는 사용자가 있는 경우
    if exact_match.any():
        filtered_user = user_df[exact_match]

        st.sidebar.write("검색 결과:")
        st.sidebar.write(filtered_user[['user_id', 'user_tier']].to_markdown(index=False))

        st.sidebar.write("")

        # 사용자가 있을 때 사용자 등록 버튼 추가
        if st.sidebar.button("사용자 등록", key=f"register_button_{user_search}"):
            if user_search not in st.session_state["selected_users"]:
                    st.session_state["selected_users"].append(user_search)

    # 정확히 일치하는 사용자가 없는 경우
    else:
        st.sidebar.write("검색 결과가 없습니다.")
        st.sidebar.write(pd.DataFrame({"user_id": [user_search], "user_tier": ["❓"]}).to_markdown(index=False))

        st.sidebar.write("")

        # 사용자가 없을 때 사용자 등록 버튼 추가
        if st.sidebar.button("사용자 등록", key=f"register_button_{user_search}"):
            selected_user = user_search
            if selected_user not in st.session_state["selected_users"]:
                st.session_state["selected_users"].append(selected_user)

st.header('*BAEKJOON: Group-based Problem Recommendation Service*', divider='rainbow')

# Tips 추가
st.write("### **💡 Tips**")
st.markdown("""
- 백준 그룹 문제 추천 서비스 대시보드는 **실제 백준 사이트**([Baekjoon 링크](https://www.acmicpc.net/))의 정보를 참조하여 기능합니다.
- 백준 등급은 기본적으로 **Bronze**부터 **Master**등급까지 구성되어 있습니다.
- **Master** 등급을 제외한 각 등급마다 **5**개의 구간으로 나누어집니다. (예: Silver 1 ~ Silver 5)
- **등급 기준 수치** **6**: Silver 5 / **11**: Gold 5 / **16**: Platinum 5 / **21**: Diamond 5 / **26**: Ruby 1 / **31**: Master
- **사용자 검색**에서 아이디의 등급이 **Silver 5 미만**이거나 존재하지 않을 경우, **❓**로 나타납니다.
- 백준 그룹 문제 추천 서비스는 추천의 정확도를 위해 **Silver 5**이상 등급부터 사용 가능합니다.
- **Silver 5** 미만 사용자의 경우 개인 시각화가 제한되며, 문제 유형별 그룹 평균 레이팅에 영향을 주지 않습니다.
- 그래프는 사용자의 **현재 문제 유형별 레이팅 점수**와 그룹의 **평균 레이팅 점수**를 나타냅니다.
""")
st.markdown("<div style='text-align: left; margin-left: 30px;'> ⭐ <span style='color:blue'>파란색: 개인 레이팅</span> / <span style='color:red'>빨간색: 현재 그룹 평균 레이팅</span> / <span style='color:green'>초록색: 조절된 그룹 평균 레이팅</span></div>", unsafe_allow_html=True)

st.write("")
st.write("")

check_tier_help_text = """
1. **Check Baekjoon Tier** 메뉴 아래에 **그룹 목록**에서 조회할 사용자를 선택합니다.
2. 조회할 사용자를 선택하면(1), 그룹의 백준 **평균 등급**이 아래에 **빨간색 텍스트**로 표시됩니다.
3. 조회할 사용자를 선택하면(2), **문제 유형별** 개인 레이팅 및 그룹 평균 레이팅을 시각화합니다.
4. **그룹 평균 등급 조절** 슬라이더를 사용하여, 평균 등급을 조절할 수 있습니다.
5. **조정된 평균 등급**은 특정 등급의 문제 유형별 평균 레이팅을 나타내며, **초록색 텍스트**로 표시됩니다.
6. 슬라이더로 **조정된 평균 등급**에 맞춰 해당 등급 유저들의 **카테고리별 평균 레이팅**을 시각화합니다.
7. **Tips**에 설명된 그래프 색을 참조하여, **개인/그룹 평균/특정 등급 평균**에 대한 결과를 확인합니다.
"""

# Check Baekjoon Tier 메뉴 추가
st.markdown("""
    <div style="display: block; text-align: left; margin-left: 0px;">
        <h3>✔️ Check Baekjoon Tier</h3>
    </div>
""", unsafe_allow_html=True)

with st.expander("**How to use❓**", expanded=False):
    st.markdown(check_tier_help_text, unsafe_allow_html=True)

st.sidebar.write("")
st.sidebar.write("")

# 등록된 사용자 정보 표시, 선택된 사용자들의 등급 정보 추출
if st.session_state["selected_users"]:
    unique_selected_users = list(set(st.session_state["selected_users"]))

    selected_users = st.multiselect("", unique_selected_users)

    # 등록된 사용자 리스트 표시
    st.sidebar.write("### **등록된 사용자 목록** 💻")
    st.sidebar.write("사용자 아이디 두 번 클릭 시 그룹에서 **제외**")

    for user in st.session_state["selected_users"]:
        delete_button_clicked = st.sidebar.button(f"{user}", key=f"delete_button_{user}")
        if delete_button_clicked:
            st.session_state["selected_users"].remove(user)
            break  

    if selected_users:
        selected_user_info = user_df[user_df['user_id'].isin(selected_users)][['user_id', 'user_tier', 'implementation', 'ds', 'dp', 'graph', 'search', 'string', 'math', 'opt', 'geo', 'adv']]
        
        # 그룹 평균 등급 계산
        all_users = selected_users + list(selected_user_info[selected_user_info['user_id'].isin(selected_users) == False]['user_id'])
        average_tiers = [tier_to_num(tier) for tier in selected_user_info['user_tier'].tolist()]
        average_tier = np.mean(average_tiers)

        # 평균 티어를 텍스트로 변환
        average_tier_text = tier_avg_to_text(average_tier)

        # 선택된 각 사용자에 대해 만약 데이터셋에 없는 경우 반영하지 않고 건너뛰기
        for user in selected_users:
            user_info = selected_user_info[selected_user_info['user_id'] == user]
            if user_info.empty:
                continue  

            # 사용자 정보가 있으면 처리
            user_tier = tier_to_num(user_info['user_tier'].values[0])

        st.write("")

        # 텍스트로 변환된 그룹 평균 등급 표시(빨강)
        st.write(f"<div style='text-align: center; font-size: xx-large;'><strong> ➡️ 현재 그룹의 백준 평균 등급은 <span style='color: red;'>{average_tier_text}</span>입니다.</strong></div>", unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.write("")

        # 그룹 평균 등급값을 slider로 조정
        group_average_slider = st.slider("**그룹 평균 등급 조절**", min_value=1.0, max_value=35.0, value=average_tier, step=0.5)

        st.write("")

        # 텍스트로 변환된 등급 표시
        adjusted_average_tier_text = tier_avg_to_text(group_average_slider)

        # 조절된 그룹 평균 등급 표시
        st.write(f"<div style='text-align: center; font-size: xx-large;'><strong> ➡️ 조정된 백준 평균 등급은 <span style='color: green;'>{adjusted_average_tier_text}</span>입니다.</strong></div>", unsafe_allow_html=True)
        st.write("")

        # 조절된 그룹 레이팅 평균값을 텍스트로 변환
        group_average_text = tier_avg_to_text(group_average_slider)

        st.write("")
        st.write("")

        # 사용자에 대한 레이더 차트 그리기
        if selected_users:
            st.write("### 🏆 **Individual Ratings by Category**")

            st.write("")
            st.write("")

            # 사용자에 대한 레이더 차트 그리기 
            fig = plt.figure(figsize=(12, 12))
            gs = gridspec.GridSpec(3, 3, figure=fig)

            current_position = 0  
            num_selected_users = len(selected_users)

            for user in selected_users:
                user_info = selected_user_info[selected_user_info['user_id'] == user]

                # 사용자 정보가 비어있거나 또는 해당 사용자의 categories 값이 비어있으면 차트를 그리지 않음
                if user_info.empty:
                    continue

                # categories와 values 설정
                categories = ['implementation', 'ds', 'dp', 'graph', 'search', 'string', 'math', 'opt', 'geo', 'adv']
                values = (user_info[categories].values.flatten() + 20.0).tolist()
                values = [min(val, 100) for val in values]
                values += [values[0]]

                # 각 카테고리의 수 만큼 각도 설정
                angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
                angles += angles[:1]

                # 레이더 차트를 그릴 subplot 위치 계산
                row = current_position // 3
                col = current_position % 3
                ax = fig.add_subplot(gs[row, col], polar=True)

                # 개인 레이팅에 대한 레이더 차트 그리기(파랑)
                ax.plot(angles, values, 'o-', linewidth=2, color='blue', alpha=0.75)

                # 그룹 평균 레이팅에 대한 레이더 차트 그리기(빨강)
                average_values = (np.mean(selected_user_info[categories].values, axis=0) + 20.0).tolist()
                average_values = [min(val, 100) for val in average_values]
                average_values += [average_values[0]]  
                ax.plot(angles, average_values, 'o-', linewidth=2, color='red', alpha=0.7)

                # 슬라이더로 조절된 평균 등급의 평균 레이팅에 대한 레이더 차트 그리기(초록)
                if group_average_slider != average_tier:
                    adjusted_average_values = (user_df[user_df['user_tier'] == group_average_text][categories].mean().values + 20.0).tolist()
                    adjusted_average_values = [min(val, 100) for val in adjusted_average_values]
                    adjusted_average_values += [adjusted_average_values[0]]
                    ax.plot(angles, adjusted_average_values, 'o-', linewidth=2, color='green', alpha=0.75)

                ax.set_thetagrids(np.array(angles[:-1]) * 180 / np.pi, categories)
                ax.set_title(f"{user}", fontsize=15, fontweight='bold')
                ax.set_ylim(0, 100)

                # 다음 위치로 이동
                current_position += 1

            # 레이아웃 조정
            plt.tight_layout(rect=[0, 0, 1, 0.96])

            # Streamlit에서 그림 표시
            st.pyplot(fig)

st.write("")

group_rec_help_text = """
1. 사용자 ID를 아래 사용자 목록에서 선택합니다. 
2. 백준 사용자가 아닌 ID를 입력하는 경우, 문제 추천 시 해당 사용자 정보를 **제외**하고 계산됩니다.
3. 그룹에서 추천 받고 싶은 문제의 **등급**을 선택해주세요. 
4. **유형**별로 추천 받고 싶은 문제의 개수를 **각각** 입력해주세요.(쉼표로 구분)
5. **문제 추천** 버튼을 누르면, 추천 받은 문제 등급/문제 유형/문제 번호/문제 제목/문제 URL을 제공합니다.
"""

# Problem Recommendation 메뉴 추가
st.markdown("""
    <div style="display: block; text-align: left; margin-left: 0px;">
        <h3> 🤔 Problem Recommendation </h3>
    </div>
""", unsafe_allow_html=True)

with st.expander("**How to use❓**", expanded=False):
    st.markdown(group_rec_help_text, unsafe_allow_html=True)

st.write("")

def main():
    if "selected_users" in st.session_state and st.session_state["selected_users"]:
        user_id_list = st.multiselect("**사용자 아이디를 선택하세요**", st.session_state["selected_users"], key="user_ids")

    tier_mapping = {
        "Bronze 5": 1,
        "Bronze 4": 2,
        "Bronze 3": 3,
        "Bronze 2": 4,
        "Bronze 1": 5,
        "Silver 5": 6,
        "Silver 4": 7,
        "Silver 3": 8,
        "Silver 2": 9,
        "Silver 1": 10,
        "Gold 5": 11,
        "Gold 4": 12,
        "Gold 3": 13,
        "Gold 2": 14,
        "Gold 1": 15,
        "Platinum 5": 16,
        "Platinum 4": 17,
        "Platinum 3": 18,
        "Platinum 2": 19,
        "Platinum 1": 20,
        "Diamond 5": 21,
        "Diamond 4": 22,
        "Diamond 3": 23,
        "Diamond 2": 24,
        "Diamond 1": 25,
        "Ruby 5": 26,
        "Ruby 4": 27,
        "Ruby 3": 28,
        "Ruby 2": 29,
        "Ruby 1": 30,
        "Master": 31
    }
    # Tier 입력 받기
    tier = st.selectbox("**등급을 선택하세요**", list(tier_mapping.keys()))
    tier = tier_mapping[tier]

    # 카테고리 이름 리스트
    categories = ["implementation", "ds", "dp", "graph", "search", "string", "math", "opt", "geo", "adv"]

    # 카테고리별 문제 개수 입력 받기
    category_num = []

    # 처음 5개 유형에 대한 문제 개수 입력
    first_row_input = st.text_input("**implementation, ds, dp, graph, search에 대해 추천받을 문제 개수를 각각 입력하세요.(쉼표로 구분)**")
    first_row_values = [int(num.strip()) for num in first_row_input.split(',') if num.strip().isdigit()]

    # 나머지 5개 유형에 대한 문제 개수 입력
    second_row_input = st.text_input("**string, math, opt, geo, adv에 대해 추천받을 문제 개수를 각각 입력하세요.(쉼표로 구분)**")
    second_row_values = [int(num.strip()) for num in second_row_input.split(',') if num.strip().isdigit()]

    # 입력된 값들을 category_num 리스트에 추가
    category_num.extend(first_row_values[:5]) 
    category_num.extend(second_row_values[:5])

    # 문제 추천 버튼
    if st.button("문제 추천"):
        api_response = recommend_problems(user_id_list, tier, category_num)

        # 결과 처리 및 표시
        if api_response:
            df = create_dataframe(api_response, tier)

            def make_clickable(url):
                return f'<a target="_blank" href="{url}">{url}</a>'

            if '문제 URL' in df.columns:
                df['문제 URL'] = df['문제 URL'].apply(make_clickable)

            html = df.to_html(index=False, escape=False, justify = "center")
            st.markdown(html, unsafe_allow_html=True)

        else:
            st.error("문제 추천에 실패했습니다.")

if __name__ == "__main__":
    main() 