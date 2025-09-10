# English_chat

## 项目简介
本平台融合 DeepSeek-V2 大模型，面向英语口语学习场景，支持多角色 AI 对话、群聊场景模拟与语音评分等核心能力，可从发音、语法、流利度与用词等维度帮助学习者系统提升口语水平。系统采用前后端分离架构（前端基于 Vue；后端提供 API 服务），集成语音识别（ASR）与语音合成（TTS）技术，适用于成人与青少年英语口语学习场景。

## 主要功能
- 多角色 AI 对话：支持与不同身份设定的 AI 进行情景交流
- 群聊模拟：模拟多人会话，提升真实沟通环境下的表达能力
- 语音评分：从发音、语法、流利度、多样性等维度给出反馈
- 语音识别 ASR：实时将语音转文字，便于纠错与回放
- 语音合成 TTS：将文本转为自然语音，支持多音色与语速调节
- 学习记录与报告：追踪练习历史，生成个性化建议（可扩展）

## 技术栈
- 前端：Vue（基于 Vue CLI 项目结构）
- 后端：RESTful API 服务（本仓库 `backend/` 目录为 Python 实现示例）
- 大模型：DeepSeek-V2（对话与评估）
- 语音能力：ASR（识别）、TTS（合成）

## 目录结构
```
English_chat/
  ├─ frontend/   # 前端应用（Vue）
  └─ backend/    # 后端服务（Python 示例）
```

## 后端启动（示例）
```
cd backend
pip install -r requirements.txt
python run.py
```

## 项目安装
```
npm install
```

### 开发环境启动（热重载）
```
npm run serve
```

### 生产环境构建（打包）
```
npm run build
```

### 自定义配置
参见 [Vue CLI 配置参考](https://cli.vuejs.org/config/)。
