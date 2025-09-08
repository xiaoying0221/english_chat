<template>
  <div class="home">
    <el-container height="100%">
      <!-- 侧边导航栏 -->
      <el-aside :width="isMobile ? '100px' : '100px'">
        <!-- 移动端显示的呼出菜单按钮 -->
        <button @click="toggleNav"  class="btn btn-primary d-lg-none mb-3">☰</button>

        <!-- 导航菜单，使用 Bootstrap 的 d-none 类控制在移动端默认隐藏 -->
        <div :class="['nav-menu-wrapper', { 'd-none': isCollapsed && isMobile }]">
          <ul class="nav flex-column">
            <li
              v-for="(item, index) in menuList"
              :key="index"
              :class="['nav-item', { 'active': index == current }]"
              @click="changeMenu(index)"
            >
              <a class="nav-link d-flex align-items-center" href="#">
                <div class="block me-2"></div>
                <span class="iconfont" :class="item"></span>
              </a>
            </li>
          </ul>
        </div>

        <!-- 头像部分，移动端仅当导航栏展开时显示 -->
        <div class="own-pic mt-auto" v-if="!isCollapsed || !isMobile">
          <HeadPortrait :imgUrl="imgUrl"></HeadPortrait>
        </div>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import HeadPortrait from "./HeadPortrait.vue";

export default {
  components: {
    HeadPortrait,
  },
  data() {
    return {
      menuList: [
        "icon-xinxi",
        "icon-shipin",
        "icon-shu",
        "icon-shandian",
        "icon-shezhi",
      ],
      current: 0,
      imgUrl: require('@/assets/img/head_portrait.jpg'),
      isCollapsed: true, // 默认收起
      isMobile: false,
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
    changeMenu(index) {
      switch (index) {
        case 0:
        this.$router.push({ path: '/ChatHome', query: { flag: true, time: Date.now() } });
          break;
        case 1:
          this.$router.push({ name: "ChatGroup", query: { flag: true, time: Date.now() } });
          break;
        case 2:
        case 3:
        case 4:
          this.$message("该功能还没有开发哦，敬请期待一下吧~🥳");
          break;
        default:
      }
      this.current = index;
      this.toggleNav(); // 关闭导航栏
    },
    toggleNav() {
      this.isCollapsed = !this.isCollapsed;
      this.$emit('update-nav-data',this.isCollapsed);
    },
    checkIfMobile() {
      this.isMobile = window.innerWidth <= 768;
    }
  },
};
</script>

<style lang="scss" scoped>
.nav-container {
  width: 100%;
  height: 90vh;
  border-radius: 20px 0 0 20px;
  background-color: rgb(39, 42, 55);
}

.nav-item.active .nav-link {
  color: rgb(29, 144, 245) !important;
}

.block {
  background-color: rgb(29, 144, 245);
  width: 6px;
  height: 25px;
  border-radius: 4px;
  opacity: 0;
  transition: 0.3s;
}

.nav-item:hover .block,
.nav-item.active .block {
  opacity: 1;
}

.own-pic {
  margin-top: auto;
}
</style>
