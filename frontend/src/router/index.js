import VueRouter from 'vue-router'
 
import ChatHome from '../view/pages/chatHome/index.vue'
import ChatGroup from '../view/pages/chatGroup/index.vue'
import Video from '../view/pages/video.vue'
import Lingting from '../view/pages/lingting.vue'
import Setting from '../view/pages/setting.vue'
import ChatWindow from '../view/pages/chatHome/chatwindow.vue'
import ChatWindowG from '../view/pages/chatGroup/chatwindowG.vue'
export default new VueRouter({
    routes: [
        {
            path: "/",
            redirect: "/ChatHome",
          },
          {
            path: "/Video",
            name: "Video",
            component: Video,
        }, 
        {
            path: "/ChatWindow",
            name: "ChatWindow",
            component: ChatWindow,
        }, 
        {
            path: "/ChatWindowG",
            name: "ChatWindowG",
            component: ChatWindowG,
        }, 
        {
            path: "/ChatHome",
            name: "ChatHome",
            component: ChatHome,
        }, 
        {
            path: "/",
            redirect: "/ChatGroup",
          },   
        {
            path: "/ChatGroup",
            name: "ChatGroup",
            component: ChatGroup
        }, 
        {
            path: "/Lingting",
            name: "Lingting",
            component: Lingting
        },   
        {
            path: "/Setting",
            name: "Setting",
            component: Setting
        },    
    ]
})