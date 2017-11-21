const api = require("../../utils/api.js");
const app = getApp()
const date = new Date();
Page({
    data: {
      optionList: [
        { icon: '' },
        { icon: '' }
      ],
      showAddBtn: 1,
      date: `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`,
      time: `${date.getHours()+2}:${date.getMinutes()}`,
      voteType: ['单选'],
      // voteType: ['单选', '多选，最多2项', '多选，无限制'],
      voteTypeIndex: 0,
      totalForms: 2,
      files: []
    },
    updateVoteType: function (){
      let _optionList = this.data.optionList;
      let _voteType = this.data.voteType;
      _voteType = [];
      _optionList.map(function (obj, i) {
        if (i === 0){
          _voteType.push('单选');
        }else {
          _voteType.push('多选，最多'+ (i + 1) +'项');
        }
        console.log(i)
        console.log(_voteType)
        })
        _voteType.push('多选，无限制');
        this.setData({voteType: _voteType});
        console.log(111)
    },
    showTopTips: function(){
      var that = this;
      this.setData({
          showTopTips: true
      });
      setTimeout(function(){
          that.setData({
            showTopTips: false
          });
      }, 3000);
    },
    bindVoteTypeChange: function (e){
        this.setData({
          voteTypeIndex: e.detail.value
        })
    },
    bindTimeChange: function (e) {
        this.setData({
          time: e.detail.value
        })
    },
    bindDateChange: function (e) {
        this.setData({
          date: e.detail.value
        })
    },
    recordValue: function (e){
      let _optionList = this.data.optionList;
      let _index = e.target.dataset.index;
      let value = e.detail.value;
      _optionList[_index].value = value;
      this.setData({optionList: _optionList});

    },
    addOption: function (e){
      let _optionList = this.data.optionList;
      _optionList.push({icon: '/images/common/5.png'})
      this.setData({optionList: _optionList});
      this.setData({totalForms: this.data.optionList.length})
      // 选项大于15个后移除添加按钮
      if(_optionList.length >= 15) {
        this.setData({showAddBtn: 0});
      }
      // 更新投票选项
      this.updateVoteType();
    },
    delOption: function (e){
        let _index = e.target.dataset.index;
        let _optionList = this.data.optionList;
        _optionList.splice(_index, 1);
        this.setData({optionList: _optionList});
        // 更新投票选项
        this.updateVoteType();
    },
    chooseImage: function (e) {
      var that = this;
      wx.chooseImage({
        sizeType: ['original', 'compressed'], 
        sourceType: ['album', 'camera'], 
        count: 1, 
        success: function (res) {
          // 返回选定照片的本地文件路径列表
          that.setData({
            files: that.data.files.concat(res.tempFilePaths)
          });
        }
      })
    },
    previewImage: function(e){
        wx.previewImage({
          current: e.currentTarget.id, // 当前显示图片的http链接
          urls: this.data.files // 需要预览的图片http链接列表
        })
    },
    formSubmit: function (e) {
      console.log('submit，data：', e.detail.value)
      var formData = e.detail.value;
      wx.request({
        url: `${app.host}create/`,
        data: formData,
        method: "POST",
        header: {
          'content-type': 'application/x-www-form-urlencoded', // 默认值
          'session': wx.getStorageSync('wxapp_session')
        },
        success: function (res) {
          console.log(res)
          if (res.data.status==200) {
            wx.redirectTo({
              url: `../publish/publish?pk=${res.data.pk}`,
            })
          }
        }
      })
    }
});
