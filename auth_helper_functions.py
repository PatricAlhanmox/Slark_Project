from werkzeug.exceptions import HTTPException
import random
import string
from server.token_functions import decodeToken

from server.global_variables import get_global_loggedInUsers, get_global_registeredUsers
from server.global_variables import get_global_existingChannels, MEMBER, ADMIN, OWNER,DEFAULTPHOTO
from server.global_variables import save_registered_users, save_channel, load_channel, load_user
from server.Errors import ValueError

def convert_legible_name(name):
	firstLetter = name.upper()
	firstLetter = firstLetter[0]
	return firstLetter + name[1:]

def get_registered_user(dataBaseListDict, email, password):
	is_found = False
	for user in dataBaseListDict:
		if user['email'] == email:
			if user['password'] == password:
				is_found = True
				return user
			else: 
				raise ValueError(description="Wrong password")
	if not is_found:
		raise ValueError(description="User Does Not Exist")

def is_already_registered(dataBaseListDict, email):
	for user in dataBaseListDict:
		if user['email'] == email:
			return True
	return False

def is_loggedIn(dataBaseListDict, email):
	is_found = False
	for user in dataBaseListDict:
		if user['email'] == email:
			is_found = True
	return is_found

def logout_user(dataBaseListDict, email, u_id):
	channels = get_global_existingChannels()

	for user in dataBaseListDict:
		if user['email'] == email:
			dataBaseListDict.remove(user)

def token_to_email(token):
	userDictionary = decodeToken(token)
	return userDictionary['email']

def generate_reset_code():
	length = 50
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def check_valid_reset_code(reset_code):
	length = 50
	if len(reset_code) != length:
		raise ValueError(description='invalid reset code')

def make_online(channelDictionary, u_id):
	for channel in channelDictionary:
		for owner in channel['owner_members']:
			if owner['u_id'] == u_id:
				channel['online_members'].append(owner)
		for member in channel['other_members']:
			if member['u_id'] == u_id:
				channel['online_members'].append(member)

def make_offline(channelDictionary, u_id):
	for channel in channelDictionary:
		for user in channel['online_members']:
			if user['u_id'] == u_id:
				channel['online_members'].remove(user)
				save_channel()

def generate_empty_user(email, password, u_id, handle, first_name, last_name, permission_id):
	return {'email':email, 'password':password, 'u_id':u_id, 'handle_str':handle, 'name_first': first_name, 'name_last': last_name, 'reset_code' : None, 'permission_id': permission_id, 'profile_img_url':DEFAULTPHOTO()}

def generate_permission_id(email):
	if email == 'z5226463@unsw.edu.au':
		return OWNER()
	else:
		return MEMBER()
