const api = require("../../utils/api.js");
const app = getApp();
Page({
  data: {
    logged: !1,
    iv: '',
    encryptedData: '',
    logo: '/images/common/logo.jpg',
    weixin_logo: '/images/common/weixin.png'
  },
  onLoad() {},
  onShow() {
    const token = wx.getStorageSync('token')
    this.setData({
      logged: token
    })
    token && setTimeout(this.goIndex, 1000)
  },
  login() {
    console.log('a')
    this.signIn(this.goIndex)
  },
  goIndex() {
    wx.switchTab({
      url: '/pages/index/index'
    })
  },
  signIn() {
    let that =this;
    if (wx.getStorageSync('token')) return
    wx.login({
      success(res){
        wx.getUserInfo({
          success(resp) {
            that.setData({
              iv: resp.iv,
              encryptedData: resp.encryptedData
            })
            setTimeout(function() {
              let data = {
                code: res.code,
                iv: that.data.iv,
                encryptedData: that.data.encryptedData
              }
              console.log(data)
              api.signIn({
                data,
                success(res) {
                  console.log('登陆成功！')
                  wx.setStorageSync('token', res.data.token)
                }
              })
            }, 1000)
          }
        });
      }
    })
    that.goIndex()
  },
})
