'''
TOOL 사용, LLM 적용
'''
# 1. 모듈 가져오기
from langgraph.graph import StateGraph, END, MessagesState, START
from typing import TypedDict
from langchain_core.tools import tool            # 툴 정의할때 사용 데코레이터용
from langchain_core.messages import HumanMessage # 사용자의 메세지 형태 편하게 구성
from langchain_aws import ChatBedrock, ChatBedrockConverse # AWS bedrock llm 호출시 사용
from langgraph.prebuilt import ToolNode, tools_condition  # 툴 -> 노드로 변환, 조건부 툴 적용
from dotenv import load_dotenv
import os
import boto3

# 2. 환경변수 로드
load_dotenv()

# 3. LLM 추론용 객체 생성(전역변수)
#    모델별로 ChatBedrock or ChatBedrockConverse
llm = ChatBedrock(model  = os.getenv['MODEL_ID'],
                  client = boto3.client('bedrock-runtime',region_name=os.getenv['AWS_REGION'])
                )

# 4. 툴 준비
@tool # LLM이 알 수 있는(이해할 수 있는) 형식으로 자동 변환됨
def multiply( a:int, b:int ) -> int:
    '''두 수를 곱한 후 반환'''
    print(f'    [TOOL 실행]{a}x{b} 계산중..')
    return a*b
# 프롬프트 받고 LLM은 직접 추론할것인지? 아니면 도구를 사용하여 해결할것인지 스스로 판단하여 처리함

# 5. 여러개의 툴(여기서는 1개만 있음)을 모아서 llm에 등록
tools = [ multiply ]
llm_with_tools = llm.bind_tools(tools) # llm에게 이런 툴도 사용할 수 있다는 것을 등록(알림)

# 6. 노드 구성 ->  사전에 필요한것 -> 상태메모리 필요 -> 랭그래프가 정의한 MessageState(라이브러리에서 준비되있음)를 사용
def chatbot_node( state:MessagesState ):
    print('[chatbot_bode 호출전 상태값]',state)

    # 전달된 내용(사용자의 프롬프트)을 LLM에게 전달 -> 추론 요청 -> LLM판단 -> 직접해결 or 도구 사용 해결 -> 수행 -> 응답
    llm_with_tools.invoke( state['messages'] ) # messages 키값은 MessagesState에 정의되어 있음
    new_state = {"message":[res]} # MessagesState에 형식에 맞춰서 구성했음

    print('[chatbot_bode 호출후 상태값]',new_state)
    return new_state
