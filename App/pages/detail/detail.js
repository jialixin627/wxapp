//detail.js
//获取应用实例
const api = require("../../utils/api.js");
const app = getApp()
Page({
  data: {
    detailImg: '/images/common/vote.jpeg',
    checkboxMax: 2,
    progress: 0,
    disabled: false,
    result:{},
    scene: app.scene
  },
  onLoad: function (data) {
    const self = this;
    api.getResult({data,
      success: function (res) {
        console.log('_____b______')
        console.log(res.data)
        self.setData({ result: res.data })
      }
    })
    // wx.request({
    //   url: `${app.host}result/`,
    //   method: 'POST',
    //   data: data,
    //   header:{
    //     'content-type': 'application/x-www-form-urlencoded',
    //   },
      // success: function(res){
      //   // console.log('_____a______')
      //   console.log(res.data)
      //   that.setData({result: res.data})
      // }
    // })
  },
  radioChange: function (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value);
    var radioItems = this.data.radioItems;
    for (var i = 0, len = radioItems.length; i < len; ++i) {
        radioItems[i].checked = radioItems[i].value == e.detail.value;
    }
    this.setData({
        radioItems: radioItems
    });
  },
    checkboxChange: function (e) {
      console.log('checkbox发生change事件，携带value值为：', e.detail.value);
      let checkboxItems = this.data.checkboxItems;
      let checkboxMax = this.data.checkboxMax;
      let values = e.detail.value;

        if ( checkboxMax < values.length  ) {
          values = values.splice(0, checkboxMax);
          console.log(values)

          for ( let j = 0; j <  checkboxItems.length; j++) {
            checkboxItems[j].checked = false;

            for (let i = 0; i < values.length; i++){
                if ( checkboxItems[j].value ==  values[i]) {
                    checkboxItems[j].checked = true;
                }
            }
          }
          console.log(checkboxItems)
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
    upload: function(){
        if(this.data.disabled) return;
        this.setData({
            progress: 0,
            disabled: true
        });
        _next.call(this);
    },
    onShareAppMessage: function(e){
      console.log('abc')
      console.log(e)
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
