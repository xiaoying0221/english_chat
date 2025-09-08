const Mock = require("mockjs");

Mock.mock(/friend\/friendList/, 'post', () => { //三个参数。第一个：路径，第二个：请求方式post/get，第三个：回调，返回值
    return friendList
})

Mock.mock(/friend\/chatMsg/, 'post', (config) => { //三个参数。第一个：路径，第二个：请求方式post/get，第三个：回调，返回值
    let params = JSON.parse(config.body)
    if (params.frinedId == "1002")
        return chatMsg1002
    if (params.frinedId == "1003")
        return chatMsg1003
    if (params.frinedId == "1004")
        return chatMsg1004
    if(params.frinedId == "1005")
        return chatMsg1005
    
    
})

Mock.mock(/friend\/groupList/, 'post', () => { //三个参数。第一个：路径，第二个：请求方式post/get，第三个：回调，返回值
    return groupList
})

let friendList = Mock.mock(
    [
        {
            img: "",
            name: "Alloy",
            detail: "Hi, I’m Alloy!",
            id: "1002",
            headImg: require("frontend/src/assets/img/ENTP.png"),

        },
        {
            img: "",
            name: "Lucas",
            detail: "An ENFP ",
            id: "1003",
            headImg: require("frontend/src/assets/img/enfp.png"),

        },
        {
            img: "",
            name: "Sophia",
            detail: "An INTJ",
            id: "1004",
            headImg: require("frontend/src/assets/img/intj.png"),

        },
    ]
)

let groupList = Mock.mock(
    [
        {
            img: "",
            name: "Surprise Group",
            detail: "Science and art",
            id: "1005",
            headImg: require("frontend/src/assets/img/Sen.jpg"),

        },
    ]
)

let chatMsg1002 = Mock.mock(
    [
        {
            headImg: require("frontend/src/assets/img/ENTP.png"),
            name: "Alloy",
            time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
            msg: "Hey there! So, let’s jump right into it. What’s the most exciting thing you’ve done recently? I love hearing people’s stories!",
            translateText: "嘿!那么，让我们直接开始吧。你最近做过的最令人兴奋的事情是什么？我喜欢听别人讲故事！",
            showTranslation: false,
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
    ]
)
let chatMsg1003 = Mock.mock(
    [
        {
            headImg: require("frontend/src/assets/img/enfp.png"),
            name: "Lucas",
            time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
            msg: "Hi! It’s so great to meet you. Tell me, what’s something you’re really passionate about?",
            translateText: "嗨！很高兴见到你。告诉我，你真正热衷的是什么？",
            showTranslation: false,
            chatType: 0, //信息类型，0文字，1图片
            uid: "1003", //uid
        },
    ]
)
let chatMsg1004 = Mock.mock(
    [
        {
            headImg: require("frontend/src/assets/img/intj.png"),
            name: "Sophia",
            time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
            msg: "Hello. Let’s get started. What’s your main goal for improving your English?",
            translateText: "你好。让我们开始吧。你提高英语水平的主要目标是什么？",
            showTranslation: false,
            chatType: 0, //信息类型，0文字，1图片
            uid: "1004", //uid
        },
    ]
)
let chatMsg1005 = Mock.mock(
    [
        {
            headImg: require("frontend/src/assets/img/enystan.jpg"),
            name: "Albert Einstein",
            time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
            msg: "Ah, welcome to this fascinating dialogue between science and art! Today, we stand at the intersection of these two seemingly different realms, but I would argue that they are not so separate after all. You see, both science and art seek to understand the mysteries of the universe, just through different lenses. In my work, imagination has always been my most important tool—yes, more important than knowledge. But enough about me! I’m curious to hear your thoughts. Tell me, as a young scientist (or artist), what aspect of this interplay between science and art do you find most intriguing?",
            translateText: "啊，欢迎来到这场科学与艺术的精彩对话！今天，我们站在这两个看似不同的领域的交汇处，但我认为它们毕竟不是那么分开的。你看，科学和艺术都试图通过不同的视角来理解宇宙的奥秘。在我的工作中，想象力一直是我最重要的工具——是的，比知识更重要。但是关于我已经说得够多了！我很想听听你的想法。告诉我，作为一名年轻的科学家（或艺术家），你觉得科学与艺术之间相互作用的哪个方面最吸引人？",
            showTranslation: false,
            chatType: 0, //信息类型，0文字，1图片
            uid: "1005", //uid
        },
    ]
)
