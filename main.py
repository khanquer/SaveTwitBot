import tweepy
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import urllib
import emoji
import os
#print(os.path.abspath(os.getcwd()))
	
consumer_key = 'TeBR4DGeH6NsSKrdFvgrwYJva'
consumer_secret = 'YqjvbJZKhgqXRDl6VxurwGxsLfBzLEByZGLcSKjxYSifS1LIJe'
access_token = '1245376598024560640-H7TyL2QGi7EWuUZzrYOzBJpWRfu2Qc' 
access_token_secret = 'nJsTlLBaBYGJtpl3CHHY9sSC6UnwFvifiehxTUwSIm6Yl'

global base_path
#base_path = '/home/imrhankhan_shajahan/Projects/SaveTweetBot'
base_path = '/home/imri_linux/Projects/SaveTwitBot'
#base_path = os.path.abspath(os.getcwd())
#print(base_path)

global testing
testing = True

def sendPic(api, tweet, num):
	res = api.media_upload(base_path + '/media/sendfinal{}.jpg'.format(num))
	api.update_status('@' + tweet.user.screen_name, media_ids=[res.media_id], in_reply_to_status_id=tweet.id)


def give_emoji_free_text(text):
	clean_text = emoji.get_emoji_regexp().sub(u'', text)
	print(clean_text)
	txt_list = (clean_text.split(' '))
	for i in txt_list:
		#print('https://t.co' in i)
		if ('https://t.co' in i):
			txt_list.remove(i)
	clean_text = ' '.join(txt_list)
	return clean_text

def formatText(text):
	text = give_emoji_free_text(text)
	finaltext = ''
	maxlen = 26
	lines = text.split('\n')
	# print(len(lines))
	for line in lines:
		# print(len(line))
		if (len(line) < maxlen):
			finaltext += line + '\n'
			continue
		llen = 1
		words = line.split(' ')
		for word in words:
			# print(len(word))
			if (llen + len(word) > maxlen):
				finaltext += '\n' + word + ' '
				llen = len(word)
			else:
				finaltext += word + ' '
				llen += len(word)
		finaltext += '\n'
	print(finaltext.count('\n'))
	numlines = finaltext.count('\n')
	#finaltext = give_emoji_free_text(finaltext)
	return (finaltext,numlines)


def obtainProfPic(origTweet,num):
	tweetdict = origTweet.__dict__
	userA = tweetdict['user']
	#print(type(userA))
	#print(userA.__dict__.keys())
	#PROFILE PICTURE
	img_url = tweetdict['user'].profile_image_url
	img_local_path = base_path + '/media/profpic{}.jpg'.format(num)
	try:
		urllib.urlretrieve(img_url, img_local_path)
	except:
		pass

def obtainTweetPics(origTweet,num):
	if(u'media' in origTweet.entities.keys()):
		tw_img = True
		print(origTweet.entities['media'])
		print(origTweet.entities['media'][0])
		print(origTweet.entities['media'][0]['media_url'])
		img_url = origTweet.entities['media'][0]['media_url'] 
		img_local_path = base_path + '/media/tweetpic{}.jpg'.format(num)
		try:
			urllib.urlretrieve(img_url, img_local_path)
			return True
		except:
			return False

