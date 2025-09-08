<template>
  <transition name="fade">
    <div v-if="visible" class="evaluation-container">
      <!-- 整体评估结果展示 -->
      <div class="overall">
        <p>整体得分: {{ overall }} 分</p>
      </div>
      <div class="others">
        <p>语速: {{ speed }} 词/分钟</p>
        <p>发音准确度: {{ accuracy }} 分</p>
        <p>流利度: {{ fluency }} 分</p>
        <p>完整度: {{ integrity }} 分</p>
      </div>

      <!-- 遍历并展示每个单词的音标和发音得分 -->
      <div class="words-container">
        <div v-for="(word, index) in evaluation" :key="index" class="word-item">
          <p class="word-text">
            单词: {{ word.word }}
          </p>
          <p class="ipa-text">
            音标:
            <span v-for="(phoneme, idx) in word.phonemes" :key="idx" :style="{ color: getPhonemeColor(phoneme.pronunciation) }">
              {{ phoneme.phoneme }}
            </span>
          </p>
          <p class="pronunciation-score">单词发音得分: {{ word.pronunciation }} 分</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    evaluation: {
      type: Array,
      default: () => []
    },
    overall: {
      type: Number,
      default: 0
    },
    speed: {
      type: Number,
      default: 0
    },
    accuracy: {
      type: Number,
      default: 0
    },
    fluency: {
      type: Number,
      default: 0
    },
    integrity: {
      type: Number,
      default: 0
    }
  },
  methods: {
    // 根据发音得分计算颜色，得分越高颜色越绿，得分越低颜色越红
    getPhonemeColor(pronunciation) {
      const red = Math.min(255, Math.max(0, Math.round(255 * (100 - pronunciation) / 100)));
      const green = Math.min(255, Math.max(0, Math.round(255 * pronunciation / 100)));
      return `rgb(${red}, ${green}, 0)`; // 红到绿的颜色渐变
    }
  }
}
</script>

<style scoped>
.evaluation-container {
  margin: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
}

.overall {
  color: rgba(50, 110, 222, 0.911);
  font-family: 楷体;
  font-size: 20px;
  margin-bottom: 20px;
}

.others {
  font-family: 楷体;
  font-size: 16px;
  margin-bottom: 20px;
}

.words-container {
  margin-top: 20px;
}

.word-item {
  margin-bottom: 20px;
}

.word-text {
  font-family: 楷体;
  font-weight: bold;
}

.ipa-text {
  font-family: 楷体;
  font-family: monospace;
  font-size: 16px;
}

.pronunciation-score {
  font-family: 楷体;
  color: #666;
  font-size: 14px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
