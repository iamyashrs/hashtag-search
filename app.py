import Queue
import threading
import requests
from requests_oauthlib import OAuth1

def facebook(q,query):
	app_id='APP_ID'
	app_secret='APP_SECRET'
	fields = 'id,from,story,picture,message,type,created_time,name,link,caption,properties,to'
	url = 'https://graph.facebook.com/search?q='+query+'&type=post&key=value&access_token='+app_id+'|'+app_secret+'&fields='+fields
	result = requests.get(url)
	# print result.text
	# return result
	q[0]=result

def twitter(q,query):
	app_key = 'APP_KEY'
	app_secret = 'APP_SECRET'
	access_token = 'ACCESS_TOKEN' # TODO: Get access token from server.
	access_token_secret = 'ACCESS_TOKEN_SECRET'
	url = 'https://api.twitter.com/1.1/search/tweets.json?q='+query
	auth = OAuth1(app_key,app_secret,access_token,access_token_secret)
	result =  requests.get(url,auth=auth)
	# print result.text
	# return result
	q[1]=result

def instagram(q,query):
	CLIENTID = 'CLIENT_ID'
	CLIENTSECRET = 'CLIENT_SECRET'
	REDIRECTURL = 'REDIRECT_CODE'
	CODE = 'CODE'
	ACCESSTOKEN = 'ACCESS_TOKEN' # TODO : Get access token from server.
	url = 'https://api.instagram.com/v1/tags/coffee/media/recent?access_token='+ACCESSTOKEN
	result = requests.get(url)
	# print result.text
	# return result
	q[2]=result

query = '%23QUERY'
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

for i in q:
	print i.json()
