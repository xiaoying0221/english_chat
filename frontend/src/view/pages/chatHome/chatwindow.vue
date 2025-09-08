<template>
    <div class="chat-window">
      <!-- 聊天窗口顶部区域，包含好友头像、名称以及一些功能按钮 -->
      <div class="top">
        <div class="head-pic">
          <!-- 显示好友头像，使用 HeadPortrait 组件 -->
          <HeadPortrait :imgUrl="frinedInfo.headImg"></HeadPortrait>
        </div>
        <div class="info-detail">
          <!-- 显示好友名称和详细信息 -->
          <div class="name">{{ frinedInfo.name }}</div>
          <div class="detail">{{ frinedInfo.detail }}</div>
        </div>
        <!-- 顶部右侧的其他功能按钮，视频、电话、文件和图片上传 -->
        <div class="other-fun">
          <span class="iconfont icon-shipin" @click="video"> </span> <!-- 视频按钮 -->
          <span class="iconfont icon-gf-telephone" @click="telephone"></span> <!-- 电话按钮 -->
          <!-- 上传文件 -->
          <label for="docFile">
            <span class="iconfont icon-wenjian"></span>
          </label>
          <!-- 上传图片 -->
          <label for="imgFile">
            <span class="iconfont icon-tupian"></span>
          </label>
          <!-- 图片上传控件 -->
          <input
            type="file"
            id="imgFile"
            @change="sendImg"
            accept="image/*"
          />
          <!-- 文件上传控件 -->
          <input
            type="file"
            id="docFile"
            @change="sendFile"
            accept="application/*,text/*"
          />
        </div>
      </div>
  
      <!-- 聊天窗口内容和输入框部分 -->
      <div class="botoom">
        <!-- 聊天记录展示区 -->
        <div class="chat-content" ref="chatContent">
          <div class="chat-wrapper" v-for="item in chatList" :key="item.id">
            <!-- 显示对方的消息 -->
            <div class="chat-friend" v-if="item.uid !== '1001'">
              <div class="chat-text" v-if="item.chatType == 0">
                {{ item.msg }} <!-- 文本消息 -->
                <div class="Trans" v-if ="item.showTranslation">
                {{ item.translateText }}
                </div>
                <div class="message-options">
                  <button class="translate-btn" @click="changeText(item)">
                    <img src="https://pic.imgdb.cn/item/66f94026f21886ccc0b559d3.png" alt="Translate" />
                  </button>
                  <button class="speak-btn" @click="main(item.msg)">
                    <img src="https://pic.imgdb.cn/item/66f8ff21f21886ccc066daec.png" alt="play" />
                  </button>
  
                </div>
              </div>
              <!-- 图片消息 -->
              <div class="chat-img" v-if="item.chatType == 1">
                <img
                  :src="item.msg"
                  alt="表情"
                  v-if="item.extend.imgType == 1"
                  style="width: 100px; height: 100px"
                />
                <el-image :src="item.msg" :preview-src-list="srcImgList" v-else>
                </el-image>
              </div>
              <!-- 文件消息 -->
              <div class="chat-img" v-if="item.chatType == 2">
                <div class="word-file">
                  <FileCard
                    :fileType="item.extend.fileType"
                    :file="item.msg"
                  ></FileCard>
                </div>
              </div>
              <!-- 语音消息 -->
              <div class="chat-voice" v-if="item.chatType == 3">
                <audio :src="item.msg" controls></audio>
                <div class="message-options">
                  <button class="translate-btn" @click="translateText(item.msg)">
                    <img src="https://pic.imgdb.cn/item/670b6e4cd29ded1a8cc5469e.png" alt="Translate" />
                  </button>
                  <button class="speak-btn" @click="main(item.msg)">
                    <img src="https://pic.imgdb.cn/item/670b6ed0d29ded1a8cc5b6e8.png" alt="play" />
                  </button>
                </div>
              </div>
              <div class="chat-text" v-if="item.chatType == 10">
                <div v-for="(item, index) in item.msg" :key="index" class="response-section">
                  <h3>{{ getTitle(item) }}</h3>
                  <p>{{ getContent(item) }}</p>
                </div>
                <div class="message-options">
                  <button class="speak-btn" @click="main(item.msg)">
                    <img src="https://pic.imgdb.cn/item/66f8ff21f21886ccc066daec.png" alt="play" />
                  </button>
  
                </div>
              </div>
              <!-- 显示发送者头像、名称、时间 -->
              <div class="info-time">
                <img :src="item.headImg" alt="" />
                <span>{{ item.name }}</span>
                <span>{{ item.time }}</span>
              </div>
            </div>
  
            <!-- 显示自己发送的消息 -->
            <div class="chat-me" v-else>
              <div class="chat-text" v-if="item.chatType == 0">
                {{ item.msg }} <!-- 文本消息 -->
                <div class="Trans" v-if ="item.showTranslation">
                {{ item.translateText }}
                </div>
                <div class="message-options">
                  <button class="translate-btn" @click="changeText(item)">
                    <img src="https://pic.imgdb.cn/item/66f94026f21886ccc0b559d3.png" alt="Translate" />
                  </button>
                  <button class="speak-btn" @click="main(item.msg)">
                    <img src="https://pic.imgdb.cn/item/66f8ff21f21886ccc066daec.png" alt="play" />
                  </button>
                </div>
              </div>
              <!-- 图片消息 -->
              <div class="chat-img" v-if="item.chatType == 1">
                <img
                  :src="item.msg"
                  alt="表情"
                  v-if="item.extend.imgType == 1"
                  style="width: 100px; height: 100px"
                />
                <el-image
                  style="max-width: 300px; border-radius: 10px"
                  :src="item.msg"
                  :preview-src-list="srcImgList"
                  v-else
                >
                </el-image>
                <div class="chat-transition" v-if ="item.showTranslation">
                {{ item.picText }}
                </div>
                <div class="message-options">
                  <button class="translate-btn" @click="changeText(item)">
                    <img src="https://pic.imgdb.cn/item/670b6e4cd29ded1a8cc5469e.png" alt="Translate" />
                  </button>
                  <button class="speak-btn" @click="SpeechAnlyise(item)">
                    <img src="https://pic.imgdb.cn/item/670b6ed0d29ded1a8cc5b6e8.png" alt="play" />
                  </button>
                </div>
              </div>
              <!-- 文件消息 -->
              <div class="chat-img" v-if="item.chatType == 2">
                <div class="word-file">
                  <FileCard
                    :fileType="item.extend.fileType"
                    :file="item.msg"
                  ></FileCard>
                </div>
              </div>
              <!-- 语音消息 -->
              <div class="chat-voice" v-if="item.chatType == 3">
                <audio :src="item.msg" controls></audio>
                <div class="chat-transition" v-if ="item.showTranslation">
                {{ item.translateText }}
                </div>
                <FloatingWindow
                :visible="item.isWindowVisible"
                :evaluation="item.evaluation"
                :overall="item.overall"
                :speed="item.speed"
                :accuracy="item.accuracy"
                :fluency="item.fluency"
                :integrity="item.integrity"
                ></FloatingWindow>
                <div class="message-options">
                  <button class="translate-btn" @click="changeText(item)">
                    <img src="https://pic.imgdb.cn/item/670b6e4cd29ded1a8cc5469e.png" alt="Translate" />
                  </button>
                  <button class="speak-btn" @click="SpeechAnlyise(item)">
                    <img src="https://pic.imgdb.cn/item/670b6ed0d29ded1a8cc5b6e8.png" alt="play" />
                  </button>
                </div>
              </div>
              <!-- 批改消息 -->
              <div class="chat-text" v-if="item.chatType == 9">
                <Try :result="item.msg"></Try>
                <CorrectT :result="item.msg"
                v-show="item.showTotal"
                ></CorrectT>
                <div class="message-options">
                  <button class="translate-btn" @click="showT(item)">
                    <img src="https://pic.imgdb.cn/item/670b6ed0d29ded1a8cc5b6e8.png" alt="Translate" />
                  </button>
                </div>
              </div>
              <!-- 显示自己头像、名称、时间 -->
              <div class="info-time">
                <span>{{ item.name }}</span>
                <span>{{ item.time }}</span>
                <img :src="item.headImg" alt="" />
              </div>
            </div>
          </div>
        </div>
  
        <!-- 输入框和功能区 -->
        <div class="chatInputs">
          <!-- 作文批改模式 -->
          <div class="emoji boxinput" @click="clickWriting">
            <img src="https://pic.imgdb.cn/item/670f6445d29ded1a8cf695cc.png" alt="" />
          </div>
          <!-- 录音按钮，按住时开始录音 -->
          <div class="emoji boxinput" @mousedown="startRecording" 
            @mouseup="stopRecording" @touchstart="startRecording" @touchend="stopRecording">
            <img src="@/assets/img/head_yuyin.png" alt="" />
          </div>
          <!-- 显示录音状态 -->
          <p v-if="isRecording">正在录音...</p>
          <!-- 表情选择按钮 -->
          <div class="emoji boxinput" @click="clickEmoji">
            <img src="@/assets/img/emoji/smiling-face.png" alt="" />
          </div>
          <!-- 表情选择内容 -->
          <div class="emoji-content">
            <Emoji
              v-show="showEmoji"
              @sendEmoji="sendEmoji"
              @closeEmoji="clickEmoji"
            ></Emoji>
          </div>
          <div class="emoji-content">
            <Writing
              v-show="showWriting"
              @updateSelections="updateSet"
              @closeEmoji="clickWriting"
            ></Writing>
          </div>
          <!-- 文本输入框 -->
          <input class="inputs" v-model="inputMsg" @keyup.enter="sendText" />
          <!-- 发送按钮 -->
          <div class="send boxinput" @click="sendText">
            <img src="@/assets/img/emoji/rocket.png" alt="" />
          </div>
          <div class="send boxinput" @click="FinalAnlyise">
            <img src="https://pic.imgdb.cn/item/670bda7ed29ded1a8c2869e6.png" alt="" />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { animation } from "@/util/util"; // 导入滚动动画工具
  import { getChatMsg } from "@/api/getData"; // 导入获取聊天记录的 API
  import HeadPortrait from "@/components/HeadPortrait"; // 导入头像组件
  import Emoji from "@/components/Emoji.vue"; // 导入表情组件
  import FileCard from "@/components/FileCard.vue"; // 导入文件卡片组件
  import FloatingWindow from "@/components/FloatingWindow.vue"
  import Writing from "@/components/Writing.vue"
  import CorrectT from "@/components/CorrectT.vue"
  import Try from "@/components/try.vue"
  import axios from 'axios'; // 导入 axios 用于发送 HTTP 请求
  import OpenAI from "openai";
  import CryptoJS from 'crypto-js';
  import Recorder from 'recorder-core';
  import 'recorder-core/src/engine/wav'
  

  // 设置 API 请求的基础 URL
  const api = axios.create({
    baseURL: 'http://localhost:5000',
  });
  
  // 有道 API 的 axios 实例
  const youdaoApi = axios.create({
    baseURL: 'https://openapi.youdao.com', // 有道翻译 API 地址
  });
  
  export default {
    components: {
      HeadPortrait, // 头像组件
      Emoji, // 表情组件
      FileCard, // 文件卡片组件
      FloatingWindow,
      Writing,
      CorrectT,
      Try,
    },
    props: {
      frinedInfo: Object, // 从父组件传递的好友信息
      default() {
        return {};
      },
    },
    data() {
      return {
        chatList: [], // 聊天记录
        inputMsg: "", // 输入框中的消息
        showEmoji: false, // 是否显示表情选择器
        showWriting: false,
        srcImgList: [], // 图片列表
        isRecording: false, // 录音状态
        voiceMessage: null, // 语音消息对象
        recordingTime: 0, // 录音时间
        map3buffer: null, //
        appKey: '08159463405d57c9',
        key: '6NyH1FXHpa5InNG0bf6AM1pI4kDoIMV8', // 注意：暴露appSecret，有被盗用造成损失的风险
        from: 'en',
        to: 'zh-CHS',
        vocabId: '您的用户词表ID',
        recorder: null,
        rec: null,
        audioContext: null,
        XFappId:'509ff552',
        XFapiKey:'72f9381bcd1ec1d216fb3383a6ef5cf6',
        XFapiSecret:'NzFlOWQ2YWY4NmQwZTU1N2ZiOTc3MzVj',
        vcn: 'xiaoyan',
      speed: 20,
      volume: 50,
      pitch: 50,
        selections: {
          p:null,
          title:null,
          modelContent:null,
          selectedGrade: null, // 存储选中的学级
          selectedSynonym: null, // 存储选中的同义词
          selectedCorrectVersion: null, // 存储选中的批改模式
          selectedEssayReport: null, // 存储选中的详细报告
        },
        tryItem: {
          "RequestId": "9cd0e024-5927-4c43-8fbf-0d36462cb4ca",
          "errorCode": "0",
          "Result": {
            "rawEssay": "Actually, it is sort of a fish berry jam. Lots of job loss is just one thing resulting from automation. We do the essential Python on 22nd September 2019. We do an important python on the 22nd of September 2019. We have 5 apples in the important things 5 on Sep 2019.",
            "sentNum": 5,
            "uniqueKey": "3b9e61e0-d6c1-4194-8cf6-2c4c9ae209c2",
            "essayFeedback": {
              "sentsFeedback": [
                {
                  "rawSent": "Actually, it is sort of a fish berry jam.",
                  "sentFeedback": "词汇频繁使用，建议替换新单词；不必要的修饰词，建议删除〖sort of〗"
                },
                {
                  "rawSent": "Lots of job loss is just one thing resulting from automation.",
                  "sentFeedback": "建议使用更正式的词汇来替换'job loss'"
                },
                {
                  "rawSent": "We do the essential Python on 22nd September 2019.",
                  "sentFeedback": "日期格式不一致，建议统一为'Month Day, Year'格式"
                },
                {
                  "rawSent": "We do an important python on the 22nd of September 2019.",
                  "sentFeedback": "大小写不一致，建议将'python'修改为'Python'"
                },
                {
                  "rawSent": "We have 5 apples in the important things 5 on Sep 2019.",
                  "sentFeedback": "数字应使用英文拼写，建议将'5'修改为'five'"
                }
              ]
            }
          }
        }
      };
    },
    watch: {
      // 监听好友信息变化，获取新的聊天记录
      frinedInfo() {
        this.getFriendChatMsg();
      },
    },
    mounted() {
      this.getFriendChatMsg(); // 获取初始聊天记录
    },
    methods: {
      async updateSet(updateSelections) {
  // 更新选择项
  this.selections = updateSelections;
  try {
    // 调用后端作文批改接口
    const res = await axios.post('http://localhost:5000/correct_writing', {
      q: this.selections.p,
      grade: this.selections.selectedGrade,
      title: this.selections.title,
      modelContent: "",
      isNeedSynonyms: "false",
      correctVersion: "basic",
      isNeedEssayReport: "false"
    });
    const response = res.data;
    console.log("批改返回结果：", response);

    // 将用户原始作文显示为一条聊天消息（类型 0：文本消息）
    let inputMsg = {
      headImg: this.frinedInfo.headImg,
      name: "zkx",
      time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
      msg: this.selections.p,
      chatType: 0,
      uid: "1001"
    };
    this.sendMsg(inputMsg);

    // 将批改结果作为一条作文批改消息（类型 9）发送
    let resultMsg = {
      headImg: this.frinedInfo.headImg,
      name: "zkx",
      time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
      msg: response, // 整个格式化后的批改结果
      showTotal: false,
      chatType: 9,
      uid: "1001"
    };
    this.sendMsg(resultMsg);
    // 切换作文批改界面（关闭作文编辑界面）
    this.clickWriting();
  } catch (error) {
    console.error('Error submitting the form:', error);
  }
},
      showT(item){
        item.showTotal = !item.showTotal;
      },
      SpeechAnlyise(item){
        item.isWindowVisible = !item.isWindowVisible;
      },
      SpeechToText(item){
  
      },
      async FinalAnlyise(){
        try {
          let message={
            session_id:"1001"
          }
      const response = await api.post('http://localhost:5001/judge', message);
      this.sendMsg({
        headImg: this.frinedInfo.headImg,
        name: this.frinedInfo.name,
        time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
        msg: response.data.output,
        chatType: 10, // 信息类型，0代表文字
        uid: "1002", // 发送者 ID
      });
    } catch (error) {
      console.error('Error sending message:', error);
    }
      },
      getTitle(item) {
        const titleRegex = /^(总评分|[1-5]\\.\\S+|总评语)：/;
        const match = item.match(titleRegex);
        return match ? match[0].replace(/：$/, '') : '';
      },
      getContent(item) {
        const titleRegex = /^(总评分|[1-5]\\.\\S+|总评语)：/;
        return item.replace(titleRegex, '').trim();
      },
      analyiseText(Text){
  
      },
    //翻译显示函数
      changeText(item){
        item.showTranslation=!item.showTranslation;
        console.log(item.showTranslation);
      },
      translateTexttest(output) {
        return "nihao";
      },
      //文本翻译
      async translateText(output) {
    try {
      const salt = new Date().getTime();
      const curtime = Math.round(new Date().getTime() / 1000);
      const str1 = this.appKey + this.truncate(output) + salt + curtime + this.key;
      const sign = CryptoJS.SHA256(str1).toString(CryptoJS.enc.Hex);
  
      const response = await axios.post('https://openapi.youdao.com/api', null, {
        params: {
          q: output,
          appKey: this.appKey,
          salt: salt,
          from: this.from,
          to: this.to,
          sign: sign,
          signType: 'v3',
          curtime: curtime,
          vocabId: this.vocabId,
        },
      });
  
      console.log(response.data);
      return response.data.translation[0];
    } catch (error) {
      console.error('Error:', error);
    }
  },
  
      truncate(q) {
        const len = q.length;
        if (len <= 20) return q;
        return q.substring(0, 10) + len + q.substring(len - 10, len);
      },

      /*async main1(output) {
  const audioContext = this.audioContext || new (window.AudioContext || window.webkitAudioContext)();
  this.audioContext = audioContext;

  const audioQueue = []; // 缓存音频片段队列
  let isPlaying = false; // 控制顺序播放

  function base64ToArrayBuffer(base64) {
    let binaryString = atob(base64);
    let len = binaryString.length;
    let bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) bytes[i] = binaryString.charCodeAt(i);
    return bytes.buffer;
  }

  function playAudioQueue() {
    if (isPlaying || audioQueue.length === 0) return;
    isPlaying = true;

    const audioData = audioQueue.shift();
    audioContext.decodeAudioData(audioData, (buffer) => {
      const source = audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContext.destination);
      source.start(0);
      
      source.onended = () => {
        isPlaying = false;
        playAudioQueue(); // 播放下一段
      };
    }, (error) => {
      console.error("Audio decode error:", error);
      isPlaying = false;
      playAudioQueue();
    });
  }

  const appId = this.XFappId;
  const apiKey = this.XFapiKey;
  const apiSecret = this.XFapiSecret;
  const host = "tts-api.xfyun.cn";
  const date = new Date().toUTCString();
  const signatureOrigin = `host: ${host}\ndate: ${date}\nGET /v2/tts HTTP/1.1`;
  const signatureSha = CryptoJS.HmacSHA256(signatureOrigin, apiSecret);
  const signature = CryptoJS.enc.Base64.stringify(signatureSha);
  const authorizationOrigin = `api_key="${apiKey}", algorithm="hmac-sha256", headers="host date request-line", signature="${signature}"`;
  const authorization = btoa(authorizationOrigin);
  const url = `wss://${host}/v2/tts?authorization=${encodeURIComponent(authorization)}&date=${encodeURIComponent(date)}&host=${host}`;

  const ttsWS = new WebSocket(url);

  ttsWS.onopen = () => {
    const params = {
      common: { app_id: appId },
      business: {
        aue: "lame",  // 强烈建议使用MP3
        sfl: 1,
        auf: "audio/L16;rate=16000",
        vcn: this.vcn,
        speed: this.speed,
        volume: this.volume,
        pitch: this.pitch,
        bgs: 1,
        tte: "UTF8"
      },
      data: {
        status: 2,
        text: btoa(unescape(encodeURIComponent(output)))
      }
    };
    ttsWS.send(JSON.stringify(params));
  };

  ttsWS.onmessage = (event) => {
    const jsonData = JSON.parse(event.data);
    if (jsonData.code !== 0) {
      console.error("TTS Error:", jsonData);
      ttsWS.close();
      return;
    }

    const audioBase64 = jsonData.data.audio;
    const audioBuffer = base64ToArrayBuffer(audioBase64);
    audioQueue.push(audioBuffer); // 推入音频片段
    playAudioQueue(); // 尝试播放队列中的数据

    if (jsonData.data.status === 2) {
      ttsWS.close();
    }
  };

  ttsWS.onerror = (err) => {
    console.error("TTS WebSocket error:", err);
  };
},*/


    async main(output) {
      console.log(0);
      const mp3 = await openai.audio.speech.create({
        model: "gpt-4o-mini-tts",
        voice: "coral",
        input: output,
        instructions: "Speak in a cheerful and positive tone.",
      });
      console.log(1);
      const buffer = await mp3.arrayBuffer();
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      audioContext.decodeAudioData(buffer, (buffer) => {
        const source = audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(audioContext.destination);
        source.start(0);
        console.log(2);
      }, (error) => {
        console.error('解码音频失败:', error);
      });
    },
      // 获取聊天记录
      getFriendChatMsg() {
        let params = {
          frinedId: this.frinedInfo.id,
        };
        getChatMsg(params).then((res) => {
          this.chatList = res;
          // 如果是图片消息，将图片加入图片列表中
          this.chatList.forEach((item) => {
            if (item.chatType == 2 && item.extend.imgType == 2) {
              this.srcImgList.push(item.msg);
            }
          });
          this.scrollBottom(); // 滚动到底部
        });
      },
      // 发送文本消息
      async sendText() {
  
        if (this.inputMsg) {
          let trText= await this.translateText(this.inputMsg);
          console.log(trText);
          let chatMsg = {
            headImg: this.frinedInfo.headImg,
            name: "zkx",
            time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
            msg: this.inputMsg,
            translateText:trText,
            showTranslation:false,
            chatType: 0, // 信息类型，0代表文字
            uid: "1001", // 发送者 ID
          };
          this.sendMsg(chatMsg); // 添加消息到聊天记录
          let message = {
            input: this.inputMsg,
            session_id:chatMsg.uid,
          };
          this.sendMessage(message); // 发送消息到服务器
          this.inputMsg = ""; // 清空输入框
        } else {
          this.$message({
            message: "消息不能为空哦~",
            type: "warning",
          });
        }
      },
      // 发送文字消息的函数
    async sendMessage(message){
    try {
      const response = await api.post('http://localhost:5005/chat', message);
      let trText= await this.translateText(response.data.output);
          console.log(trText);
      this.sendMsg({
        headImg: this.frinedInfo.headImg,
        name: this.frinedInfo.name,
        time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
        msg: response.data.output,
        translateText:trText,
        showTranslation:false,
        chatType: 0, // 信息类型，0代表文字
        uid: "1002", // 发送者 ID
      });
    } catch (error) {
      console.error('Error sending message:', error);
    }
  },
      // 开始录音
      // 开始录音并处理翻译
      startRecording() {
    this.rec = Recorder({
      type: "wav",
      sampleRate: 16000,
      bitRate: 16,
    });
  
    this.rec.open(() => {
      console.log("录音已打开");
      this.rec.start();
      this.isRecording = true; // 设置标志位
      console.log("已开始录音");
    }, (msg, isUserNotAllow) => {
      console.log((isUserNotAllow ? "UserNotAllow，" : "") + "无法录音:" + msg);
    });
  
    if (!this.rec) {
      console.error("未打开录音");
      return;
    }
  },
  
  async stopRecording() {
    if (!this.isRecording) {
      console.error("未开始录音，无法停止");
      return;
    }
  
    this.rec.stop(async (blob, duration) => {
      this.recBlob = blob;
      var localUrl = (window.URL || webkitURL).createObjectURL(blob);
      console.log("录音成功", blob, localUrl, "时长:" + duration + "ms");
  
      const data=await this.translate(blob);
      const translatedText=data.translateText;
      console.log(translatedText);
      const voice_evaluation= data.evaluation;
      console.log(voice_evaluation);
      this.rec.close();
      this.rec = null;
      this.isRecording = false; // 重置标志位
      let chatMsg = {
              headImg: require("@/assets/img/head_portrait.jpg"),
              name: "zkx",
              time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
              msg: localUrl,
              translateText: translatedText,
              showTranslation:false,
              chatType: 3,
              uid: "1001",
              evaluation: voice_evaluation.evaluation,
              overall:voice_evaluation.overall,
              accuracy:voice_evaluation.accuracy,
              integrity:voice_evaluation.integrity,
              fluency:voice_evaluation.fluency,
              speed:voice_evaluation.speed,
              isWindowVisible:false,
            };
      this.sendMsg(chatMsg); 
      let message = {
            input: chatMsg.translateText,
            id:chatMsg.uid,
          };
      this.sendMessage(message); // 发送消息到服务器
    }, (err) => {
      console.error("结束录音出错：" + err);
      this.rec.close();
      this.rec = null;
      this.isRecording = false; // 重置标志位
    });
  
    if (!this.rec) {
      console.error("未打开录音");
      return;
    }
  },
  
    // 发送音频到后端进行翻译
    async translate(audioBlob) {
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.wav');
  
      try {
        const response = await axios.post('http://localhost:5010/evaluate', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const data = response.data;
        console.log(data);
        return data;
  
      } catch (error) {
        console.error("翻译失败", error);
      }
    },
  
  
  
      // 播放语音消息
      playVoiceMessage() {
        if (this.voiceMessage) {
          const audio = new Audio(URL.createObjectURL(this.voiceMessage));
          audio.play();
        }
      },
      // 发送表情消息
      sendEmoji(msg) {
        let chatMsg = {
          headImg: require("@/assets/img/head_portrait.jpg"),
          name: "zkx",
          time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
          msg: msg,
          chatType: 1, // 信息类型，1代表表情
          extend: {
            imgType: 1, // 1代表表情，2代表本地图片
          },
          uid: "1001",
        };
        this.sendMsg(chatMsg); // 发送表情消息
        this.clickEmoji(); // 关闭表情选择器
      },
      // 发送本地图片
      sendImg(e) {
        let _this = this;
        let chatMsg = {
          headImg: require("@/assets/img/head_portrait.jpg"),
          name: "zkx",
          time: "09:12 AM",
          msg: "",
          chatType: 1, // 信息类型，1代表图片
          extend: {
            imgType: 2, // 2代表本地图片
          },
          uid: "1001",
        };
        let files = e.target.files[0];
        if (!e || !window.FileReader) return;
        let reader = new FileReader();
        reader.readAsDataURL(files);
        reader.onloadend = function() {
          chatMsg.msg = this.result; // 设置图片的 base64 数据
          _this.srcImgList.push(chatMsg.msg); // 将图片加入图片列表
        };
        this.sendMsg(chatMsg); // 发送图片消息
        e.target.files = null;
      },
      // 发送文件
      sendFile(e) {
        let chatMsg = {
          headImg: require("@/assets/img/head_portrait.jpg"),
          name: "zkx",
          time: "09:12 AM",
          msg: "",
          chatType: 2, // 信息类型，2代表文件
          extend: {
            fileType: "", // 文件类型
          },
          uid: "1001",
        };
        let files = e.target.files[0];
        chatMsg.msg = files;
        if (files) {
          // 根据文件类型设置扩展名
          switch (files.type) {
            case "application/msword":
            case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
              chatMsg.extend.fileType = 1;
              break;
            case "application/vnd.ms-excel":
            case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
              chatMsg.extend.fileType = 2;
              break;
            case "application/vnd.ms-powerpoint":
            case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
              chatMsg.extend.fileType = 3;
              break;
            case "application/pdf":
              chatMsg.extend.fileType = 4;
              break;
            case "application/zip":
            case "application/x-zip-compressed":
              chatMsg.extend.fileType = 5;
              break;
            case "text/plain":
              chatMsg.extend.fileType = 6;
              break;
            default:
              chatMsg.extend.fileType = 0;
          }
          this.sendMsg(chatMsg); // 发送文件消息
          e.target.files = null;
        }
      },
      // 添加消息到聊天列表并滚动到底部
      sendMsg(msgList) {
        this.chatList.push(msgList);
        this.scrollBottom(); // 滚动到底部
      },
      // 滚动到聊天记录的底部
      scrollBottom() {
        this.$nextTick(() => {
          const scrollDom = this.$refs.chatContent;
          animation(scrollDom, scrollDom.scrollHeight - scrollDom.offsetHeight);
        });
      },
      // 切换表情选择器的显示状态
      clickEmoji() {
        this.showEmoji = !this.showEmoji;
      },
      // 切换作文模式的显示状态
      clickWriting() {
        this.showWriting = !this.showWriting;
      },
      // 视频功能（未实现）
      video() {
        this.$message("该功能还没有开发哦，敬请期待~");
      },
      // 电话功能（未实现）
      telephone() {
        this.$message("该功能还没有开发哦，敬请期待~");
      },
    },
  };
  </script>
            
  <style lang="scss" scoped>
  .Trans{
    font-size: 16px;
    font-family: 楷体;
  }
  
  .chat-window {
    width: 100%;
    height: 100%;
    margin-left: 20px;
    position: relative;
  
    .top {
      margin-bottom: 50px;
      &::after {
        content: "";
        display: block;
        clear: both;
      }
      .head-pic {
        float: left;
      }
      .info-detail {
        float: left;
        margin: 5px 20px 0;
        .name {
          font-size: 20px;
          font-weight: 600;
          color: #fff;
        }
        .detail {
          color: #9e9e9e;
          font-size: 12px;
          margin-top: 2px;
        }
      }
      .other-fun {
        float: right;
        margin-top: 20px;
        span {
          margin-left: 30px;
          cursor: pointer;
        }
        input {
          display: none;
        }
      }
    }
  
    .botoom {
      width: 100%;
      height: 70vh;
      background-color: rgb(50, 54, 68);
      border-radius: 20px;
      padding: 20px;
      box-sizing: border-box;
      position: relative;
      .chat-content {
        width: 100%;
        height: 85%;
        overflow-y: scroll;
        padding: 20px;
        box-sizing: border-box;
        &::-webkit-scrollbar {
          width: 0;
          height: 0;
          display: none;
        }
  
        .chat-wrapper {
          position: relative;
          word-break: break-all;
          .chat-friend {
            width: 100%;
            float: left;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            .chat-text {
              max-width: 90%;
              padding: 20px;
              border-radius: 20px 20px 20px 5px;
              background-color: rgb(56, 60, 75);
              color: #fff;
              &:hover {
                background-color: rgb(39, 42, 55);
              }
            }
            .chat-img {
              img {
                width: 100px;
                height: 100px;
              }
            }
            .info-time {
              margin: 10px 0;
              color: #fff;
              font-size: 14px;
              img {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                vertical-align: middle;
                margin-right: 10px;
              }
              span:last-child {
                color: rgb(101, 104, 115);
                margin-left: 10px;
                vertical-align: middle;
              }
            }
          }
  
          .chat-me {
            width: 100%;
            float: right;
            margin-bottom: 20px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: flex-end;
            .chat-transition {
              max-width: 90%;
              padding: 20px;
              border-radius: 20px 20px 5px 20px;
              background-color: rgb(29, 144, 245);
              color: #fff;
              &:hover {
                background-color: rgb(26, 129, 219);
              }
            }
            .chat-text {
              float: right;
              max-width: 90%;
              padding: 20px;
              border-radius: 20px 20px 5px 20px;
              background-color: rgb(29, 144, 245);
              color: #fff;
              &:hover {
                background-color: rgb(26, 129, 219);
              }
            }
            .chat-img {
              img {
                max-width: 300px;
                max-height: 200px;
                border-radius: 10px;
              }
            }
            .info-time {
              margin: 10px 0;
              color: #fff;
              font-size: 14px;
              display: flex;
              justify-content: flex-end;
              img {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                vertical-align: middle;
                margin-left: 10px;
              }
              span {
                line-height: 30px;
              }
              span:first-child {
                color: rgb(101, 104, 115);
                margin-right: 10px;
                vertical-align: middle;
              }
            }
          }
        }
      }
      .chatInputs {
        width: 90%;
        position: absolute;
        bottom: 0;
        margin: 3%;
        display: flex;
        .boxinput {
          margin-right: 5px;
          width: 50px;
          height: 50px;
          background-color: rgb(66, 70, 86);
          border-radius: 15px;
          border: 1px solid rgb(80, 85, 103);
          position: relative;
          cursor: pointer;
          img {
            width: 30px;
            height: 30px;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
          }
        }
        .emoji {
          transition: 0.3s;
          &:hover {
            background-color: rgb(46, 49, 61);
            border: 1px solid rgb(71, 73, 82);
          }
        }
  
        .inputs {
          width: 90%;
          height: 50px;
          background-color: rgb(66, 70, 86);
          border-radius: 15px;
          border: 2px solid rgb(34, 135, 225);
          padding: 10px;
          box-sizing: border-box;
          transition: 0.2s;
          font-size: 20px;
          color: #fff;
          font-weight: 100;
          margin: 0 20px;
          &:focus {
            outline: none;
          }
        }
        .send {
          background-color: rgb(29, 144, 245);
          border: 0;
          transition: 0.3s;
          box-shadow: 0px 0px 5px 0px rgba(0, 136, 255);
          &:hover {
            box-shadow: 0px 0px 10px 0px rgba(0, 136, 255);
          }
        }
      }
  
    }
  
    .message-options {
    margin-top: 10px;
    display: flex;
    gap: 10px;
    
    .translate-btn, .speak-btn {
      background-color: transparent;
      border: none;
      cursor: pointer;
      img {
        width: 24px;
        height: 24px;
      }
    }
  }
  
  }
  </style>
  