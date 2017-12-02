const api = require("../../utils/api.js");
const app = getApp()
Page({
  data: {
    disabled: true,
  },
  voteInfo: {},
  radioItems: [],
  onLoad (data) {
    let self = this;
    console.log(data);
    api.getVoteInfo({
      data,
      success(res) {
        console.log(res.data)
        if (res.data.resNo == 400){
          wx.navigateTo({
            url: `../login/login?pk=${data.pk}`
          })
        } else{
          self.setData({
            voteInfo: res.data,
            radioItems: res.data.choices_data
          })
        }
      }
    })
  },
  radioChange (e) {
    const self = this;
    console.log('radio发生change事件，携带value值为：', e.detail.value);
    const radioItems = self.data.radioItems;
    for (let i = 0, len = radioItems.length; i < len; ++i) {
      radioItems[i]['checked'] = radioItems[i].pk == e.detail.value;
    }
    // console.log(radioItems);
    self.setData({
      radioItems: radioItems,
      disabled: false
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
  }
})
