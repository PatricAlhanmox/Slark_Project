from werkzeug.exceptions import HTTPException

from server.global_variables import get_global_loggedInUsers, get_global_registeredUsers, get_global_existingChannels, PAGINATION
from server.global_variables import  MEMBER, ADMIN, OWNER, save_registered_users, save_channel, load_user, load_channel

from server.auth_helper_functions import token_to_email, is_loggedIn, is_already_registered
from server.userID_functions import token_to_u_ID

from server.channel_helper_functions import listUserChannels, check_valid_channel_name, generateChannelID, add_to_channel 
from server.channel_helper_functions import true_or_false, join_special, join_nonSpecial, is_inChannel
from server.channel_helper_functions import remove_user_from_channel, add_member_to_owner, remove_owner, get_channel_details, create_channel_details
from server.channel_helper_functions import get_user_permission, getChannel, get_firstName, get_lastName, get_url, channel_name_id_dictionary

from server.Errors import ValueError, AccessError


def channels_list(token):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to view a list of channels!")

	u_id = token_to_u_ID(registeredUsersDB, token)
	if not channelsDB:
		return {'channels':[]}

	channelListDict = listUserChannels(channelsDB, u_id)
	return {'channels':channelListDict}

def channels_listall(token):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to view a list of channels!")

	if not channelsDB:
		return {'channels':[]}

	u_id = token_to_u_ID(registeredUsersDB,token)
	u_id = int(u_id)
	pID = get_user_permission(u_id)

	channelListDict = []
	for channel in channelsDB:
		if pID < MEMBER():
			channelDict = channel_name_id_dictionary(channel)
			channelListDict.append(channelDict)

		elif channel['is_public']:
			channelDict = channel_name_id_dictionary(channel)
			channelListDict.append(channelDict)

	return {'channels':channelListDict}


def channel_delete(token, channel_id):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	
	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be in a channel to delete a channel!")

	u_id = token_to_u_ID(loggedInUsersDB, token)
	u_id = int(u_id)
	channel_id = int(channel_id)

	if not is_inChannel(u_id=u_id, channel_id=channel_id, channelsDB = channelsDB):
		raise AccessError(description='You must be in the channel to delete a channel!')

	for channel in channelsDB:
		if channel['channel_id'] == channel_id:
			for owner in channel['owner_members']:
				if u_id == owner['u_id']:
					channelsDB.remove(channel)
					save_channel()
					return {}

	raise ValueError(description='You must be an owner to delete the channel!')


def channel_name_change(token, channel_id, name):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = load_channel()

	check_valid_channel_name(name)
	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to change the name of a channel!")

	u_id = token_to_u_ID(loggedInUsersDB, token)
	u_id = int(u_id)
	channel_id = int(channel_id)
	if not is_inChannel(u_id=u_id, channel_id=channel_id, channelsDB = channelsDB):
		raise AccessError(description='You must be in the channel to change the name of a channel!')
	for channel in channelsDB:
		if channel['channel_id'] == channel_id:
			for owner in channel['owner_members']:
				if u_id == owner['u_id']:
					channel['name'] = name
					save_channel()
					return {}
	raise AccessError(description='You must be an owner of the channel to change the name of the channel!')

def channels_create(token, name, is_public):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()
	email = token_to_email(token)
	
	if not is_loggedIn(loggedInUsersDB, email):
		
		raise AccessError(description="You must be logged in to create a channel!")
	
	is_public = true_or_false(is_public)

	check_valid_channel_name(name)

	u_id = token_to_u_ID(loggedInUsersDB, token)
	u_id = int(u_id)

	channel_id = generateChannelID(channelsDB, name, u_id)

	first_name = get_firstName(u_id)
	last_name = get_lastName(u_id)	
	url = get_url(u_id)

	channelDict = create_channel_details(name = name, channel_id = channel_id, is_public = is_public, u_id = u_id, name_first = first_name, name_last = last_name, profile_img_url = url)
	channelsDB.append(channelDict)

	save_channel()

	return {'channel_id': channel_id}

def channel_join(token, channel_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()


	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="you must be logged in to join of a channel!")


	# CHECK THE VALIDITY 

	u_id = token_to_u_ID(loggedInUsersDB, token)
	u_id = int(u_id)
	channel_id = int(channel_id)
	first_name = get_firstName(u_id)
	last_name = get_lastName(u_id)
	profile_img_url = get_url(u_id)

	permission = get_user_permission(u_id)
	if permission < MEMBER():
		return join_special(channelsDB, channel_id, u_id, first_name, last_name, profile_img_url)

	else:
		return join_nonSpecial(channelsDB, channel_id, u_id, first_name, last_name, profile_img_url)
	


	raise ValueError(description="Invalid Channel ID")


def channel_invite(token, channel_id, u_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()


	email = token_to_email(token)
	u_id = int(u_id)

	if not is_loggedIn(loggedInUsersDB, email):		
		raise AccessError(description="You must be logged in invite a friend into a channel!")
	
	if not is_already_registered(registeredUsersDB, email):
		raise ValueError(description=f"User with ID {u_id} does not exist")
	


	ownerU_ID = token_to_u_ID(loggedInUsersDB, token)

	ownerU_ID = int(ownerU_ID)
	channel_id = int(channel_id)

	add_to_channel(channelsDB, ownerU_ID, u_id, channel_id)
	save_channel()
	return {}

def channel_leave(token, channel_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):		
		raise AccessError(description="You must be logged in to leave a channel!")

	u_id = token_to_u_ID(loggedInUsersDB, token)
	u_id = int(u_id)
	channel_id = int(channel_id)
	remove_user_from_channel(channelsDB,u_id, channel_id)
	save_channel()
	return {}

def channel_addowner(token, channel_id, u_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):		
		raise AccessError(description="you must be logged in to add an owner to a channel!")

	ownerU_ID = token_to_u_ID(loggedInUsersDB, token)
	add_member_to_owner(channelsDB, ownerU_ID, u_id, channel_id)
	save_channel()	
	return {}

def channel_removeowner(token, channel_id, u_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to remove an owner of a channel!")

	ownerU_ID = token_to_u_ID(registeredUsersDB, token)
	remove_owner(channelsDB, ownerU_ID, u_id, channel_id)
	save_channel()
	return {}

def channel_details(token, channel_id):
	registeredUsersDB = load_user()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = load_channel()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to view the details of a channel!")

	u_id = token_to_u_ID(loggedInUsersDB, token)
	channelDictionary = get_channel_details(channelsDB, u_id, channel_id)
	save_channel()    
	return channelDictionary



def channel_messages(token, channel_id, start):

	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	start = int(start)
	end = start + PAGINATION()
	channel_id = int(channel_id)
	email = token_to_email(token)

	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to view the messages of a channel!")

	u_id = token_to_u_ID(loggedInUsersDB, token)
	channel = getChannel(channelsDB, channel_id)
	messagesLength = len(channel['messagesListDict'])
	
	if messagesLength < start:
		raise ValueError(description="Starting message too big")

	returnDictionary = {'messages':[]}

	if messagesLength < end:
		returnDictionary['end'] = -1
		returnDictionary['start'] = start
	else:
		returnDictionary['end'] = end
		returnDictionary['start'] = start
	
	for message in channel['messagesListDict']:
		if start == end:
			break
		returnDictionary['messages'].append(message)
		start += 1
	save_channel()
	return returnDictionary