def genTweetPic(api, origTweetId, num):
	origTweet = api.get_status(origTweetId, tweet_mode='extended')


	print('ORIGINAL TWEET ENTITIES')
	img_urls = None
	tw_img = False
	print('\n \n \n')
		
	print('KEYS FOR TWEET/status')
	tweetdict = origTweet.__dict__
	userA = tweetdict['user']

	print(tweetdict['created_at'])
	created_dttm = tweetdict['created_at']


	obtainProfPic(origTweet, num)
	tw_img = obtainTweetPics(origTweet, num)
	
	finaltext,numlines = formatText(origTweet.full_text)

	#if (tw_img):

	nsize = 800
	
	if (tw_img is True):
		hsize = int(nsize/2) + numlines*45 + int(nsize/2)
	else:
		hsize = int(nsize/2) + numlines*45

	bg_img = Image.new('RGB', (nsize, hsize), color=(0, 0, 0))
	d = ImageDraw.Draw(bg_img)

	fnt2 = ImageFont.truetype(base_path + '/fonts/OpenSansEmoji.ttf', size=nsize/21)
	fnt3 = ImageFont.truetype(base_path + '/fonts/Roboto-Bold.ttf', size=nsize/23)
	d.text((nsize/4, nsize/16), userA.name, font=fnt2, fill=(255, 255, 255))
	d.text((nsize/4, nsize/7.7), '@' + userA.screen_name, font=fnt3, fill=(255, 255, 255))

	prof_img = Image.open(base_path + '/media/profpic{}.jpg'.format(num))
	prof_img = prof_img.resize((nsize/8,nsize/8))
	bg_img.paste(prof_img, (nsize/16, nsize/16))

	fnt1 = ImageFont.truetype(base_path + '/fonts/Roboto-Regular.ttf', size=nsize/17)
	#d.text((nsize/16, nsize/4), finaltext, font=fnt1, fill=(255, 255, 255))
	d.text((nsize/16, nsize/4), finaltext, font=fnt1)

	fnt4 = ImageFont.truetype(base_path + '/fonts/Roboto-Regular.ttf', size=nsize/25)
	dttime = str(created_dttm.strftime("%-I:%M %p   %d %b %y"))
	d.text((nsize/16, hsize - nsize/10), dttime, font=fnt4, fill=(169,169,169))

	if (tw_img):
		pic_width = 700
		pic_height = 400
		img_url = Image.open(base_path + '/media/tweetpic{}.jpg'.format(num))
		print(img_url.size)
		img_width,img_height = img_url.size
		print(pic_width/float(img_width))
		pic_size = (pic_width, int(pic_width/float(img_width) * img_height))
		print(pic_size)
		img_url = img_url.resize(pic_size)
		print(img_url.size)
		img_width,img_height = img_url.size

		left = 0
		#top = int((img_height - pic_height)/2)
		top = 0
		right = pic_size[0]
		#bottom = img_height - int((img_height - pic_height)/2)
		bottom = pic_height

		print(left,top,right,bottom)
		img_url = img_url.crop((left,top,right,bottom))
		print(img_url.size)
		#img_url.show()
		print(img_url.size)
		bg_img.paste(img_url, (nsize/16, int(nsize/16) + 180 + numlines*50))

	bg_img.save(base_path + '/media/sendfinal{}.jpg'.format(num))
	print('HI')
	pass


def write_last_replied(num):
	with open(base_path + '/file_store/last_replied.txt', 'w') as f:
		f.write(str(num))

def load_last_replied():
	with open(base_path + '/file_store/last_replied.txt', 'r') as f:
		num = int(f.read())
	return num

def setup_auth():
	print(consumer_key)
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	print(access_token)
	print(access_token_secret)
	
	api = tweepy.API(auth)
	return api
	
def main():
	api = setup_auth()
	
	print(type(api))
	
	last_replied_id = load_last_replied()

	tweets = api.mentions_timeline()

	num = 0
	for tweet in reversed(tweets):
		
		print(str(tweet.id) + ' -- ' + tweet.text + ' -- REPLYING TO ' + str(tweet.in_reply_to_status_id))
		print(tweet.text[:13])
		if(tweet.id <= last_replied_id):
			continue
		if(tweet.text[:13] == '@SaveTweetBot'):
			continue

		origTweetId = tweet.in_reply_to_status_id
		#print('in reply ' + str(tweet.in_reply_to_status_id))

		if origTweetId:
			try:
				genTweetPic(api,origTweetId,num)
			except Exception as ex:
				print(str(ex))
				continue
			#print(tweet.id)
			if (not testing):
				sendPic(api,tweet,num)
				write_last_replied(tweet.id)
		num = num + 1
	return

if __name__ == "__main__":
	main()