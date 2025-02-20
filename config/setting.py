import os
from dotenv import load_dotenv

# .env 파일 로드
env_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(env_path)

# OpenAI API Key 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API Key가 없으면 오류 발생
if OPENAI_API_KEY is None:
    raise ValueError("Error: OPENAI_API_KEY is not set. Please check your .env file.")
