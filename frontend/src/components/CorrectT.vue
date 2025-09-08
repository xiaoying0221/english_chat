<template>
  <transition name="fade">
    <div class="evaluation-container">
      <!-- 整体评估结果展示 -->
      <div class="overall">
        <h3>整体得分: <strong>{{ result.totalScore }}</strong> / {{ result.fullScore }} 分</h3>
      </div>
      <div class="others">
        <p>语法得分: <strong>{{ result.majorScore.grammarScore }}</strong> 分</p>
        <p>结构得分: <strong>{{ result.majorScore.structureScore }}</strong> 分</p>
        <p>重点得分: <strong>{{ result.majorScore.emphasis }}</strong> 分</p>
      </div>

      <!-- 文章反馈与建议 -->
      <div class="feedback-container">
        <h3>作文建议与反馈</h3>
        <p>总体建议: {{ result.essayAdvice }}</p>
        <p>语法建议: {{ result.majorScore.grammarAdvice }}</p>
        <p>结构建议: {{ result.majorScore.structureAdvice }}</p>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    result: {
      type: Object,
      required: true,
      default: () => ({
        totalScore: 0,
        fullScore: 25,
        majorScore: {
          grammarScore: 0,
          structureScore: 0,
          emphasis: 0,
          grammarAdvice: '',
          structureAdvice: '',
        },
        essayAdvice: '',
        rawEssay: '',
        essayFeedback: {
          sentsFeedback: []
        },
        allFeatureScore: {}
      })
    }
  },
  data() {
    return {
      sentences: [],
      feedbackMap: {},
      selectedFeedback: null,
      selectedFeedbackIndex: null,
    };
  },
  watch: {
    // 监听result对象更新，实现数据响应式刷新
    result: {
      immediate: true,
      deep: true,
      handler(newVal) {
        this.initFeedback(newVal);
      },
    },
  },
  methods: {
    initFeedback(result) {
      // 拆分原文句子
      if (result.rawEssay) {
        this.sentences = result.rawEssay.split(/(?<=[.?!])\s+/);
      } else {
        this.sentences = [];
      }

      // 构建反馈映射
      this.feedbackMap = {};
      if (result.essayFeedback && result.essayFeedback.sentsFeedback) {
        result.essayFeedback.sentsFeedback.forEach((item, idx) => {
          this.feedbackMap[idx] = item.sentFeedback;
        });
      }
    },
    showFeedback(index) {
      this.selectedFeedbackIndex = index;
      this.selectedFeedback = this.feedbackMap[index] || 'No feedback available for this sentence.';
    },
    // 根据得分计算颜色（备用）
    getScoreColor(score) {
      const red = Math.min(255, Math.max(0, Math.round(255 * (100 - score) / 100)));
      const green = Math.min(255, Math.max(0, Math.round(255 * score / 100)));
      return `rgb(${red}, ${green}, 0)`;
    },
  }
};
</script>

<style scoped>
.evaluation-container {
  margin: 20px;
  padding: 20px;
  font-family: 楷体;
  border-radius: 5px;
  border: 1px solid #cccccc;
  background-color: #5296de;
}

.overall {
  font-size: 20px;
  margin-bottom: 20px;
  color: #efe6e8;
  font-family: 楷体;
  border-radius: 5px;
}

.others {
  font-size: 16px;
  margin-bottom: 20px;
  font-family: 楷体;
  border-radius: 5px;
  color: #a09b9d;
}

.feedback-container {
  margin-bottom: 20px;
  color: #a09b9d;
}

.essay-container {
  background-color: #f0f3f5;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #e8e8e8;
  padding: 10px;
  border-radius: 5px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
