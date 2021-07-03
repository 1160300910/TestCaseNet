//store.js
export const store = {
    data: {
        userName: '',
        userId: "",
        work: ""
    },
    // 设置属性
    state: {
        isLogin: false,
    },
    //获取登录状态
    getLoginState() {
        return this.state.isLogin
    },
    //保存登录状态
    userStatus(state, flag) {
        state.isLogin = flag
    },
    //修改登录状态为true
    userLogin(flag) {
        this.state.isLogin = flag
    },
    setUserData(id, name, work) {
        this.data.userId = id
        this.data.userName = name
        this.data.work = work
            //console.log("setUserData", this.data)
    },
    getUserData() {
        //console.log("getdata", this.data)
        return this.data
    },
    setUserId(id) {
        this.data.userId = id
    },
    getUserId() {
        return this.data.userId
    },
    setUserName(name) {
        this.data.userName = name
    },
    getUserName() {
        return this.data.userName
    },
    setWork(work) {
        this.data.work = work
    },
    getWork() {
        return this.data.work
    }
}