# 1. 모듈 가져오기
import boto3
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import dotenv
import os

dotenv.load_dotenv()

# LLM 생성, 차후 에이전트별로 역할에 따라 최적의 LLM 배치할 수 있음
llm = ChatBedrock(model_id = os.getenv('MODEL_ID'),
    client       = boto3.client('bedrock-runtime',region_name = os.getenv('AWS_REGION')),
    model_kwargs = {"temperature":0.7} 
)

# Agent 1, 신입 개발자를 위한 프롬프트 구성
developer_prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 열정적인 "신입 파이썬 개발자"입니다. 요청받은 기능을 구현하는 코드를 작성하세요. 설명은 최소화하고 코드 위주로 작성하세요.'),
    ('user'  , '{request}'),
])

# Agent 2, 전문 리뷰어를 위한 프롬프트 구성
reviewer_prompt = ChatPromptTemplate.from_messages([
    ('system', '''당신은 까다로운 "전문 개발자"입니다. 신입 개발자가 작성한 코드를 리뷰하세요.
보안 취약점, 비효율적인 부분, 스타일 가이드를 점검하고 수정 제안을 하세요.
코드가 완벽하다면, "PASS"라고만 답하세요.
'''),
    ('user'  , ''),
])

# Agent 3, (코드 리뷰를 기반으로 코드를 수정하는) 리파인더를 위한 프롬프트 구성
reviewer_prompt = ChatPromptTemplate.from_messages([
    ('system', ''),
    ('user'  , ''),
])