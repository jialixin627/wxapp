const api = require("../../utils/api.js");
const util = require('../../utils/util.js');

const formatTime = util.formatTime;
const app = getApp()
const sliderWidth = 100;
Page({
  data: {
    url: 'detail/detail',
    weui_icon: '/images/common/weui.png',
    vote_list:{},
    join_list: {},
    tabs: ["我创建的", "我参与的"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0
  },
  onLoad(options) {
    const self = this;
    wx.getSystemInfo({
      success(res) {
        self.setData({
          sliderLeft: (res.windowWidth / self.data.tabs.length - sliderWidth) / 2,
          sliderOffset: res.windowWidth / self.data.tabs.length * self.data.activeIndex
        });
      }
    });

    api.getVoteList({
      success(res) {
        console.log(res)
        self.setData({ vote_list: res.data })
        self.join()
      },
      fail() {
        console.log("获取列表失败！")
      }
    })
  },
  redirectTo(e) {
    console.log(e)
    var pk = e.currentTarget.dataset.pk;
    wx.navigateTo({
      url: `../detail/detail?pk=${pk}`,
    })
  },
  tabClick(e) {
    this.setData({
      sliderOffset: e.currentTarget.offsetLeft,
      activeIndex: e.currentTarget.id
    });
  },
  join(){
    const self = this;
    api.join({
      success(res){
        console.log('加载成功！')
        self.setData({ join_list: res.data })
      }
    })
  }
})
