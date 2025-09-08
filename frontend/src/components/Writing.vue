<template>
    <div class="emoji-content">
      <div class="emoji">
        <div class="emoji-wrapper">
          <ul class="emoji-list">
            <select v-model="selectedGrade">
                <option v-for="(item, index) in Grades" :value="item.value" :key="index">
                    {{ item.name }}
                </option>
            </select>
            <span class="FF">考学年级</span>
            <textarea v-model="title" placeholder="请输入作文标题（没有可以为空）..."></textarea>
            <textarea v-model="p" placeholder="请输入作文正文..."></textarea>
            <el-button type="primary" round ><span class="BB" @click="sendMessage">批改！</span></el-button>
            <el-button type="danger" icon="el-icon-delete" circle @click="clear"></el-button>
          </ul>
        </div>
      </div>
      <div class="mask" @click="closeEmoji"></div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        p:null,
        title:null,
        modelContent:null,
        selectedGrade: null, // 存储选中的学级
        selectedSynonym: null, // 存储选中的同义词
        selectedCorrectVersion: null, // 存储选中的批改模式
        selectedEssayReport: null, // 存储选中的详细报告
            Grades: [
    { name: "不考虑级别，单纯评价句子好坏", value: "default" },
    { name: "小学", value: "elementary" },
    { name: "初中", value: "junior" },
    { name: "高中", value: "high" },
    { name: "四级", value: "cet4" },
    { name: "六级", value: "cet6" },
    { name: "考研", value: "graduate" },
    { name: "考研英语(一)大作文", value: "graduate_b1" },
    { name: "考研英语(一)小作文", value: "graduate_a1" },
    { name: "考研英语(二)小作文", value: "graduate_a2" },
    { name: "考研英语(二)大作文", value: "graduate_b2" },
    { name: "托福", value: "toefl" },
    { name: "托福-独立写作", value: "toefl_independent" },
    { name: "托福-综合写作", value: "toefl_comprehensive" },
    { name: "考研", value: "graduate" },
    { name: "GRE", value: "gre" },
    { name: "雅思", value: "ielts" },
    { name: "雅思-task1", value: "ielts_task1" },
    { name: "雅思-task2", value: "ielts_task2" },
    { name: "学术写作", value: "academic" }
],
            Synonyms: [
                { name: '是', value:'true'},
                { name: '否', value:'false'},
            ],
            correctVersion: [
                { name: '基础',value:'basic'},
                { name: '高级',value:'advanced'},
            ],
            EssayReport:[
                { name: '是', value:'true'},
                { name: '否', value:'false'},
            ]
      };
    },
    methods: {
        clear(){
            this.p = null;
            this.title = null;
            this.modelContent = null;
            this.selectedGrade = null;
            this.selectedSynonym = null;
            this.selectedCorrectVersion = null;
            this.selectedEssayReport = null;
        },
        sendMessage(){
            this.$emit("updateSelections", {
                p: this.p,
                title: this.title,
                selectedGrade: this.selectedGrade,
            });
        },
      closeEmoji() {
        this.$emit("closeEmoji");

      }
    },
  };
  </script>
  
  <style lang="scss" scoped>
    .FF{
        font-family: 楷体;
        font-size: 16px;
        margin-left: 20px;
        color: #e2dada;
    }
    .BB{
        font-family: 楷体;
        font-size: 16px;
        color: #e2dada;
    }
    textarea{
        -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            padding: 8px;
            border: 1px solid rgb(50, 54, 68);
            border-radius: 5px;
            background-color: rgb(50, 54, 68);
            color: #cbc7c7;
            font-size: 16px;
            font-family: 楷体;
            width: 300px;
            margin-bottom: 5%;
    }
    select {
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            padding: 8px;
            border: 1px solid rgb(50, 54, 68);
            border-radius: 5px;
            background-color: rgb(50, 54, 68);
            color: #cbc7c7;
            font-size: 16px;
            font-family: 楷体;
            width: 240px;
            margin-bottom: 5%;
        }
 
        /* 美化select的下拉箭头 */
        select:after {
            content: "\25BC"; /* Unicode编码，表示向下的箭头 */
            position: absolute;
            top: 12px;
            right: 10px;
        }
 
        /* 美化选项内容 */
        option {
            padding: 5px;
            background-color: rgb(50, 54, 68);
            color: #c8c6c6;
        }

  .emoji-content {
    .emoji {
    width: 400px;
    height: 200px;
    background-color: rgb(39, 42, 55);
    position: absolute;
    top: -220px;
    left: -10px;
    border-radius: 10px;
    transition: 0.3s;
    z-index: 3;
  
    &::after {
      content: "";
      display: block;
      width: 0;
      height: 0;
      border-top: 10px solid rgb(39, 42, 55);
      border-right: 10px solid transparent;
      border-left: 10px solid transparent;
      position: absolute;
      bottom: -8px;
      left: 15px;
      z-index: 100;
    }
    .emoji-wrapper {
      width: 100%;
      height: 100%;
      overflow-y: scroll;
      padding: 10px;
      box-sizing: border-box;
      position: relative;
      &::-webkit-scrollbar {
        /*滚动条整体样式*/
        width: 4px; /*高宽分别对应横竖滚动条的尺寸*/
        height: 1px;
      }
      &::-webkit-scrollbar-thumb {
        /*滚动条里面小方块*/
        border-radius: 10px;
        box-shadow: inset 0 0 5px rgba(97, 184, 179, 0.1);
        background: rgb(95, 101, 122);
      }
      &::-webkit-scrollbar-track {
        /*滚动条里面轨道*/
        box-shadow: inset 0 0 5px rgba(87, 175, 187, 0.1);
        border-radius: 10px;
        background: rgb(39, 42, 55);
      }
      .emoji-list {
        display: flex;
        justify-content: flex-start;
        flex-wrap: wrap;
        margin-left: 10px;
        .emoji-item {
          list-style: none;
          width: 50px;
          height: 50px;
          border-radius: 10px;
          margin: 5px;
          position: relative;
          cursor: pointer;
          &:hover {
            background-color: rgb(50, 54, 68);
          }
          img {
            width: 35px;
            height: 35px;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
          }
        }
      }
    }
  
  }
  .mask {
      width: 100%;
      height: 100%;
      position: fixed;
      background: transparent;
      left: 0;
      top: 0;
      z-index: 1;
    }
  }
  
  </style>