const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: './',
  devServer: {
    hot: true,//自动保存
    proxy: {

      '/api': {
        target: 'https://openapi.youdao.com',
        secure: true, // 如果是 https 接口，需要配置这个参数
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
    },
  },
})
