from werkzeug.exceptions import HTTPException
import uuid

from server.global_variables import get_global_registeredUsers, get_global_loggedInUsers, MEMBER, ADMIN, OWNER,save_channel
from server.Errors import ValueError, AccessError


def get_firstName(u_id):
	registeredUsersDB = get_global_registeredUsers()
	for user in registeredUsersDB:
		if user['u_id'] == u_id:
			return user['name_first']

def get_lastName(u_id):
	registeredUsersDB = get_global_registeredUsers()
	for user in registeredUsersDB:
		if user['u_id'] == u_id:
			return user['name_last']
def get_url(u_id):
	registeredUsersDB = get_global_registeredUsers()
	for user in registeredUsersDB:
		if user['u_id'] == u_id:
			return user['profile_img_url']

def check_valid_channel_name(name):
	if len(name) > 20:
		raise ValueError(description="Channel name too long")

def generateChannelID(channelDatabaseListDict, name, u_id):

	key = str(name) + str(u_id)
	bitSize = 64
	channel_id = uuid.uuid5(uuid.NAMESPACE_DNS, key).int>>bitSize
	channel_id = str(channel_id)
	channel_id = channel_id[:10]
	channel_id = int(channel_id)
	count = 0
	is_found = False

	if not channelDatabaseListDict:
		return channel_id

	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:
			count += 1
			channel_id = channel_id + count

	return channel_id

def add_to_channel(channelDatabaseListDict, ownerU_ID, nonMemberU_ID, channel_id):
	
	loggedInUsersDB = get_global_loggedInUsers()

	nonMemberU_ID = int(nonMemberU_ID)
	channel_id = int(channel_id)
	ownerU_ID = int(ownerU_ID)
	firstName = get_firstName(nonMemberU_ID)
	lastName = get_lastName(nonMemberU_ID)
	profile_img_url = get_url(nonMemberU_ID)
	nonMemberP_ID = get_user_permission(nonMemberU_ID)

	if not is_inChannel(channelDatabaseListDict, channel_id, ownerU_ID):
		raise AccessError(description='You must be in the channel to invite other members')

	if nonMemberP_ID < MEMBER():
		temp = join_special(channelDatabaseListDict, channel_id, nonMemberU_ID, firstName, lastName, profile_img_url)
		return
	else:
		temp = join_nonSpecial(channelDatabaseListDict, channel_id, nonMemberU_ID, firstName, lastName, profile_img_url)
		return
	raise ValueError(description="Unauthorised Access")



def remove_user_from_channel(channelDatabaseListDict, u_id, channel_id):
	channel_id = int(channel_id)
	u_id = int(u_id)
	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:
			for message in channel['messagesListDict']:
				for react in message['reacts']:
					if u_id in react['u_ids']:
						react['u_ids'].remove(u_id)
		
			for owner in channel['owner_members']:
				if u_id == owner['u_id']:
					channel['owner_members'].remove(owner)
					channel['online_members'].remove(owner)

			for member in channel['other_members']:
				if u_id == member['u_id']:		
					channel['other_members'].remove(member)
					channel['online_members'].remove(member)

			# IF OWNERS ARE EMPTY
			if not channel['owner_members']:
	
				# PROMOTE ALL OTHER MEMBERS AS OWNERS
				if channel['other_members']:
					channel['owner_members'] = channel['other_members']
					channel['other_members'] = []
				# OTHERWISE DELETE CHANNEL
				else:
					channelDatabaseListDict.remove(channel)


def	add_member_to_owner(channelDatabaseListDict, ownerU_ID, u_id, channel_id):
	ownerU_ID = int(ownerU_ID)
	u_id = int(u_id)
	channel_id = int(channel_id)

	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:
			flag = False
			for owner in channel['owner_members']:
				if u_id == owner['u_id']:
					raise ValueError(description="User already an owner of channel")
				if ownerU_ID == owner['u_id']:
					flag = True

			if flag:
				for member in channel['other_members']:
					if u_id == member['u_id']:

						channel['owner_members'].append(member)
						channel['other_members'].remove(member)
						return
			else:
				raise ValueError(description=f'You cannot promote the uer {u_id} as an owner')


def remove_owner(channelDatabaseListDict, userRemoving, userToBeRemoved, channel_id):
	userRemoving = int(userRemoving)
	userToBeRemoved = int(userToBeRemoved)
	channel_id = int(channel_id)

	userRemoving_PID = get_user_permission(userRemoving)
	userToBeRemoved_PID = get_user_permission(userToBeRemoved)

	if userRemoving == userToBeRemoved:
		raise ValueError(description='You cant remove yourself!')

	if userRemoving_PID > userToBeRemoved_PID:
		# ACCESS ERROR
		raise AccessError(description="You cannot remove a user with higher permission ")


	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:

			for member in channel['other_members']:
				if userRemoving == member['u_id']:
					raise AccessError(description="You are not an owner")
				if userToBeRemoved == member['u_id']:
					raise AccessError(description='User is not an owner')

			found = False
			for owner in channel['owner_members']:
				if owner['u_id'] == userRemoving:
					found = True
			if not found:
				raise ValueError(description="You must be an owner to remove an owner")

			for owner in channel['owner_members']:
				if owner['u_id'] == userToBeRemoved:
					channel['other_members'].append(owner)
					channel['owner_members'].remove(owner)
					return

