from werkzeug.exceptions import HTTPException
from urllib import request
from pathlib import Path


from server.global_variables import get_global_loggedInUsers, get_global_registeredUsers
from server.global_variables import get_global_existingChannels, MEMBER, ADMIN, OWNER, DEFAULTPHOTO
from server.global_variables import save_registered_users, save_channel, load_user, load_channel

from server.helperFunctions import check_valid_email, check_valid_name	
from server.userID_functions import generateU_ID, get_u_ID, token_to_u_ID
from server.token_functions import generateToken, generateUserDictionary
from server.password_functions import hashPassword, check_valid_password
from server.userHandle_functions import generateUserHandle, check_valid_handle
from server.channel_helper_functions import remove_user_from_channel

from server.user_helper_functions import get_user_profile, update_name, update_email, update_handle
from server.user_helper_functions import is_url_valid, get_image_sizes, delete_user, crop_image
from server.user_helper_functions import update_profile_photo, update_online_profile_photo

from server.auth_helper_functions import get_registered_user, is_loggedIn, logout_user
from server.auth_helper_functions import token_to_email, is_already_registered

from server.Errors import ValueError, AccessError, TypeError

def user_profile(token, u_id):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)

	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to view a profile!")

	viewerID = token_to_u_ID(registeredUsersDB,token)

	userDictionary = get_user_profile(registeredUsersDB, u_id)
	save_registered_users()
	return userDictionary

def user_setname(token, name_first, name_last):

	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to change your name!")

	check_valid_name(name_first)
	check_valid_name(name_last)

	u_id = token_to_u_ID(registeredUsersDB, token)

	update_name(registeredUsersDB, channelsDB, u_id, name_first, name_last)
	return {}


def user_profile_setemail(token, emailChange):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to change your email")


	check_valid_email(emailChange)

	u_id = token_to_u_ID(registeredUsersDB, token)

	update_email(registeredUsersDB, u_id, emailChange)
	save_registered_users()
	return {}


def user_profile_sethandle(token, handle):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError(description="You must be logged in to change your handle")

	check_valid_handle(registeredUsersDB, handle)

	u_id = token_to_u_ID(registeredUsersDB, token)

	update_handle(registeredUsersDB, u_id, handle)
	save_registered_users()
	return {}

def user_profiles_deleteProfilePhoto(token):
	return user_profiles_uploadphoto(token, DEFAULTPHOTO(), 1,1,200,200, None)

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base):
	channelsDB = get_global_existingChannels()
	loggedInUsersDB = get_global_loggedInUsers()
	registeredUsersDB = get_global_registeredUsers()

	email = token_to_email(token)
	u_id = token_to_u_ID(registeredUsersDB, token)
	u_id = int(u_id)
	if not base:
		try:
			update_profile_photo(registeredUsersDB, channelsDB, u_id, img_url)
			return update_online_profile_photo(loggedInUsersDB, u_id, img_url)
		except:
			raise AccessError(description="Error uploading the photo")
	base = str(base)
	x_start = int(x_start)
	y_start = int(y_start)
	x_end = int(x_end)
	y_end = int(y_end)
	

	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError("You must be logged in to change your photo")
	try:
		request.urlopen(img_url)
	except:
		raise ValueError(description="Cannot open image URL. Please try other images")
	
	request.urlretrieve(img_url, f'frontend/prebundle/images/{u_id}.jpg')
	crop_image(f'frontend/prebundle/images/{u_id}.jpg', x_start, y_start, x_end, y_end).save(f'frontend/prebundle/images/cropped_{u_id}.jpg') 
	port = base[-5:-1]
	port = int(port)
	port += 3000
	string = 'http://localhost:' + str(port) + '/'
	local_url = string + f'images/cropped_{u_id}.jpg'  #adding port and http to match the localhost'port'
	print(local_url, '\n\n\n\n\n\n\n\n\n\n\n')
	# UNTIL HERE ONLYhttp://localhost
	# DONT TOUCH THE CODE BELOW
	try:
		update_profile_photo(registeredUsersDB, channelsDB, u_id, local_url)
		return update_online_profile_photo(loggedInUsersDB, u_id, local_url)
	except:
		raise AccessError(description="Error uploading the photo")

def users_all(token):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError("You must be logged in to view all users")
	userList = []
	for user in registeredUsersDB:
		userList.append(user)
	return {'users':userList}		


def user_profile_delete(token, password):
	registeredUsersDB = get_global_registeredUsers()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = get_global_existingChannels()

	password = hashPassword(password)
	email = token_to_email(token)
	u_id = token_to_u_ID(registeredUsersDB, token)
	u_id = int(u_id)
	
	if not is_loggedIn(loggedInUsersDB, email):
		raise AccessError("You must be logged in to delete your account")

	delete_user(registeredUsersDB, u_id, password)
	delete_user(loggedInUsersDB, u_id, password)

	for channel in channelsDB:
		remove_user_from_channel(channelsDB, u_id, channel['channel_id'])

	save_channel()
	save_registered_users()
	return {}
