const api = require("../../utils/api.js");
const util = require('../../utils/util.js');

const addHours = util.addHours;
const app = getApp()

Page({
  data: {
    optionList: [
      { icon: '' },
      { icon: '' }
    ],
    showAddBtn: 1,
    date: addHours(new Date(), 4)[0],
    time: addHours(new Date(), 4)[1],
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
      } else {
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
    const self = this;
    this.setData({
        showTopTips: true
    });
    setTimeout(function(){
        self.setData({
          showTopTips: false
        });
    }, 3000);
  },
  bindVoteTypeChange (e){
      this.setData({
        voteTypeIndex: e.detail.value
      })
  },
  bindTimeChange (e) {
      this.setData({
        time: e.detail.value
      })
  },
  bindDateChange (e) {
      this.setData({
        date: e.detail.value
      })
  },
  recordValue (e){
    let _optionList = this.data.optionList;
    let _index = e.target.dataset.index;
    let value = e.detail.value;
    _optionList[_index].value = value;
    this.setData({optionList: _optionList});

  },
  addOption (e){
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
  delOption (e){
      let _index = e.target.dataset.index;
      let _optionList = this.data.optionList;
      _optionList.splice(_index, 1);
      this.setData({optionList: _optionList});
      // 更新投票选项
      this.updateVoteType();
  },
  chooseImage (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], 
      sourceType: ['album', 'camera'], 
      count: 1, 
      success (res) {
        // 返回选定照片的本地文件路径列表
        that.setData({
          files: that.data.files.concat(res.tempFilePaths)
        });
      }
    })
  },
  previewImage (e) {
      wx.previewImage({
        current: e.currentTarget.id, // 当前显示图片的http链接
        urls: this.data.files // 需要预览的图片http链接列表
      })
  },
  formSubmit (e) {
    console.log(`submit data：${e.detail.value}`)
    const data = e.detail.value;
    console.log('submit data: ', data)
    api.create({
      data,
      success (res) {
        console.log(res)
        if (res.data.status == 200) {
          wx.navigateTo({
            url: `../vote/vote?pk=${res.data.pk}`,
          })
        } else {
          wx.navigateTo({
            url: '../login/login',
          })
        }
      }
    })
  }
});
