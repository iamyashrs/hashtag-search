#TODO: WHEN X CREATED AN EVENT
import json
import Queue
import threading
import requests
import ConfigParser
from requests_oauthlib import OAuth1
from flask import Flask, render_template, request


def get_data(fbs, gps, igs, tws, gns, query):
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    def facebook(q, query):
        app_id = Config.get('Facebook', 'app_id')
        app_secret = Config.get('Facebook', 'app_secret')
        fields = 'object_id,id,from,story,picture,message,type,created_time,name,link,caption,properties,to'
        url = 'https://graph.facebook.com/search?q=' + query + '&type=post&key=value&access_token=' + app_id + '|' + app_secret + '&fields=' + fields
        result = requests.get(url)
        # return result
        q[0] = result

    def twitter(q, query):
        app_key = Config.get('Twitter', 'app_key')
        app_secret = Config.get('Twitter', 'app_secret')
        access_token = Config.get('Twitter', 'access_token')  # TODO: Get access token from server.
        access_token_secret = Config.get('Twitter', 'access_token_secret')
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + query
        auth = OAuth1(app_key, app_secret, access_token, access_token_secret)
        result = requests.get(url, auth=auth)
        # return result
        q[1] = result

    def instagram(q, query):
        CLIENTID = Config.get('Instagram', 'CLIENTID')
        CLIENTSECRET = Config.get('Instagram', 'CLIENTSECRET')
        REDIRECTURL = Config.get('Instagram', 'REDIRECTURL')
        CODE = Config.get('Instagram', 'CODE')
        ACCESSTOKEN = Config.get('Instagram', 'ACCESSTOKEN')  # TODO : Get access token from server.
        query = query[3:]
        url = 'https://api.instagram.com/v1/tags/' + query + '/media/recent?access_token=' + ACCESSTOKEN
        result = requests.get(url)
        # return result
        q[2] = result

    def googleplus(q, query):
        key = Config.get('GOOGLE_PLUS', 'KEY')
        url = 'https://www.googleapis.com/plus/v1/activities?query=' + query + '&key=' + key
        result = requests.get(url)
        # return result
        q[3] = result


    def googlenews(q, query):
        url = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&rsz=8&q=' + query
        result = requests.get(url)
        # return result
        q[4] = result

    query = '%23' + query
    q = [0, 0, 0, 0, 0]

    if fbs:
        t1 = threading.Thread(target=facebook, args=(q, query))
        t1.daemon = True
        t1.start()

    if tws:
        t2 = threading.Thread(target=twitter, args=(q, query))
        t2.daemon = True
        t2.start()

    if igs:
        t3 = threading.Thread(target=instagram, args=(q, query))
        t3.daemon = True
        t3.start()

    if gps:
        t4 = threading.Thread(target=googleplus, args=(q, query))
        t4.daemon = True
        t4.start()

    if gns:
        t5 = threading.Thread(target=googlenews, args=(q, query))
        t5.daemon = True
        t5.start()
    if fbs:
        t1.join()

    if tws:
        t2.join()

    if igs:
        t3.join()

    if gps:
        t4.join()

    if gns:
        t5.join()

    try:
        fb = q[0].json()
    except:
        fb = {'data': []}
    try:
        twitter = q[1].json()
    except:
        twitter = {'statuses': []}
    try:
        ig = q[2].json()
    except:
        ig = {'data': []}
    try:
        gp = q[3].json()
    except:
        gp = {'items': []}
    try:
        gn = q[4].json()
    except:
        gn = {'responseStatus': 0}

    fbdict = []
    instadict = []
    twitdict = []
    gpdict = []
    gndict = []

    for i in fb['data']:
        q = {}
        q['id'] = 'https://facebook.com/' + i['id'].replace('_', '/posts/')
        if i['type'] == 'status':
            try:
                q['story'] = i['story']
            except:
                q['story'] = ''
            try:
                q['message'] = i['message']
            except:
                q['message'] = ''
            q['type'] = 'status'
            q['user'] = i['from']['name']
            q['userhref'] = 'https://facebook.com/' + i['from']['id']



        elif i['type'] == 'link':
            try:
                q['story'] = i['story']
            except:
                q['story'] = ''
            try:
                q['message'] = i['message']
            except:
                q['message'] = ''
            try:
                q['name'] = i['name']
            except:
                q['name'] = ''
            try:
                q['link'] = i['link']
            except:
                q['link'] = ''
            try:
                q['description'] = i['description']
            except:
                q['description'] = ''
            q['type'] = 'link'
            q['user'] = i['from']['name']
            q['userhref'] = 'https://facebook.com/' + i['from']['id']

        elif i['type'] == 'photo':
            try:
                q['story'] = i['story']
            except:
                q['story'] = ''
            try:
                q['message'] = i['message']
            except:
                q['message'] = ''
            try:
                q['caption'] = i['caption']
            except:
                q['caption'] = ''
            q['type'] = 'photo'
            q['user'] = i['from']['name']
            q['userhref'] = 'https://facebook.com/' + i['from']['id']
            q['picture'] = i['picture']

        elif i['type'] == 'video':
            try:
                q['story'] = i['story']
            except:
                q['story'] = ''
            try:
                q['message'] = i['message']
            except:
                q['message'] = ''
            try:
                q['description'] = i['description']
            except:
                q['description'] = ''
            q['type'] = 'video'
            q['user'] = i['from']['name']
            q['userhref'] = 'https://facebook.com/' + i['from']['id']
            q['picture'] = i['picture']
        fbdict.append(q)

    try:
        for i in ig['data']:
            q = {}
            q['photo'] = i['images']['low_resolution']['url']
            try:
                q['caption'] = i['caption']
            except:
                q['caption'] = ''
            q['user'] = i['user']['username']
            q['link'] = i['link']
            instadict.append(q)
    except:
        pass

    for i in twitter['statuses']:
        q = {}
        q['user'] = i['user']['screen_name']
        q['text'] = i['text']
        q['id'] = i['id_str']
        try:
            q['picture'] = i['entities']['media'][0]['media_url_https']
        except:
            q['picture'] = ''
        twitdict.append(q)

    for i in gp['items']:
        q = {}
        q['user'] = i['actor']['displayName']
        q['user_image'] = i['actor']['image']['url']
        q['title'] = i['title']
        q['post_url'] = i['url']
        if 'attachments' in i['object']:
            if i['object']['attachments'][0]['objectType'] == "photo":
                try:
                    q['photo'] = i['object']['attachments'][0]['image']['url']
                except:
                    q['photo'] = ''

            if i['object']['attachments'][0]['objectType'] == "article":
                try:
                    q['url'] = i['object']['attachments'][0]['url']
                    q['text'] = i['object']['attachments'][0]['displayName']
                except:
                    q['url'] = ''

            if i['object']['attachments'][0]['objectType'] == "video":
                try:
                    q['url'] = i['object']['attachments'][0]['url']
                    q['photo'] = i['object']['attachments'][0]['image']['url']
                except:
                    q['photo'] = ''
                    q['url'] = ''
        gpdict.append(q)

    if gn['responseStatus'] == 200:
        for i in gn['responseData']['results']:
            q = {}
            q['publisher'] = i['publisher']
            q['title'] = i['titleNoFormatting']
            q['content'] = i['content']
            q['url'] = i['unescapedUrl']
            q['publishedDate'] = i['publishedDate']
            if 'image' in i:
                try:
                    q['image'] = i['image']['url']
                except:
                    q['image'] = ''

            gndict.append(q)

    return fbdict, instadict, twitdict, gpdict, gndict


