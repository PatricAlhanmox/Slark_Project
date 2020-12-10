from werkzeug.exceptions import HTTPException
import datetime
from datetime import timezone

from server.global_variables import get_global_message_id, get_global_loggedInUsers, get_global_registeredUsers
from server.global_variables import get_global_existingChannels, get_global_messageQueue, save_message_id, load_message_id
from server.userID_functions import token_to_u_ID
from server.message_helper_functions import get_channel, pin_message, unpin_message, is_time_to_send
from server.message_helper_functions import create_message, init_reacts, create_message_later
from server.channel_helper_functions import get_user_permission, is_inChannel
from server.Errors import ValueError, AccessError


message_id = 0

def message_send(token, channel_id, message, time_sent):
	if len(message) > 1000:
		raise ValueError(description="Message too long")

	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	channel_id = int(channel_id)

	u_id = token_to_u_ID(loggedInUsersDB, token)

	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel_id):
		raise AccessError(description='You must join the channel to send a message!')
	return send_message_help(u_id, channel_id, message, time_sent)

def message_send_later(token, channel_id, message, time_to_send):
	messageQueue = get_global_messageQueue()

	time_to_send = float(time_to_send)
	time_to_send = int(time_to_send)

	if len(message) > 1000:
		raise ValueError(description="Message too long")

	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	messageQueue = get_global_messageQueue()

	channel_id = int(channel_id)

	u_id = token_to_u_ID(loggedInUsersDB, token)


	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel_id):
		raise AccessError(description='You must join the channel to send a message!')

	timeNow = (datetime.datetime.utcnow() - datetime.timedelta(seconds=1)).replace(tzinfo=timezone.utc).timestamp()

	if time_to_send < timeNow:
		raise ValueError(description='You selected a time in the past!')


	length = len(messageQueue) + 1
	msgElement = create_message_later(u_id, message, time_to_send, channel_id)
	messageQueue.append(msgElement)
	# This is just temporary; it will get updated once the message actually sends
	return {'message_id': length}


def update_message():
	messageQueue = get_global_messageQueue()
	if not messageQueue:
		return
	for message in messageQueue:
		time_now = int((datetime.datetime.utcnow()).replace(tzinfo=timezone.utc).timestamp())
		if is_time_to_send(message['time_created'], time_now):
			send_message_help(message['u_id'], message['channel_id'], message['message'], message['time_created'])
			messageQueue.remove(message)
			print('\n\n\n\n\nupdated!\n\n\n\n\n')

def send_message_help(u_id, channel_id, message, time_created):
	global message_id
	channelsDB = get_global_existingChannels()
	channel = getChannel(u_id=u_id, channel_id=channel_id)
	print('\n\n\n\n\n\n', message_id, '\n\n\n\n\n\n')
	
	try:	
		msgElement = create_message(message_id, u_id, message, time_created)
		channel['messagesListDict'].insert(0, msgElement)
		print(channel['messagesListDict'], '\n\n\n\n\n\n\n\n\n\n\n')
		message_id += 1
		save_message_id()
		return {'message_id':message_id}
	except:
		raise AccessError(description='Cannot send message; you are not in the channel!')

def getChannel(u_id, channel_id):
	channelsDB = get_global_existingChannels()
	for channel in channelsDB:
		if channel['channel_id'] == channel_id:
			for owner in channel['owner_members']:
				if u_id == owner['u_id']:
					return channel
			for member in channel['other_members']:
				if u_id == member['u_id']:
					return channel
	raise AccessError(description='The channel does not exist!')
#DONE
def message_pin(token, message_id):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	message_id = int(message_id)
	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = get_channel(channelsDB, message_id)

	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel['channel_id']):
		raise AccessError(description='You must be in the channel to pin a message!')

	for owner in channel['owner_members']:
		if u_id == owner['u_id']:
			return pin_message(channel, message_id)

	for member in channel['other_members']:
		if u_id == member['u_id']:
			raise AccessError(description="You must be an owner of the channel to pin!")

def message_unpin(token, message_id):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	message_id = int(message_id)
	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = get_channel(channelsDB, message_id)
	
	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel['channel_id']):
		raise AccessError(description='You must be in the channel to unpin a message!')

	for owner in channel['owner_members']:
		if u_id == owner['u_id']:
			return unpin_message(channel, message_id)
	for member in channel['other_members']:
		if u_id == member['u_id']:
			raise AccessError(description="You must be an owner of the channel to unpin!")

def message_edit(token, message_id, editMessage):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	message_id = int(message_id)

	if len(editMessage) > 1000:
		raise ValueError(description="Message too long")


	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = get_channel(channelsDB, message_id)

	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel['channel_id']):
		raise AccessError(description='You must be in the channel to edit a message!')

	for message in channel['messagesListDict']:
		if message['message_id'] == message_id:
			if message['u_id'] == u_id:
				if editMessage.isspace():
					message_remove(token, message_id)
				else:
					message['message'] = editMessage
				return {}
			else: 
				for owner in channel['owner_members']:
					if u_id == owner['u_id']:
						if editMessage.isspace():
							message_remove(token, message_id)
						else:
							message['message'] = editMessage
						return {}
				raise AccessError(description="You did not write this message. You need to be an owner of the channel to edit a message you did not write!")

	raise ValueError(description="Error editting")



def message_remove(token, message_id):

	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	message_id = int(message_id)

	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = get_channel(channelsDB, message_id)
	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel['channel_id']):
		raise AccessError(description='You must be in the channel to remove a message!')

	for message in channel['messagesListDict']:
		if message['message_id'] == message_id:
			if message['u_id'] == u_id:
				channel['messagesListDict'].remove(message)
				return {}
			for owner in channel['owner_members']:
				if u_id == owner['u_id']:
					channel['messagesListDict'].remove(message)
					return {}			
	raise AccessError(description="You are not allowed to remove this message")


def check_reaction(react_id):
	if react_id != 1:
		raise ValueError(description='invalid react id')

def message_react(token, message_id, react_id):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	message_id = int(message_id)
	react_id = int(react_id)

	check_reaction(react_id)

	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = get_channel(channelsDB, message_id)

	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel['channel_id']):
		raise AccessError(description='You must be in the channel to react to a message!')

	for message in channel['messagesListDict']:
		if message['message_id'] == message_id:
			for reaction in message['reacts']:
				if reaction['react_id'] == react_id:
					if u_id in reaction['u_ids']:
						raise ValueError(description='You already reacted to this message!')
					else:
						reaction['u_ids'].append(u_id)
						if get_user_permission(u_id) < 2:
							reaction['is_this_user_reacted'] = True
						return {}
			
	raise ValueError("Error reacting")
	

def message_unreact(token, message_id, react_id):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	message_id = int(message_id)
	react_id = int(react_id)

	check_reaction(react_id)

	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = get_channel(channelsDB, message_id)

	if not is_inChannel(channelsDB=channelsDB, u_id=u_id, channel_id=channel['channel_id']):
		raise AccessError(description='You must be in the channel to unreact to a message!')

	for message in channel['messagesListDict']:
		if message['message_id'] == message_id:
			for reaction in message['reacts']:
				if reaction['react_id'] == react_id:
					if u_id in reaction['u_ids']:
						reaction['u_ids'].remove(u_id)
						reaction['is_this_user_reacted'] = False
						for userID in reaction['u_ids']:
							if get_user_permission(userID) < 2:
								reaction['is_this_user_reacted'] = True	
						return
					else:
						raise ValueError(description='You cant unreact a unreacted message!')
	raise ValueError("Error unreacting")
