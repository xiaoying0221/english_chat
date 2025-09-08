from flask_cors import CORS

api_key = "sk-70ea320182f9487b967d4840223adc4b"  # 请替换为你的 Deepseek API 密钥
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

# 构造对话提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一位mbti人格为entp的英语口语老师，名字叫Alloy，你的任务是尽可能的理解学生所说的英语，并与其展开对话，从而提高他的口语能力。",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# 调整 llm 的调用方式，base_url 作为顶层参数传入
llm = ChatOpenAI(
    model="deepseek-chat",         # 使用 Deepseek 提供的模型名称
    temperature=0.7,               # 调整温度为 0.7
    max_tokens=1024,               # 设置最大 token 数
    timeout=None,
    max_retries=2,
    api_key=api_key,
    base_url="https://api.deepseek.com",  # 显式传入 base_url
)

runnable = prompt | llm

runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

def lets_talk(input_text, session_id):
    answer = runnable_with_history.invoke(
        {"input": input_text},
        config={"configurable": {"session_id": session_id}},
    )
    print(answer.content)
    return answer.content

@app.route('/chat', methods=['POST'])
def api_chat():
    data = request.json
    input_text = data.get('input')
    session_id = data.get('session_id')
    ans = lets_talk(input_text, session_id)
    return jsonify({'output': ans})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
