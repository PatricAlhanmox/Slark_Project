from werkzeug.exceptions import HTTPException
import datetime
from datetime import timezone
from server.global_variables import get_global_loggedInUsers, get_global_registeredUsers, get_global_existingChannels
from server.global_variables import OWNER, ADMIN, MEMBER, save_channel,save_registered_users
from server.userID_functions import token_to_u_ID
from server.userHandle_functions import get_user_handle
from server.auth_helper_functions import is_loggedIn, token_to_email
from server.channel_helper_functions import getChannel, get_firstName, get_lastName
from server.channel_helper_functions import get_user_permission, is_inChannel, promote_to_owner_all_channels
from server.message_functions import send_message_help
from server.message_helper_functions import is_time_to_send

from server.Errors import ValueError, AccessError

def admin_permission_change(token, u_id, permission_id):
	if permission_id > MEMBER() or permission_id < OWNER():
		raise ValueError(description="Invalid Permission ID")

	registeredUsersDB = get_global_registeredUsers()
	channelsDB = get_global_existingChannels()

	appointerID = token_to_u_ID(registeredUsersDB, token)
	appointerID = int(appointerID)
	u_id = int(u_id)
	permission_id = int(permission_id)
	appointerPID = get_user_permission(appointerID)
	u_PID = get_user_permission(u_id)

	if appointerPID > permission_id:
		raise ValueError(description="You are not permitted to change a user to higher permission!")

	if appointerPID > u_PID:
		raise ValueError(description="You cannot change a permission of a user with higher permission than you")

	registeredUsersDB = get_global_registeredUsers()
	for user in registeredUsersDB:
		if user['u_id'] == u_id:
			user['permission_id'] = permission_id
			promote_to_owner_all_channels(channelsDB, u_id)
			save_registered_users()
			return {}


	raise ValueError(description=f"User with the user id {u_id} not found")

def search(token, query_str):
	loggedInUsers = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	u_id = token_to_u_ID(loggedInUsers, token)
	messagesDictionary = {'messages':[]}
	for channel in channelsDB:
		for owner in channel['owner_members']:
			if owner['u_id'] == u_id:
				for message in channel['messagesListDict']:
					if query_str in message['message']:
						messagesDictionary['messages'].append(message)
					
		for member in channel['other_members']:
			if member['u_id'] == u_id:
				for message in channel['messagesListDict']:
					if query_str in message['message']:
						messagesDictionary['messages'].append(message)
					
	return messagesDictionary


def standup_start(token, channel_id, length):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	
	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You should be logged in to start a standup")	
	
	channel_id = int(channel_id)
	channel = getChannel(channelsDB, channel_id)
	u_id = token_to_u_ID(loggedInUsersDB, token)

	if channel['is_standup_running']:
		raise ValueError("Another standup is currently running")
	
	# Only owner of the channel can start a standup
	found = False
	for owner in channel['owner_members']:
		if owner['u_id'] == u_id:
			found = True
	if not found:
		raise AccessError(description='You must be an owner of a channel to start a standup')

	now = datetime.datetime.utcnow()
	time_start = int(now.replace(tzinfo=timezone.utc).timestamp())
	time_end = int(time_start + int(length)) 
	
	tempDict = {}
	tempDict['u_id'] = u_id
	tempDict['isActive'] = True
	tempDict['time_start'] = time_start
	tempDict['time_end'] = time_end
	tempDict['messages'] = ''
	channel['is_standup_running'] = True
	channel['standups'].append(tempDict)

	return {'time_finish': time_end}

def standup_send(token, channel_id, message):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="Unauthorised Access")	
	
	channel_id = int(channel_id)
	channel = getChannel(channelsDB, channel_id)
	u_id = token_to_u_ID(loggedInUsersDB, token)

	if not channel['is_standup_running']:
		raise ValueError(description="No standup is running")
	if len(message) > 1000: 
		raise ValueError(description="Message too long")


	if not is_inChannel(channelsDB,channel_id, u_id):
		raise AccessError(description='You must be in a channel to send a standup')


	handle = get_user_handle(registeredUsersDB, u_id)

	message = handle + ' : ' + message +'\n'
	for standup in channel['standups']:
		if standup['isActive']:

			standup['messages'] += message
			
	return {}

def update_standup():
	channelsDB = get_global_existingChannels()
	for channel in channelsDB:
		if channel['is_standup_running']:
			for standup in channel['standups']:
				if standup['isActive']:
					time_now = int((datetime.datetime.utcnow()).replace(tzinfo=timezone.utc).timestamp())
					if is_time_to_send(standup['time_end'], time_now):
						print("standup sent!")
						send_message_help(standup['u_id'], channel['channel_id'], standup['messages'], standup['time_end'])
						standup['isActive'] = False
						channel['is_standup_running'] = False


def standup_active(token, channel_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to see if a standup is active!")	
	
	channel_id = int(channel_id)
	channel = getChannel(channelsDB, channel_id)
	u_id = token_to_u_ID(loggedInUsersDB, token)

	if not channel['is_standup_running']:
		for standup in channel['standups']:
			standup['isActive'] = False
		return {'is_active':False, 'time_finish': None}

	for standup in channel['standups']:
		if standup['isActive']:
			return {'is_active':True, 'time_finish': standup['time_end']}

	channel['is_standup_running'] = False
	save_channel()
 
