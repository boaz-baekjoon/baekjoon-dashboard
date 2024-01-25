from utils.mapping import *
from load_data import *

def create_dataframe(api_response, tier):
    categories = ["implementation", "ds", "dp", "graph", "search", "string", "math", "opt", "geo", "adv"]
    data = []

    for category, problems in api_response.items():
        category_name = categories[int(category)]

        for problem_id in problems:
            problem_info = problem_df[problem_df['problem_id'] == problem_id]

            if not problem_info.empty:
                problem_title = problem_info['problem_title'].iloc[0]
                tier_text = tier_num_to_text(int(problem_info['problem_level'].iloc[0]))
                problem_url = f"https://www.acmicpc.net/problem/{problem_id}"
                data.append({
                    "문제 등급": tier_text,
                    "문제 유형": category_name,
                    "문제 번호": problem_id,
                    "문제 제목": problem_title,
                    "문제 URL": problem_url
                })

    return pd.DataFrame(data)
