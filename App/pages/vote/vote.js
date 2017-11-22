const api = require("../../utils/api.js");
const app = getApp()
Page({
  data: {},
  voteInfo: {},
  radioItems: [],
  onLoad: function (data) {
    var self = this;
    console.log(data);
    var data = {'pk': 2};
    api.getVoteInfo({
      data,
      success(res) {
        console.log(res.data)
        self.setData({ voteInfo: res.data })
        self.setData({ radioItems: res.data.choices_data })
      }
    })
  },

  /**
   * 用户点击右上角分享
   */
  // onShareAppMessage: function () {
  
  // },
  radioChange: function (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value);
    const radioItems = this.data.radioItems;
    for (var i = 0, len = radioItems.length; i < len; ++i) {
      radioItems[i]['checked'] = radioItems[i].pk == e.detail.value;
    }
    console.log(radioItems);
    this.setData({
      radioItems: radioItems
    });
  },
  formSubmit (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
    var data = e.detail.value;
    api.voteSubmit({
      data,
      success: function (res) {
        console.log(res)
        if (res.data.status == 200) {
          wx.redirectTo({
            url: `../detail/detail?pk=${res.data.pk}`,
          })
        }
      }
    })
    // wx.request({
    //   url: app.host + "vote-submit/",
    //   data: formData,
    //   method: "POST",
    //   header: {
    //     'content-type': 'application/x-www-form-urlencoded', // 默认值
    //     'session': wx.getStorageSync('wxapp_session')
    //   },
    //   success: function (res) {
    //     console.log(res)
    //     if (res.data.status==200) {
    //       wx.redirectTo({
    //         url: "../detail/detail?pk=" + res.data.pk,
    //       })
    //     }
    //   }
    // })
  }
})