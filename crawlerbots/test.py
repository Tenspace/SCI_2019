# from proxycrawl.proxycrawl_api import ProxyCrawlAPI
# # import json
# # # api = ProxyCrawlAPI('https://www.facebook.com/100005187035294')
# #
# # api = ProxyCrawlAPI({ 'token': 'V8yqvfz3rVcOzNXVW5NuOA' })
# # response = api.get('https://www.reddit.com/r/pics/comments/5bx4bx/thanks_obama/', {
# #     'user_agent': 'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/30.0',
# #     'format': 'json'
# # })
# # print(response['status_code'])
# # if response['status_code'] == 200:
# #     print(response['body'])
# #
# # # response = api.post('https://producthunt.com/search', { 'text': 'example search' })
# # # print(response['status_code'])
# # # if response['status_code'] == 200:
# # #     print(response['body'])
# # #
# # # response = api.post('https://httpbin.org/post', json.dumps({ 'some_json': 'with some value' }), { 'post_content_type': 'json' })
# # # print(response['status_code'])
# # # if response['status_code'] == 200:
# # #     print(response['body'])
# # #
# # api = ProxyCrawlAPI({ 'token': 'QHGge_q4KCmXtRvXqmQeMQ' })
# # response = api.get('https://www.nfl.com')
# # print(response['status_code'])
# # if response['status_code'] == 200:
# #     print(response['body'])
# #
# # response = api.get('https://www.freelancer.com', { 'page_wait': 5000 })
# # print(response['status_code'])
# # if response['status_code'] == 200:
# #     print(response['body'])
# a = 'aa bb cc'
# b = a[-2:]
# print(b)
# import datetime
#
# s = '2019년 1월 10일 오전 11:08'.replace('년', '-').replace('월', '-').replace("일", '').replace('오전', 'AM').replace('오후', 'PM').replace(' ', '')
# dt = datetime.datetime.strptime(s, '%Y-%m-%d%p%I:%M')
# try:
#     print(dt.strftime('%Y-%m-%d%I:%M%s'))
# except Exception:
#     print('?')
# a=[1,2,3,4]
# print(len(a))
# a = 'a'
# if '시간' or '분' in a:
#     print('pp')
# from datetime import datetime
#
# now=datetime.now()
# print(now.day-1)
# b = '1월 9일'
# c='2019년'+b
# print(c)
# a = '2017-08-01'
# b = '2018-08-01'
# post_date2 = '2016-07-01'

import re
# user = 'https://www.facebook.com/profile.php?id=100005123796303&hc_location=friend_browser'
# p = re.findall('=\w+&', user)
# ida = p[0].replace('=', '').replace('&', '')
#
# print(ida)
#
# user = 'https://www.facebook.com/qmfforwnahd'
# p = re.findall('\/\w+\s', user)
# print(p)
# ida = p[0].replace('/', '')
#
# print(ida)

# user_page_id = ['profile.php?v=info&lst=100003275046658%3A100006691393038%3A1550719683&id=100006691393038&refid=17']
# id_list = []
# for page_id in user_page_id:
#     id_list.append(page_id[0])
#
# p = re.findall('%\w+%', id_list[0])
# print(p)
# data='''{"hq-profile-logging": {"profile_id": 100015608505556, "profile_high_quality_metric": "action_bar_friend",
#                                 "profile_session_token": "100006841668710:100015608505556:1550720931",
#                                 "profile_surface_type": "action_bar", "profile_event_type": "click"}}'''
# print(data)
# data = dict(data)
# print(data.get('hq-profile-logging').get('profile_id'))
idx = 14301
if idx > 11301 and idx < 14301:
    print(idx)