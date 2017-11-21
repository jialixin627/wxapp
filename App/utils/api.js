const apiURL = "http://192.168.2.79:5000";

const wxRequest = (params, url) => {
  wx.request({
    url,
    method: params.method || 'POST',
    data: params.data || {},
    header: {
      // Accept: 'application/json',
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

const create = (params) => {
  wxRequest(params, `${apiURL}/create/`);
};
const getVoteList = (params) => {
  wxRequest(params, `${apiURL}/vote-list/`);
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
// const getUsers = (params) => {
//   wxRequest(params, `${apiURL}/users`);
// };
// const getUserInfoById = (params) => {
//   wxRequest({ success: params.success }, `${apiURL}/user/${params.data.userId}`);
// };
// const getHotByWeekly = (params) => {
//   wxRequest(params, `${apiURL}/hot/weekly`);
// };
// const getHotByMonthly = (params) => {
//   wxRequest(params, `${apiURL}/hot/monthly`);
// };

module.exports = {
  create,
  getResult,
  getVoteList,
  voteSubmit,
  getVoteInfo,
  // getTopicByName,
  // getUsers,
  // getUserInfoById,
  // getHotByWeekly,
  // getHotByMonthly,
  // getLiveInfoById
};
