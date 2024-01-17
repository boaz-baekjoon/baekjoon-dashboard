import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st

# 모듈 수준에서 session_state 객체 정의
if "selected_users" not in st.session_state:
    st.session_state["selected_users"] = []

# tier 숫자와 tier 이름으로 변환 함수 정의
def tier_to_num(tier):
    division = 1
    for char in tier[::-1]:
        if char.isdigit():
            division = int(char)
            break
    
    if tier.startswith("Bronze"):
        return 10.0 - 2.0 * (division - 1), "Bronze"
    elif tier.startswith("Silver"):
        return 20.0 - 2.0 * (division - 1), "Silver"
    elif tier.startswith("Gold"):
        return 30.0 - 2.0 * (division - 1), "Gold"
    elif tier.startswith("Platinum"):
        return 40.0 - 2.0 * (division - 1), "Platinum"
    elif tier.startswith("Diamond"):
        return 50.0 - 2.0 * (division - 1), "Diamond"
    elif tier.startswith("Ruby"):
        return 60.0 - 2.0 * (division - 1), "Ruby"
    elif tier == "Master":
        return 70.0, "Master"
    else:
        return 10.0, "Bronze 5"

# 미리 정의된 CSV 파일을 데이터프레임으로 읽기
csv_path = "/Users/thjeong/Desktop/BOAZ/adv/files/new_users_detail.csv"  
user_df = pd.read_csv(csv_path)

# 사용자 검색창을 사이드바에 추가
user_search = st.sidebar.text_input("### **사용자 검색**", key="user_search", help="도움말: 백준 사이트에서 사용하는 아이디를 입력하세요.")

# 사용자가 검색어를 입력한 경우
if user_search:
    exact_match = user_df['user_id'].str.lower() == user_search.lower()

    # 정확한 일치하는 사용자가 있는 경우
    if exact_match.any():
        filtered_user = user_df[exact_match]

        st.sidebar.write("검색 결과:")
        st.sidebar.write(filtered_user[['user_rank', 'user_id', 'user_tier']].to_markdown(index=False))

        st.sidebar.write("")

        # 분석 등록 버튼 추가
        if st.sidebar.button("유저 등록", key=f"register_button_{user_search}"):
            if user_search not in st.session_state["selected_users"]:
                st.session_state["selected_users"].append(user_search)

    # 정확한 일치하는 사용자가 없는 경우
    else:
        st.sidebar.write("검색 결과가 없습니다.")
        st.sidebar.write(pd.DataFrame({"user_rank": [0], "user_id": [user_search], "user_tier": ["Bronze 5"]}).to_markdown(index=False))

        # 간격 추가
        st.sidebar.write("")

        # 분석 등록 버튼 추가
        if st.sidebar.button("유저 등록", key=f"register_button_{user_search}"):
            selected_user = user_search
            if selected_user not in st.session_state["selected_users"]:
                st.session_state["selected_users"].append(selected_user)

# 제목 title 넣기
st.title('*BAEKJOON: Group-based Problem Recommendation Service*')

# 간격 띄우기
st.write("")
st.write("")
st.write("")

# 개인별 정보 소제목 추가 (왼쪽으로 정렬)
st.markdown("""
    <div style="display: block; text-align: left; margin-left: 0px;">
        <h3>Personal Status</h3>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# 등록된 유저 정보 표시
if st.session_state["selected_users"]:
    st.write("**등록된 그룹 유저 목록:**")
    selected_users = st.multiselect("", st.session_state["selected_users"])
    
    if selected_users:
        # 선택된 유저들의 티어 정보 추출
        selected_user_info = user_df[user_df['user_id'].isin(selected_users)][['user_id', 'user_tier']]

        # 평균 티어 계산
        average_tiers = [tier_to_num(tier)[0] for tier in selected_user_info['user_tier'].tolist()]
        average_tier = np.mean(average_tiers)

        # 막대 그래프 생성
        fig, ax = plt.subplots(figsize=(12, 8))

        # 선택된 각 사용자에 대한 막대 추가
        for user in selected_users:
            # 만약 데이터셋에 없는 경우 기본값으로 1.0 설정
            user_tier_value, user_tier_name = tier_to_num(selected_user_info[selected_user_info['user_id'] == user]['user_tier'].values[0]) if user in selected_user_info['user_id'].values else (1.0, "Unknown")
            ax.bar(user, user_tier_value, label=user)
            # 각 막대 위에 숫자와 tier 표시
            ax.text(user, user_tier_value + 0.1, f"{user_tier_value:.1f} ({user_tier_name})", ha='center', va='bottom')

        # 그룹 평균 막대 추가
        ax.bar("Group Average", average_tier, color='gray', label='Group Average')
        # 그룹 평균 위에 숫자와 tier 표시
        ax.text("Group Average", average_tier + 0.1, f"{average_tier:.1f} (Group Average)", ha='center', va='bottom')

        ax.set_xlabel("User")
        ax.set_ylabel("Tier")

        # y-axis 범위 및 간격 설정
        ax.set_ylim(0.0, 10.0)
        ax.set_yticks(np.arange(0.0, 10.1, 1.0))

        plt.legend()
        st.pyplot(fig)
    else:
        st.warning("해당 유저는 존재하지 않습니다.")
else:
    st.warning("해당 유저는 존재하지 않습니다.")
