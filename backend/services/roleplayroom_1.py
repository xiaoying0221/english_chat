from flask_cors import CORS

api_key = "sk-70ea320182f9487b967d4840223adc4b"  # 请替换为你的 Deepseek API 密钥

from typing import Callable, List

from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求
agents_num = 3

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///room_memory.db")

class Player:
    def __init__(self, name: str) -> None:
        self.name = name

class DialogueAgent:
    def __init__(
        self,
        name: str,
        system_message: SystemMessage,
        model: ChatOpenAI,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        """
        调用聊天模型生成消息
        """
        message = self.model.invoke(
            [
                self.system_message,
                HumanMessage(content="\n".join(self.message_history + [self.prefix])),
            ]
        )
        return message.content

    def receive(self, name: str, message: str) -> None:
        """
        将 {name} 的发言 {message} 添加到消息记录中
        """
        self.message_history.append(f"{name}: {message}")

class DialogueSimulator:
    def __init__(
        self,
        agents: List[DialogueAgent],
        selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        用 {name} 的 {message} 发起对话
        """
        for agent in self.agents:
            agent.receive(name, message)
        self._step += 1

    def step(self, inputing) -> tuple[str, str]:
        # 1. 选择下一位发言者
        speaker_idx = self.select_next_speaker(self._step, self.agents)

        # 2. 发言
        if speaker_idx == 0:
            message = inputing
            speaker = Player("Player")
        else:
            speaker = self.agents[speaker_idx-1]
            message = speaker.send()

        # 3. 所有人接收消息
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        self._step += 1

        return speaker.name, message

character_names = ["William Shakespeare", "Albert Einstein", "Marie Curie"]
background = """玩家受邀参加一场被称为“**科学与艺术的跨时代对话**”的虚拟国际学术会议。这场会议的背景设定为一个未来的虚拟平台，专门用来汇聚历史上最伟大的科学家、艺术家和作家进行跨领域的讨论和思想碰撞。大会的主题是“**人类文明的发展：科学与艺术的相互作用**”。
在这场群聊中，三位英语口语老师将分别扮演莎士比亚（代表文学与艺术）、爱因斯坦（代表科学与物理）、玛丽·居里（代表科学与医学）并被邀请作为嘉宾，就科学、艺术和社会进步的话题进行对话。玩家作为一名年轻的科学或文学研究生，既可以观察三位历史巨人之间的讨论，也可以引导话题，让他们对自己感兴趣的问题发表见解。请注意，这三位历史人物都是由口语老师扮演，最终的目标是提高学生的英语口语能力
在每一轮发言中，你需要的是表达你的观点与见解，要注意你在进行一场讨论会，而并非是与单独某个人的对话。你可以在发言中加入指向性的语言，但务必保持对话的连贯"""
word_limit = 50  # 任务脑图的字数限制

# 系统消息
character_system_messages = [
    SystemMessage(content="你扮演莎士比亚，英国文艺复兴时期著名剧作家和诗人，被誉为“人类灵魂的工程师”，创作了无数经典的戏剧作品。"),
    SystemMessage(content="你扮演爱因斯坦，德国出生的著名物理学家，以提出相对论著称，是20世纪最重要的科学家之一。"),
    SystemMessage(content="你扮演玛丽·居里，法国-波兰籍的著名物理学家和化学家，因发现镭和钋而获得两次诺贝尔奖，是世界上第一位女性诺贝尔奖得主。"),
]

characters = []
for character_name, character_system_message in zip(
    character_names, character_system_messages
):
    characters.append(
        DialogueAgent(
            name=character_name,
            system_message=character_system_message,
            model=ChatOpenAI(
                temperature=0.7,
                max_tokens=1024,
                api_key=api_key,
                base_url="https://api.deepseek.com",  # 显式传入 base_url
                model="deepseek-chat"  # 使用 Deepseek 模型名称
            ),
        )
    )

def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
    return step % (len(agents) + 1)

simulator = DialogueSimulator(
    agents=characters, selection_function=select_next_speaker
)
simulator.reset()

def lets_talk(inputing):
    answer_list = []
    i = 0
    while i <= agents_num:
        name, message = simulator.step(inputing)
        if i != 0:
            answer_list.append(name + ' : ' + message)
        i += 1
    return answer_list

@app.route('/new', methods=['GET'])
def api_new():
    simulator.reset()
    return jsonify({'message': 'New conversation started'})

@app.route('/chat', methods=['POST'])
def api_chat():
    data = request.json
    inputing = data.get('input')
    ans = lets_talk(inputing)
    print(ans)
    return jsonify({'output': ans})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080)
