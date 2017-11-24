const apiURL = "http://192.168.2.79:5000";
// const apiURL = "http://192.168.31.109:5000";

const setHeaders = () => {
  return {
    // 'Accept': 'application/json', 
    'Content-Type': 'application/x-www-form-urlencoded', 
    'Authorization': wx.getStorageSync('token'),
  }
}

const wxRequest = (params, url) => {
  wx.request({
    url,
    method: params.method || 'POST',
    data: params.data || {},
    header: setHeaders(),
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

const login = (params) => {
  wxRequest(params, `${apiURL}/login/`);
};
const signIn = (params) => {
  wxRequest(params, `${apiURL}/signin/`);
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
const getVoteInfo = (params) => {
  wxRequest(params, `${apiURL}/get-vote-info/`);
};


module.exports = {
  join,
  login,
  signIn,
  create,
  getVoteList,
  voteSubmit,
  getVoteInfo,
};
