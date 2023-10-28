# MIT License

# Copyright (c) 2023 Takayuki Ito

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# simple agent for discourse

import requests,time

#投稿する
def create_post(title, body, category_id):
    api_url = discourse_url + "posts.json/" 
    theData = {
        'title': title,
        'raw' :body,
        'category': category_id,
    }
    theHeaders = {
        'Api-Key': Api_Key,
        'Api-Username': Api_Username
    }
    res = requests.post(api_url, theData, headers=theHeaders)
    res = res.json()
    return res

#投稿する
def create_post_in_topic(body, topic_id):#postする　category_idやtitleは必要ない どのtopicの何番の返信かをbodyと一緒に渡すのみ
    api_url = discourse_url + "posts.json/"
    theData = {
        'raw' :body,
        'topic_id' : topic_id
    }
    theHeaders = {
        'Api-Key': Api_Key,
        'Api-Username': Api_Username
    }
    res = requests.post(api_url, theData, headers=theHeaders)
    res = res.json()
    while "error" in res.keys():
        if res['error_type'] == 'rate_limit':
            print("rate_limit, wait 180 sec")
            time.sleep(120)
            res = requests.post(api_url, theData, headers=theHeaders)
            res = res.json()
            print("create_post: ", res) 
    return res

#返信する
def create_reply(body, topic_id, reply_to_post_number):#replyする　category_idやtitleは必要ない どのtopicの何番の返信かをbodyと一緒に渡すのみ
    api_url = discourse_url + "posts.json/"
    print('create_post:'+'body='+body)
    theData = {
        'raw' :body,
        'topic_id' : topic_id,
        'reply_to_post_number' : reply_to_post_number
    }
    theHeaders = {
        'Api-Key': Api_Key,
        'Api-Username': Api_Username
    }
    res = requests.post(api_url, theData, headers=theHeaders)
    res = res.json()
    print("create_post: ", res)#レスポンスコードを表示する.
    while "error" in res.keys():
        if res['error_type'] == 'rate_limit':
            print("rate_limit, wait 180 sec")
            time.sleep(120)
            res = requests.post(api_url, theData, headers=theHeaders)
            res = res.json()
    return res

def get_posts():
    api_url = discourse_url + "posts.json/"
    res = requests.get(api_url)
    #print(res)
    res = res.json()
    #print(res)
    return res

# あるtopicの全てのポストを得る
def get_posts_in_topic(topic_id):
    api_url = discourse_url + f"/t/-/{topic_id}.json"
    #print(api_url)
    res = requests.get(api_url)
    res = res.json()
    initial_20_posts_in_a_topic  = res['post_stream']['posts'] #最初の20ポストの中身のみ
    post_ids_list_in_a_topic = res['post_stream']['stream']
    posts_in_a_topic = initial_20_posts_in_a_topic # []でもいい？
    # get a post
    i = 0
    for a_post_id in post_ids_list_in_a_topic:
        i = i + 1
        if i > 20:
            time.sleep(3) # 待たないとレートリミットになる
            api_url = discourse_url + f"posts/{a_post_id}.json"
            #print(api_url)
            res = requests.get(api_url)
            #print('*************************')
            #pprint.pprint(res)
            res = res.json()
            posts_in_a_topic.append(res)
    #posts_in_a_topic = list(filter(lambda a_post: a_post['topic_id'] == topic_id,posts))
    return posts_in_a_topic 

def get_post_ids_in_a_topic(topic_id):
    api_url = discourse_url + f"/t/-/{topic_id}.json"
    #print(api_url)
    res = requests.get(api_url)
    res = res.json()
    post_ids_in_a_topic = res['post_stream']['stream']
    return post_ids_in_a_topic

def get_all_messages(posts_dict):
    all_messages = []
    for a_post_id in posts_dict.keys():
        a_post = posts_dict[a_post_id]
        a_message = a_post['cooked']
        all_messages.append(a_message)
    return all_messages

def get_all_messages_without_the_user(posts_dict,the_user):
    all_messages = []
    for a_post_id in posts_dict.keys():
        a_post = posts_dict[a_post_id]
        a_message = a_post['cooked']
        if a_post['username'] != the_user:
            all_messages.append(a_message)
    return all_messages        

def get_recent_post_in_topic(topic_id): 
    api_url = discourse_url + f"/t/-/{topic_id}.json"
    res = requests.get(api_url)
    res = res.json()
    post_ids_list_in_a_topic = list(res['post_stream']['stream'])
    recent_post_id = post_ids_list_in_a_topic[-1]
    return get_a_post(recent_post_id)

def get_a_post(post_id):
    api_url = discourse_url + f"posts/{post_id}.json"
    res = requests.get(api_url)
    res = res.json()
    return res

def get_topic(topic_id):
    api_url = discourse_url + f"t/{topic_id}.json/"
    res = requests.get(api_url)
    res = res.json()
    return res

def get_all_categories():
    api_url = discourse_url + "categories.json/"
    res = requests.get(api_url)
    res = res.json()
    return res

def show_category(id):
    api_url = discourse_url + f"c/{id}/show.json"
    res = requests.get(api_url)
    res = res.json()
    return res

def get_latest_posts(topic_id, count=10):
    api_url = discourse_url + f"/t/-/{topic_id}.json"
    res = requests.get(api_url)
    res = res.json()
    post_ids_list_in_a_topic = list(res['post_stream']['stream'])
    
    recent_posts = []
    for post_id in reversed(post_ids_list_in_a_topic):  # 最新の投稿から順次処理
        post_detail = get_a_post(post_id)
        if not post_detail.get('user_deleted', False):  # user_deletedがfalseの場合
            recent_posts.append(post_detail)
        
        if len(recent_posts) == count:  # countに到達したら終了
            break

    recent_posts.reverse()
    return recent_posts

def format_posts(posts):
    formatted_strings = []
    for idx, post in enumerate(posts, start=1):
        formatted_strings.append(f"----\n{post['raw']}\n")
    return "\n".join(formatted_strings)

