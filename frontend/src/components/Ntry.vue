<template>
    <div class="nav-container d-flex flex-column align-items-center py-3">
      <!-- 折叠按钮，移动端显示 -->
      <button @click="toggleNav" class="btn btn-primary d-lg-none mb-3">☰</button>
      <!-- 导航菜单，使用 Bootstrap 的显示类控制显示/隐藏 -->
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
      <!-- 头像 -->
      <div class="own-pic mt-auto" v-if="!isCollapsed || !isMobile">
        <HeadPortrait :imgUrl="imgUrl"></HeadPortrait>
      </div>
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
        isCollapsed: false,
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
            this.$router.push({ name: "ChatHome" });
            break;
          case 1:
            this.$router.push({ name: "ChatGroup" });
            break;
          case 2:
          case 3:
          case 4:
            this.$message("该功能还没有开发哦，敬请期待一下吧~🥳");
            break;
          default:
            this.$router.push({ name: "ChatHome" });
        }
        this.current = index;
      },
      toggleNav() {
        this.isCollapsed = !this.isCollapsed;
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
    background-color:rgb(39, 42, 55);
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
  