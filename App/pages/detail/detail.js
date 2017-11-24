const api = require("../../utils/api.js");
const app = getApp()
Page({
  data: {
    detailImg: '/images/common/vote.jpeg',
    checkboxMax: 2,
    progress: 0,
    disabled: false,
    result: {},
    scene: app.scene
  },
  onLoad: function (data) {
    const self = this;
    api.getVoteInfo({
      data,
      success (res) {
        console.log(res.data)
        self.setData({ result: res.data })
      }
    })
  },
  radioChange (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value);
    const self = this;
    const radioItems = self.data.radioItems;
    for (var i = 0, len = radioItems.length; i < len; ++i) {
        radioItems[i].checked = radioItems[i].value == e.detail.value;
    }
    self.setData({
        radioItems: radioItems
    });
  },
  checkboxChange (e) {
    const checkboxItems = this.data.checkboxItems;
    const checkboxMax = this.data.checkboxMax;
    let values = e.detail.value;

    if ( checkboxMax < values.length  ) {
      values = values.splice(0, checkboxMax);

      for ( let j = 0; j <  checkboxItems.length; j++) {
        checkboxItems[j].checked = false;

        for (let i = 0; i < values.length; i++){
          if ( checkboxItems[j].value ==  values[i]) {
            checkboxItems[j].checked = true;
          }
        }
      }
      // console.log(checkboxItems)
      }else {
        for (var i = 0, lenI = checkboxItems.length; i < lenI; ++i) {
          checkboxItems[i].checked = false;

          for (var j = 0, lenJ = values.length; j < lenJ; ++j) {

            if(checkboxItems[i].value == values[j]){
              checkboxItems[i].checked = true;
              break;
            }
          }
        }
      }
      this.setData({
          checkboxItems: checkboxItems
      });
  },
  upload () {
      if(this.data.disabled) return;
      this.setData({
        progress: 0,
        disabled: true
      });
      _next.call(this);
  },
  onShareAppMessage(e){
    const pk = e.target.dataset.pk;
    const self = this;
    if (e.from === 'button') {
      console.log(e.target)
    }
    return {
      title: `${self.data.result.name}邀你参与群投票`,
      path: `pages/vote/vote?pk=${pk}`,
      success: function (res) {
        console.log('分享成功')
      },
      fail: function (res) {
        console.log('分享失败！')
      }
    }
  }
})
