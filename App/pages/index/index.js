//index.js
//获取应用实例
const api = require("../../utils/api.js");
const app = getApp()
const sliderWidth = 100;
Page({
  data: {
    url: 'detail/detail',
    weui_icon: '/images/common/weui.png',
    vote_list:{},
    tabs: ["我创建的", "我参与的"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0
  },
  onLoad(options) {
    const self = this;
    wx.showToast({
      title: '正在加载',
      icon: 'loading',
      duration: 10000,
    });

    wx.getSystemInfo({
      success(res) {
        self.setData({
          sliderLeft: (res.windowWidth / self.data.tabs.length - sliderWidth) / 2,
          sliderOffset: res.windowWidth / self.data.tabs.length * self.data.activeIndex
        });
      }
    });
    wx.getStorage({
      key: 'session',
      success(res) {
        console.log(res.data)
        wx.request({
          url: `${app.host}vote-list/`,
          data: { 'wxapp_session': res.data },
          method: 'POST',
          header: {
            'content-type': 'application/x-www-form-urlencoded' // 默认值
          },
          success(res) {
            console.log('test------')
            console.log(app.session)
            console.log(res)
            self.setData({vote_list: res.data})
          },
          fail:() => {
            console.log("获取列表失败！")
          }
        })
      },
      fail: function() {
        app.getUserInfo(function (userInfo) {
          console.log('登陆成功-----')
          console.log(userInfo)
          self.setData({
            userInfo: userInfo,
          })
        });

        setTimeout(function () {
          wx.request({
            url: `${app.host}vote-list/`,
            data: { 'wxapp_session': wx.getStorageSync('session')},
            method: 'POST',
            header: {
              'content-type': 'application/x-www-form-urlencoded' // 默认值
            },
            success(res) {
              console.log('test------timeout')
              console.log(app.session)
              console.log(res)
              self.setData({ vote_list: res.data })
            }
          })
        }, 1000);
      }
    })
    wx.hideToast();
  },
  onReady: function(){

  },
  onShow: function() {
  },
  redirectTo(e) {
    console.log(e)
    var pk = e.currentTarget.dataset.pk;
    wx.navigateTo({
      url: "../detail/detail?pk=" + pk,
    })
  },
  tabClick(e) {
    this.setData({
      sliderOffset: e.currentTarget.offsetLeft,
      activeIndex: e.currentTarget.id
    });
  }
})
