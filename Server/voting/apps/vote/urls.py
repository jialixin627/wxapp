from django.conf.urls import patterns, url

urlpatterns = patterns('voting.apps.vote.views',
    url(r'^$', 'index', name='index'),
    url(r'^login/$', 'login', name='login'),
    url(r'^vote-list/$', 'vote_list', name='vote_list'),
    url(r'^subjects/$', 'subjects', name='subjects'),
    url(r'^voting-result-(?P<id>\d+)/$', 'voting_result', name='voting-result'),
    url(r'^vote-page-(?P<id>\d+)/$', 'vote_page', name='vote-page'),
    url(r'^result/$', 'result', name='result'),
    url(r'^get-vote-info/$', 'get_vote_info', name='get-vote-info'),
    url(r'^vote-submit/$', 'vote_submit', name='vote-submit'),
    url(r'^create/$', 'create', name='create'),
    url(r'^join/$', 'vote_list_join', name='join'),
    url(r'^signin/$', 'signin', name='signin'),
)
