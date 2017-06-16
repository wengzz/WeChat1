#-*- coding:utf-8 -*-

# deal with unicode error(support chinese)
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# import module from django & wechat_sdk
# pip install django && pip install wechat_sdk first
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)

# config wechat parameters
conf = WechatConf(
	token='wzztoken72575',
    appid='wx643c8d6e687cee45',
    appsecret='8dc4deecbdbfcdc7fe24fde660ed3ab2',
    encrypt_mode='normal'
)

# pass csrf check
@csrf_exempt
def wechat_home(request):
	# get signature, timestamp and nonce
	signature = request.GET.get('signature')
	timestamp = request.GET.get('timestamp')
	nonce = request.GET.get('nonce')

	# create a newInstance
	wechat_instance = WechatBasic(conf=conf)

	# check_signature function tells whether the request is sent by wechat
	# not checked
	if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
		return HttpResponseBadRequest('Verify Failed')
	else:
	# checked
		# GET method represents that Wechat sent verification information
		if request.method == 'GET':
			response = request.GET.get('echostr', 'error')
		# POST method stands for Wechat sent user's messages
		else:
			try:
				wechat_instance.parse_data(request.body)	# parse data from instance
				message = wechat_instance.get_message()			# get message
				# classify the type of message
				if isinstance(message, TextMessage):			# text message
					reply_text = 'text'
				elif isinstance(message, VoiceMessage):			# voice message
					reply_text = 'voice'
				elif isinstance(message, ImageMessage):			# image message
					reply_text = 'image'
				elif isinstance(message, LinkMessage):			# link message
					reply_text = 'link'
				elif isinstance(message, LocationMessage):		# location message
					reply_text = 'location'
				elif isinstance(message, VideoMessage):			# video message
					reply_text = 'video'
				elif isinstance(message, ShortVideoMessage):	# shortvideo message
					reply_text = 'shortvideo'
				else:
					reply_text = 'other'						# other message
				response = wechat_instance.response_text(content=reply_text)
			except ParseError:	# ERROR when parsing
				return HttpResponseBadRequest('Invalid XML Data')
		# reply with our defined message
		return HttpResponse(response, content_type="application/xml")

# END