// const apiURL = "http://192.168.2.79:5000";
const apiURL = "http://192.168.31.109:5000";
const token = wx.getStorageSync('token');

const wxRequest = (params, url) => {
  wx.request({
    url,
    method: params.method || 'POST',
    data: params.data || {},
    header: {
      'Authorization': `JWT ${token}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    success(res) {
      if (params.success) {
        params.success(res);
      }
    },
    fail(res) {
      if (params.fail) {
        params.fail(res);
      }
    },
    complete(res) {
      if (params.complete) {
        params.complete(res);
      }
    },
  });
};

const signIn = (params) => {
  wxRequest(params, `${apiURL}/login/`);
};
const create = (params) => {
  wxRequest(params, `${apiURL}/create/`);
};
const getVoteList = (params) => {
  wxRequest(params, `${apiURL}/vote-list/`);
};
const join = (params) => {
  wxRequest(params, `${apiURL}/join/`);
};
const voteSubmit = (params) => {
  wxRequest(params, `${apiURL}/vote-submit/`);
};
// const getVoteInfo = (params) => {
//   wxRequest({ success: params.success }, `${apiURL}/live/${params.data.id}`);
// };
const getVoteInfo = (params) => {
  wxRequest(params, `${apiURL}/get-vote-info/`);
};
const getResult = (params) => {
  wxRequest(params, `${apiURL}/result/`);
};


module.exports = {
  join,
  signIn,
  create,
  getResult,
  getVoteList,
  voteSubmit,
  getVoteInfo,
};
