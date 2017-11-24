const api = require("../../utils/api.js");
const app = getApp();
Page({
  data: {
    logged: !1,
    index: '',
    iv: '',
    encryptedData: '',
    logo: '/images/common/logo.jpg',
    weixin_logo: '/images/common/weixin.png'
  },
  onLoad(query) {
    console.log()
    const token = wx.getStorageSync('token')
    this.setData({
      logged: token,
      pk: query.pk
    })
    token && setTimeout(this.signIn, 1000)
  },
  goIndex() {
    let self = this;
    if (self.data.pk) {
      wx.redirectTo({
        url: `../vote/vote?pk=${self.data.pk}`
      })
    } else {
      wx.switchTab({
        url: '/pages/index/index'
      })
    }
  },
  login() {
    const that = this;
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
              api.login({
                data,
                success(res) {
                  // console.log('登陆成功！', res)
                  wx.setStorageSync('token', res.data.token)
                  that.goIndex()
                }
              })
            }, 1000)
          }
        });
      }
    })
  },
  signIn(){
    const self = this;
    api.signIn({
      success(res){
        if (res.data.resNo == 400){
          console.log(res.data.status)
          wx.removeStorageSync('token')
          self.login(self.goIndex)
        } else {
          self.goIndex()
        }
      }
    })
  }
})
