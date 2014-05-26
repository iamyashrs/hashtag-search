#TODO: WHEN X CREATED AN EVENT
import json
import Queue
import threading
# import urllib3
import requests
import ConfigParser
from requests_oauthlib import OAuth1
from flask import Flask, render_template, request

def get_data(query):
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    def facebook(q,query):
        app_id     = Config.get('Facebook','app_id')
        app_secret = Config.get('Facebook','app_secret')
        fields     = 'object_id,id,from,story,picture,message,type,created_time,name,link,caption,properties,to'
        url        = 'https://graph.facebook.com/search?q='+query+'&type=post&key=value&access_token='+app_id+'|'+app_secret+'&fields='+fields
        result     = requests.get(url)
        # return result
        q[0]       =result

    def twitter(q,query):
        app_key             = Config.get('Twitter','app_key')
        app_secret          = Config.get('Twitter','app_secret')
        access_token        = Config.get('Twitter','access_token') # TODO: Get access token from server.
        access_token_secret = Config.get('Twitter','access_token_secret')
        url                 = 'https://api.twitter.com/1.1/search/tweets.json?q='+query
        auth                = OAuth1(app_key,app_secret,access_token,access_token_secret)
        result              =  requests.get(url,auth=auth)
        # return result
        q[1]                =result

    def instagram(q,query):
        CLIENTID     = Config.get('Instagram','CLIENTID')
        CLIENTSECRET = Config.get('Instagram','CLIENTSECRET')
        REDIRECTURL  = Config.get('Instagram','REDIRECTURL')
        CODE         = Config.get('Instagram','CODE')
        ACCESSTOKEN  = Config.get('Instagram','ACCESSTOKEN') # TODO : Get access token from server.
        query        =query[3:]
        url          = 'https://api.instagram.com/v1/tags/'+query+'/media/recent?access_token='+ACCESSTOKEN
        result       = requests.get(url)
        # return result
        q[2]         =result
    query = '%23'+query
    q = [0,0,0]

    t1 = threading.Thread(target=facebook, args = (q,query))
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=twitter, args = (q,query))
    t2.daemon = True

    t2.start()

    t3 = threading.Thread(target=instagram, args = (q,query))
    t3.daemon = True
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    try :
        fb = q[0].json()
    except:
        fb = {}
    try:
        twitter = q[1].json()
    except:
        twitter = {}
    try:
        ig = q[2].json()
    except:
        ig = {}
    fbdict = []
    instadict = []
    twitdict = []
    for i in fb['data']:
        q={}
        q['id']='https://facebook.com/'+i['id'].replace('_','/posts/')
        if i['type']=='status':
            try:
                q['story']=i['story']
            except:
                q['story']=''
            try:
                q['message']=i['message']
            except:
                q['message']=''
            q['type']='status'
            q['user']=i['from']['name']
            q['userhref']='https://facebook.com/'+i['from']['id']



        elif i['type']=='link':
            try:
                q['story']=i['story']
            except:
                q['story']=''
            try:
                q['message']=i['message']
            except:
                q['message']=''
            try:
                q['name']=i['name']
            except:
                q['name']=''
            try:
                q['link']=i['link']
            except:
                q['link']=''
            try:
                q['description']=i['description']
            except:
                q['description']=''
            q['type']='link'
            q['user']=i['from']['name']
            q['userhref']='https://facebook.com/'+i['from']['id']

        elif i['type']=='photo':
            try:
                q['story']=i['story']
            except:
                q['story']=''
            try:
                q['message']=i['message']
            except:
                q['message']=''
            try:
                q['caption']=i['caption']
            except:
                q['caption']=''
            q['type']='photo'
            q['user']=i['from']['name']
            q['userhref']='https://facebook.com/'+i['from']['id']
            q['picture']=i['picture']

        elif i['type']=='video':
            try:
                q['story']=i['story']
            except:
                q['story']=''
            try:
                q['message']=i['message']
            except:
                q['message']=''
            try:
                q['description']=i['description']
            except:
                q['description']=''
            q['type']='video'
            q['user']=i['from']['name']
            q['userhref']='https://facebook.com/'+i['from']['id']
            q['picture']=i['picture']
        fbdict.append(q)

    try:
        for i in ig['data']:
            q={}
            q['photo']=i['images']['low_resolution']['url']
            try:
                q['caption']=i['caption']
            except:
                q['caption']=''
            q['user']=i['user']['username']
            q['link']=i['link']
            instadict.append(q)
    except:
        pass

    for i in twitter['statuses']:
        q={}
        q['user']=i['user']['screen_name']
        q['text']=i['text']
        q['id']=i['id_str']
        try:
            q['picture']=i['entities']['media'][0]['media_url_https']
        except:
            q['picture']=''
        twitdict.append(q)


    return fbdict, instadict, twitdict
app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('query')
    if query:
        query = ''.join(e for e in query if e.isalnum())
        fbdata,igdata,twdata = get_data(query)
    return render_template('index.html', **locals())

@app.route('/fb/')
def fb():
    fbdata,igdata,twdata = get_data('soccer')
    return render_template('fb.html', **locals())
