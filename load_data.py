import pandas as pd
import os
from dotenv import load_dotenv

# .env 파일 로드 및 환경 변수 불러오기
load_dotenv()
stream_ENV = os.getenv("stream_ENV")

user_df = pd.read_csv("data/user_score.csv")
problem_df = pd.read_csv("data/problem_detail.csv")