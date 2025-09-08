from flask_cors import CORS

api_key = "sk-70ea320182f9487b967d4840223adc4b"  # 请替换为你的 Deepseek API 密钥

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from flask import Flask, request, jsonify
import re

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """你是一位英语口语老师，你的任务是在一段学生与另一位口语老师的对话中，检查学生的发言，并为其给出百分制的分数。
你的检查准则是：
（1）检查语法是否有错误
（2）检查语言是否通顺
（3）检查语言是否有逻辑性
（4）检查语言是否符合英语母语者的习惯
（5）检查语言的表达力
这五个标准为依次递进的关系，第一条是最基本的要求，第五条是最高的要求。因此，其占分数的比例也是递减的。
请你根据这五个标准，为学生的发言打分。注意，你需要给出一个百分制的分数，并给出一段简短的评语。请用中文回复，你的回复模板如下：
"总评分：（0-100）分
 1.语法：（0-100）分
 （一段简短的评语）
 2.语言通顺：（0-100）分
 （一段简短的评语）
 3.逻辑性：（0-100）分
 （一段简短的评语）
 4.母语者习惯：（0-100）分
 （一段简短的评语）
 5.表达力：（0-100）分
 （一段简短的评语）
 总评语：（概况性的评价）""",
        ),
        MessagesPlaceholder(variable_name="history"),
    ]
)

llm = ChatOpenAI(
    model="deepseek-chat",       # 使用 Deepseek 模型名称
    temperature=0.7,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    api_key=api_key,
    base_url="https://api.deepseek.com",  # 显式传入 base_url
)

runnable = prompt | llm

@app.route('/judge', methods=['POST'])
def judge():
    data = request.json
    session_id = data.get('session_id')
    message_history = SQLChatMessageHistory(session_id, "sqlite:///memory.db")
    m_list = []
    cnt = 1
    for m in message_history.get_messages():
        if cnt % 2 == 1:
            m_list.append("Student:" + m.content)
        cnt += 1
    ans = runnable.invoke({"history": m_list}).content

    # 将回答解析为数组
    response_parts = re.split(r'\n\s*', ans)
    response_parts = [part.strip() for part in response_parts if part.strip()]

    return jsonify({'output': response_parts})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
