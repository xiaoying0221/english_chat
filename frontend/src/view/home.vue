<template>
  <div class="home">
    <el-container height="100%">
      <el-aside :width="isMobile ? '100px' : '100px'">
        <Nav @update-nav-data="handleNavData"></Nav>
      </el-aside>
      <el-main >
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Nav from "../components/Nav.vue";

export default {
  name: "App",
  components: {
    Nav,
  },
  data() {
    return {
      isMobile: false,
      FlagNav: false,
    };
  },
  mounted() {
    this.checkIfMobile();
    window.addEventListener("resize", this.checkIfMobile);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkIfMobile);
  },
  methods: {
    handleNavData(data) {
      this.FlagNav = !data; // 处理从 Nav 中接收到的数据
      console.log(this.FlagNav);
    },
    checkIfMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
  },
};
</script>

<style lang="scss" scoped>
.home {
  width: 90vw;
  height: 90vh;
  background-color: rgb(39, 42, 55);
  border-radius: 15px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  overflow: hidden;
}
</style>