def get_trending():
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    app_id = Config.get('Yahoo', 'app_id')

    ip = request.remote_addr
    url = "http://freegeoip.net/json/" + ip
    result = requests.get(url)

    results = result.json()
    area = results['country_name']

    if not app_id:
        raise NotImplementedError('WOEID App Id is empty.')
    if area == 'Reserved':
        area = 'Delhi'

    url = 'http://where.yahooapis.com/v1/places.q(%s)?appid=%s&format=json' % (area, app_id)

    r = requests.get(url)
    json = r.json()
    places = json['places']
    place = places['place'][0]

    if place:
        woeid = place['woeid']
        name = place['name']
    else:
        woeid = 1

    app_key = Config.get('Twitter', 'app_key')
    app_secret = Config.get('Twitter', 'app_secret')
    access_token = Config.get('Twitter', 'access_token')
    access_token_secret = Config.get('Twitter', 'access_token_secret')
    url = 'https://api.twitter.com/1.1/trends/place.json?id=' + str(woeid)
    auth = OAuth1(app_key, app_secret, access_token, access_token_secret)
    result = requests.get(url, auth=auth)
    results = result.json()
    trends = []
    for i in results[0]['trends']:
        q = {}
        q['query'] = i['query']
        q['name'] = i['name']
        trends.append(q)

    return trends


app = Flask(__name__)


@app.route('/')
def index():
    query = request.args.get('query')
    fb = request.args.get('fb')
    gp = request.args.get('gp')
    ig = request.args.get('ig')
    tw = request.args.get('tw')
    gn = request.args.get('gn')
    total = sum(1 for e in [fb, gp, ig, tw, gn] if e)
    if not gn:
        if total == 4:
            col = 3;
            totalcol = "12"
        elif total == 3:
            col = 4;
            totalcol = "12"
        elif total == 2:
            col = 6;
            totalcol = "8 col-md-offset-2"
        elif total == 1:
            col = 12;
            totalcol = "4 col-md-offset-4"
    else:
        if total == 5:
            col = 3;
            totalcol = "10";
            ncol = 2
        elif total == 4:
            col = 4;
            totalcol = "9";
            ncol = 3
        elif total == 3:
            col = 6;
            totalcol = "8";
            ncol = 4
        elif total == 2:
            col = 12;
            totalcol = "4 col-md-offset-2";
            ncol = 4
        elif total == 1:
            col = 4;
            totalcol = "8";
            ncol = '4 col-md-offset-4'
    if query:
        query = ''.join(e for e in query if e.isalnum())
        fbdata, igdata, twdata, gpdata, gndata = get_data(fb, gp, ig, tw, gn, query)
    if query is None: trends = get_trending()
    return render_template('index.html', **locals())


@app.route('/fb/')
def fb():
    fbdata, igdata, twdata = get_data('soccer')
    return render_template('fb.html', **locals())


app.run(debug=True)
