<template>
  <div>
    <h2>Essay Feedback</h2>
    <p v-for="(sentence, index) in sentences" :key="index" @click="showFeedback(index)">
      <span :class="{ highlight: feedbackMap[index] }">{{ sentence }}</span>
    </p>
    <div v-if="selectedFeedback" class="feedback-box">
      <h3>Feedback:</h3>
      <p>{{ selectedFeedback }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    result: {
      type: Object,
      required: true, // 明确要求必须从父组件传递 result 对象
    },
  },
  data() {
    return {
      sentences: [],
      feedbackMap: {},
      selectedFeedback: null,
    };
  },
  watch: {
    // 当后端返回的数据变化时自动重新计算句子和反馈
    result: {
      immediate: true,
      handler(newVal) {
        this.initEssayFeedback(newVal);
      },
    },
  },
  methods: {
    initEssayFeedback(result) {
      if (result.rawEssay) {
        this.sentences = result.rawEssay.split(/(?<=[.?!])\s+/);
      } else {
        this.sentences = [];
      }

      this.feedbackMap = {};

      if (result.essayFeedback && Array.isArray(result.essayFeedback.sentsFeedback)) {
        result.essayFeedback.sentsFeedback.forEach((item, idx) => {
          this.feedbackMap[idx] = item.sentFeedback || '';
        });
      }
    },
    showFeedback(index) {
      this.selectedFeedback = this.feedbackMap[index] || 'No feedback available for this sentence.';
    },
  },
};
</script>

<style scoped>
.highlight {
  color: rgb(246, 175, 60);
  cursor: pointer;
}
.feedback-box {
  margin-top: 20px;
  padding: 10px;
  font-family: 楷体;
  border-radius: 5px;
  border: 1px solid #cccccc;
  background-color: #5296de;
}
</style>
