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
llm = ChatBedrock( model_id = os.getenv('MODEL_ID'),
    client       = boto3.client('bedrock-runtime',region_name = os.getenv('AWS_REGION'))
    model_kwargs = {"temperature0.7"} 
)
