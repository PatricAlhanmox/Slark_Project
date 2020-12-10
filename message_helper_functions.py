from werkzeug.exceptions import HTTPException
from server.Errors import ValueError


def get_channel(channelDB, message_id):
	for channel in channelDB:
		for message in channel['messagesListDict']:
			
			if message['message_id'] == message_id:
				return channel
	raise ValueError(description=f"Message with {message_id} does not exist")

def pin_message(channel, message_id):
	for message in channel['messagesListDict']:
		if message['message_id'] == message_id:
			if message['is_pinned']:
				raise ValueError(description="Message already pinned")
			else:
				message['is_pinned'] = True
				return {}
def unpin_message(channel, message_id):
	for message in channel['messagesListDict']:
		if message['message_id'] == message_id:
			if not message['is_pinned']:
				raise ValueError(description="Message already unpinned")
			else:
				message['is_pinned'] = False
				return {}
def init_reacts():
	return [{'react_id':1, 'u_ids':[], 'is_this_user_reacted':False}]

def is_time_to_send(time_to_send, time_now):
	return time_now == time_to_send or (time_now - 1) == time_to_send or (time_now + 1) == time_to_send

def create_message(message_id, u_id, message, time_created):
	return {'message_id': message_id, 'u_id':u_id, 'message':message, 'time_created': time_created, 'reacts': init_reacts(), 'is_pinned':False}

def create_message_later(u_id, message, time_created, channel_id):
	return {'channel_id': channel_id, 'u_id':u_id, 'message':message, 'time_created': time_created, 'reacts': init_reacts(), 'is_pinned':False}
	