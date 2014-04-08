import json
import Queue
import threading
import requests
from requests_oauthlib import OAuth1
from flask import Flask, render_template, request

def get_data(query):
	def facebook(q,query):
		app_id='APP_ID'
		app_secret='APP_SECRET'
		fields = 'object_id,id,from,story,picture,message,type,created_time,name,link,caption,properties,to'
		url = 'https://graph.facebook.com/search?q='+query+'&type=post&key=value&access_token='+app_id+'|'+app_secret+'&fields='+fields
		result = requests.get(url)
		print result.text
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
		query=query[3:]
		url = 'https://api.instagram.com/v1/tags/'+query+'/media/recent?access_token='+ACCESSTOKEN
		result = requests.get(url)
		# print result.text
		# return result
		q[2]=result
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

	# for i in q:
		# print i.json()

	# print json.dumps(q[1].json())

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
	# print fb
	# print ig
	fbdict = []
	instadict = []
	twitdict = []

	with open('fboutput.txt', 'w') as f:
		for i in fb['data']:
			q={}
			f.write(json.dumps(i))
			f.write('\n')
			# f.write(i['link'])
			f.write('\n')
			f.write('http://facebook.com/'+i['id'].replace('_','/posts/'))
			q['id']='http://facebook.com/'+i['id'].replace('_','/posts/')
			f.write('\n')
			if i['type']=='status':
				f.write('status\t'+i['from']['name'].encode('utf8')+'\t'+'http://facebook.com/'+i['from']['id'].encode('utf8')+'\n')
				try:
					q['story']=i['story']
					f.write(i['story'].encode('utf8') + '\n')
				except:
					q['story']=''
				try:
					q['message']=i['message']
					f.write(i['message'].encode('utf8') + '\n')
				except:
					q['message']=''
				q['type']='status'
				q['user']=i['from']['name']
				q['userhref']='http://facebook.com/'+i['from']['id']



			elif i['type']=='link':
				f.write('link\t'+i['from']['name'].encode('utf8')+'\t'+'http://facebook.com/'+i['from']['id'].encode('utf8')+'\n')
				try:
					f.write(i['story'].encode('utf8') + '\n')
					q['story']=i['story']
				except:
					q['story']=''
				try:
					f.write(i['message'].encode('utf8') + '\n')
					q['message']=i['message']
				except:
					q['message']=''
				try:
					f.write(i['name'].encode('utf8') + '\n')
					q['name']=i['name']
				except:
					q['name']=''
				try:
					f.write(i['link'].encode('utf8') + '\n')
					q['link']=i['link']
				except:
					q['link']=''
				try:
					f.write(i['description'].encode('utf8') + '\n')
					q['description']=i['description']
				except:
					q['description']=''
				q['type']='link'
				q['user']=i['from']['name']
				q['userhref']='http://facebook.com/'+i['from']['id']

			elif i['type']=='photo':
				f.write('photo\t'+i['from']['name'].encode('utf8')+'\t'+'http://facebook.com/'+i['from']['id'].encode('utf8')+'\n')
				f.write(i['picture']+'\n')
				try:
					f.write(i['story'].encode('utf8') + '\n')
					q['story']=i['story']
				except:
					q['story']=''
				try:
					f.write(i['message'].encode('utf8') + '\n')
					q['message']=i['message']
				except:
					q['message']=''
				try:
					f.write(i['caption'].encode('utf8') + '\n')
					q['caption']=i['caption']
				except:
					q['caption']=''
				q['type']='photo'
				q['user']=i['from']['name']
				q['userhref']='http://facebook.com/'+i['from']['id']
				q['picture']=i['picture']

			elif i['type']=='video':
				f.write('video\t'+i['from']['name'].encode('utf8')+'\t'+'http://facebook.com/'+i['from']['id'].encode('utf8')+'\n')
				f.write(i['picture']+'\n')
				try:
					f.write(i['story'].encode('utf8') + '\n')
					q['story']=i['story']
				except:
					q['story']=''
				try:
					f.write(i['message'].encode('utf8') + '\n')
					q['message']=i['message']
				except:
					q['message']=''
				try:
					f.write(i['description'].encode('utf8') + '\n')
					q['description']=i['description']
				except:
					q['description']=''
				q['type']='video'
				q['user']=i['from']['name']
				q['userhref']='http://facebook.com/'+i['from']['id']
				q['picture']=i['picture']

			f.write('\n')
			fbdict.append(q)
		f.write('\n')
		# f.write(fb['paging']['previous'])
		f.write('\n')
		# f.write(fb['paging']['next'])
		f.write('\n')


		try:
			for i in ig['data']:
				q={}
				# print i
				# print i['images']['low_resolution']['url']
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
			print i
			q['user']=i['user']['screen_name']
			q['text']=i['text']
			q['id']=i['id_str']
			try:
				# print "yep",i['entities']['media'][0]
				q['picture']=i['entities']['media'][0]['media_url_https']
			except:
				q['picture']=''
			twitdict.append(q)


	print fbdict
	return fbdict, instadict, twitdict
app = Flask(__name__)

@app.route('/')
def index():
	# content = Markup(markdown.markdown(content))
	query = request.args.get('query')
	if query:
		query = ''.join(e for e in query if e.isalnum())
		fbdata,igdata,twdata = get_data(query)
	return render_template('index.html', **locals())

# @app.route('/')
# def search():
# 	query = request.args.get('query')
# 	# get_data(query)
# 	# fbdata=fbdict
# 	# igdata=instadict
# 	# twdata=twitdict
# 	fbdata,igdata,twdata = get_data(query)
# 	# content = Markup(markdown.markdown(content))
# 	return render_template('search.html', **locals())

app.run(debug=True)
