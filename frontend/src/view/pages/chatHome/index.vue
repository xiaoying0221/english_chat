<template>
  <div class="chatHome">

    
    <!-- 左侧的聊天列表区域，使用 v-if 来控制显示和隐藏 -->
    <div class="chatLeft" v-if="!isMobile || FlagIndex">
      <div class="title">
        <h1></h1> <!-- 聊天应用标题 -->
      </div>
      <div class="online-person">
        <span class="onlin-text">Chat List</span> <!-- "Chat List" 文字显示 -->
        <div class="person-cards-wrapper">
          <!-- 循环渲染好友列表中的每一个好友信息 -->
          <div
            class="personList"
            v-for="personInfo in personList"
            :key="personInfo.id"
            @click="clickPerson(personInfo)"  
          >
            <!-- 使用 PersonCard 组件来显示每个好友的信息 -->
            <PersonCard
              :personInfo="personInfo"
              :pcCurrent="pcCurrent" 
            ></PersonCard>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 右侧的聊天窗口区域 -->
    <div class="chatRight" v-if="!FlagIndex || !isMobile">
      <!-- 动态渲染聊天窗口 -->
      <div v-if="showChatWindow">
        <!-- 当有聊天内容时，显示 ChatWindow 组件 -->
        <ChatWindow
          :frinedInfo="chatWindowInfo"  
          @personCardSort="personCardSort" 
          @Return="Return"
        ></ChatWindow>
      </div>
      <div class="showIcon" v-else>
        <!-- 当没有选择好友时，显示图标提示用户 -->
        
      </div>
    </div>
  </div>
</template>

<script>
import PersonCard from "@/components/PersonCard.vue";  // 导入显示好友信息的组件
import ChatWindow from "./chatwindow.vue";  // 导入聊天窗口组件

import { getFriend } from "@/api/getData";  // 导入获取好友数据的 API 调用
export default {
  name: "App",
  components: {
    PersonCard, // 注册 PersonCard 组件
    ChatWindow, // 注册 ChatWindow 组件
  },
  data() {
    return {
      pcCurrent: "",  // 当前选中的好友ID
      personList: [], // 好友列表
      showChatWindow: false,  // 控制是否显示聊天窗口
      chatWindowInfo: {},  // 当前聊天窗口显示的好友信息
      isMobile: false,  // 判断是否是移动端
      showChatList: false, // 控制移动端聊天列表的显示隐藏
      FlagIndex: false, //lse, 
    };
  },
  mounted() {
    this.FlagIndex= this.$route.query.flag;
    console.log('chat:',this.FlagIndex);
    console.log("time:",this.$route.query.time)
    // 组件挂载时获取好友数据
    getFriend().then((res) => {
      this.personList = res;  // 将获取到的好友数据赋值给 personList
    });
    this.checkIfMobile();
    window.addEventListener("resize", this.checkIfMobile);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkIfMobile);
  },
  methods: {
    // 点击好友列表中的某个好友时，展示聊天窗口并设置当前聊天对象
    clickPerson(info) {
    this.showChatWindow = true;
    this.chatWindowInfo = info;
    this.pcCurrent = info.id;
    if (this.isMobile) {
      this.FlagIndex = false;
      console.log("FlagIndex changed to false:", this.FlagIndex); // 检查FlagIndex的更新
      this.$forceUpdate();  // 强制刷新视图
    }
  },
  Return(){
    this.FlagIndex = true;
  },
    // 用于将点击过的好友排到列表顶部
    personCardSort(id) {
      if (id !== this.personList[0].id) {  // 如果点击的好友不是列表中的第一个
        console.log(id);
        let nowPersonInfo;
        for (let i = 0; i < this.personList.length; i++) {
          if (this.personList[i].id == id) {  // 找到点击的好友信息
            nowPersonInfo = this.personList[i];
            this.personList.splice(i, 1);  // 将该好友从原来的位置移除
            break;
          }
        }
        this.personList.unshift(nowPersonInfo);  // 将该好友放到列表的最前面
      }
    },
    // 判断是否是移动端
    checkIfMobile() {
      this.isMobile = window.innerWidth <= 768;
      console.log(this.isMobile);
    },
    // 切换聊天列表的显示和隐藏
    toggleNav() {
      this.showChatList = !this.showChatList;
    },
  },
};
</script>

<style lang="scss" scoped>
.chatHome {
  display: flex;  // 将左侧和右侧的区域并排显示
  position: relative;

  .toggle-btn {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 10;
  }

  .chatLeft {
    width: 280px;  // 左侧区域的宽度
    .title {
      color: #fff;
      padding-left: 10px;
    }
    .online-person {
      margin-top: 100px;  // 好友列表距离顶部的间距
      .onlin-text {
        padding-left: 10px;
        color: rgb(176, 178, 189);
      }
      .person-cards-wrapper {
        padding-left: 10px;
        height: 65vh;  // 好友列表的高度
        margin-top: 20px;
        overflow: hidden;
        overflow-y: scroll;  // 当好友列表超出高度时，启用滚动条
        box-sizing: border-box;
        &::-webkit-scrollbar {
          width: 0; /* Safari,Chrome 隐藏滚动条 */
          height: 0; /* Safari,Chrome 隐藏滚动条 */
          display: none; /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
        }
      }
    }
  }

  .chatRight {
    flex: 1;  // 右侧区域自动填充剩余的宽度
    padding-right: 30px;
    .showIcon {
      position: absolute;
      top: calc(50% - 150px); /* 垂直居中 */
      left: calc(50% - 50px); /* 水平居中 */
      .icon-snapchat {
        width: 300px;
        height: 300px;
        font-size: 300px;
      }
    }
  }
}
</style>