def get_user_permission(u_id):
	registeredUsers = get_global_registeredUsers()
	for user in registeredUsers:
		if user['u_id'] == u_id:
			return user['permission_id']

def get_channel_details(channelDatabaseListDict, u_id, channel_id):
	u_id = int(u_id)
	channel_id = int(channel_id)
	pID = get_user_permission(u_id)
	
	for channel in channelDatabaseListDict:
		if matching_channel_id_and_public(channel, channel_id):
			details = channel
			details['all_members'] = channel['owner_members']+channel['other_members']
			return details
		elif matching_channel_id_and_private(channel, channel_id):
			if pID < MEMBER():
				details = channel
				details['all_members'] = channel['owner_members']+channel['other_members']
				return details
			else:
				for owner in channel['owner_members']:
					if owner['u_id'] == u_id:
						details = channel
						details['all_members'] = channel['owner_members']+channel['other_members']
						return details
				for member in channel['other_members']:
					if member['u_id'] == u_id:
						details = channel
						details['all_members'] = channel['owner_members']+channel['other_members']
						return details

	raise ValueError(description='You cannot view this channel!')
	
def matching_channel_id_and_public(channel, channel_id):
	return channel['channel_id'] == channel_id and channel['is_public']

def matching_channel_id_and_private(channel, channel_id):
	return  channel['channel_id'] == channel_id and not channel['is_public']

def listUserChannels(channelDatabaseListDict, u_id):
	u_id = int(u_id)
	listDict = []
	pID = get_user_permission(u_id)
	
	if not channelDatabaseListDict:
		return listDict

	for channel in channelDatabaseListDict:
		for owner in channel['owner_members']:
			if u_id == owner['u_id']:
				details = channel_name_id_dictionary(channel)
				listDict.append(details)

		for member in channel['other_members']:
			if u_id == member['u_id']:
				details = channel_name_id_dictionary(channel)
				listDict.append(details)

	return listDict

def join_nonSpecial(channelDatabaseListDict, channel_id, u_id, firstName, lastName, profile_img_url):
	loggedInUsersDB = get_global_loggedInUsers()
	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:
			if not channel['is_public']:			
				raise AccessError(description="You cant join a private channel; but you can get invited to one! Ask a friend to invite you!")
			else:
				found = False
				for member in channel['other_members']:
					if member['u_id'] == u_id:
						found = True
				if not found:
					user = {'u_id':u_id, 'name_first': firstName, 'name_last':lastName, 'profile_img_url':profile_img_url}
					channel['other_members'].append(user)

					for loggedinUser in loggedInUsersDB:
						if loggedinUser['u_id'] == u_id:
							channel['online_members'].append(user)
					
				save_channel()
				return {}
def join_special(channelDatabaseListDict, channel_id, u_id, firstName, lastName, profile_img_url):
	loggedInUsersDB = get_global_loggedInUsers()
	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:
			found = False
			for owner in channel['owner_members']:
				if owner['u_id'] == u_id:
					found = True
				
			if not found:
				user = {'u_id':u_id, 'name_first': firstName, 'name_last':lastName, 'profile_img_url':profile_img_url}
				channel['owner_members'].append(user)

				for loggedinUser in loggedInUsersDB:
					if loggedinUser['u_id'] == u_id:
						channel['online_members'].append(user)

			save_channel()
			return {}

def channel_name_id_dictionary(channel):
	return {'name': channel['name'], 'channel_id': channel['channel_id']}

def create_channel_details(name, channel_id, is_public, u_id, name_first, name_last, profile_img_url):
	return {'name':name, 'channel_id':channel_id, 'is_public':is_public, 'owner_members': [{'u_id' : u_id, 'name_first' : name_first, 'name_last' : name_last, 'profile_img_url' : profile_img_url}], 'online_members': [{'u_id' : u_id, 'name_first' : name_first, 'name_last' : name_last, 'profile_img_url' : profile_img_url}], 'other_members': [], 'messagesListDict':[], 'standups': [], 'is_standup_running': False }

def getChannel(channelDatabaseListDict,channel_id):
	for channel in channelDatabaseListDict:
		if channel['channel_id'] == channel_id:
			return channel
	raise ValueError(description="Channel does not exist")

def true_or_false(boolean):
	boolean = boolean.upper()
	if boolean == "TRUE":
		return True 
	else:
		return False
	raise ValueError(description='Please choose if the channel is public or private')

def is_inChannel(channelsDB, channel_id, u_id):
	for channel in channelsDB:
		if channel['channel_id'] == channel_id:
			for owner in channel['owner_members']:
				if owner['u_id'] == u_id:
					return True
			for member in channel['other_members']:
				if member['u_id'] == u_id:
					return True
	return False
 
def promote_to_owner_all_channels(channelsDB, u_id):
	for channel in channelsDB:
		for member in channel['other_members']:
			if member['u_id'] == u_id:
				channel['other_members'].remove(member)
				channel['owner_members'].append(member)
