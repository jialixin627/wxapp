//app.js
App({
  onLaunch: function (e) {
    console.log('----------我是分割线----------')
    console.log(e.scene)
    this.scene = e.scene
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
  },

    getUserInfo: function(cb) {
      //获取授权用户基本数据
      var that = this;
      if (this.globalData.userInfo) {
        typeof cb == "function" && cb(this.globalData.userInfo)
      } else {
        //调用登录接口
        wx.login({
          success: function (response) {
            var code = response.code;
            wx.getUserInfo({
              success: function (resp) {
                that.globalData.userInfo = resp.userInfo;
                typeof cb == "function" && cb(that.globalData.userInfo);
                wx.setStorageSync('userInfo', resp.userInfo);
                // 向关联网站发送请求，解密、存储数据
                wx.request({
                  url: that.host + 'login/',
                  data: {
                    code: code,
                    // iv: resp.iv,
                    // encryptedData: resp.encryptedData,
                    nickname: resp.userInfo.nickName,
                    avatarUrl: resp.userInfo.avatarUrl
                  },
                  header:
                  {
                    'content-type': 'application/x-www-form-urlencoded'
                  },
                  method: 'POST',
                  success: function (res) {
                    if (res.data) {
                      console.log('---------UserInfo----success------------');
                      console.log('statusaCode:' + res.statusCode);
                      console.log(res.data);
                      wx.setStorageSync('session', res.data.wxapp_session);
                      that.session = res.data.wxapp_session
                    }
                  }
                })
              }
            });
          }
        })
      }
    },

// 登录
// wx.login({
//   success: function (res_login) {
//     // 发送 res.code 到后台换取 openId, sessionKey, unionId
//     console.log(res_login)
//     if (res_login.code) {
//       wx.getUserInfo({
//         success: function (res_user) {
//           console.log(res_user)
//           wx.request({
//             url: that.host + 'api/login/',
//             method: 'POST',
//             header: {
//               'content-type': 'application/x-www-form-urlencoded' // 默认值
//             },
//             data: {
//               code: res_login.code,
//               nickname: res_user.userInfo.nickName,
//               // encryptedData: res_user.encryptedData,
//               // iv: res_user.iv
//             },
//             success: function (res_session) {
//               console.log(res_session)
//               wx.setStorageSync('wxapp_session', res_session.data.wxapp_session)
//             },
//             fail: function () {
//               console.log("启用wx.login登陆失败！");
//             }
//           })
//           // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
//           // 所以此处加入 callback 以防止这种情况
//           if (this.userInfoReadyCallback) {
//             this.userInfoReadyCallback(res)
//           }
//         }
//       })  
//     } else {
//       console.log('获取登陆状态失败！' + res.errMsg)
//     }
//   }
// })
  globalData: {
    userInfo: null,
  },
  host: "http://192.168.2.79:5000/",
  session: null,
  scene: null
})