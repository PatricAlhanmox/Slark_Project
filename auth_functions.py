from werkzeug.exceptions import HTTPException

from server.global_variables import get_global_loggedInUsers, get_global_registeredUsers
from server.global_variables import get_global_existingChannels
from server.global_variables import MEMBER, ADMIN, OWNER, save_registered_users, save_channel
from server.global_variables import load_channel, load_user, DEFAULTPHOTO

from server.helperFunctions import check_valid_email, check_valid_name
from server.userID_functions import generateU_ID, get_u_ID, token_to_u_ID
from server.token_functions import generateToken, generateUserDictionary
from server.password_functions import hashPassword, check_valid_password
from server.userHandle_functions import generateUserHandle, check_valid_handle

from server.auth_helper_functions import get_registered_user, is_loggedIn, logout_user
from server.auth_helper_functions import token_to_email, make_online
from server.auth_helper_functions import is_already_registered, generate_reset_code
from server.auth_helper_functions import check_valid_reset_code, make_offline
from server.auth_helper_functions import convert_legible_name, generate_empty_user
from server.auth_helper_functions import generate_permission_id

from server.Errors import ValueError

def auth_register(email, password, firstName, lastName):
	registeredUsersDB = load_user()
	loggedInUsersDB = get_global_loggedInUsers()
	check_valid_name(firstName)
	check_valid_name(lastName)
	check_valid_email(email)
	check_valid_password(password)

	# Converts the passed name into a propoer name
	# -- starting with a capital letter followed by small letters
	firstName = convert_legible_name(firstName)
	lastName = convert_legible_name(lastName)

	if is_already_registered(registeredUsersDB, email):
		raise ValueError(description='Email taken by another user')

	userHandle = generateUserHandle(registeredUsersDB, firstName, lastName)
	password = hashPassword(password)
	u_id = generateU_ID(userHandle)

	permission_id = generate_permission_id(email)
	# Generate a dictionary with the set values
	# and also set some required fields to none if not passed in
	registeredDictionary = generate_empty_user(handle=userHandle, email=email, password=password, u_id=u_id, first_name=firstName, last_name=lastName, permission_id=permission_id)
	registeredUsersDB.append(registeredDictionary)
	# Dictionary of email and password for token generation -- think of it as 'payload'
	userDictionary = generateUserDictionary(email, password)
	token = generateToken(userDictionary)
	# The user registered is now logged in
	loggedInUsersDB.append(registeredDictionary)

	save_registered_users()
	return {'u_id':u_id, 'token':token}


def auth_login(email, password):
	registeredUsersDB = load_user()
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = load_channel()

	check_valid_email(email)
	check_valid_password(password)
	password = hashPassword(password)

	# Check if the email and password belongs to a registered user
	userDictionary = get_registered_user(registeredUsersDB, email, password)
	# Set the reset code to be none, in case this log in was right after resetting password
	userDictionary['reset_code'] = None
	u_id = get_u_ID(registeredUsersDB, email)

	if not is_loggedIn(loggedInUsersDB, email):
		loggedInUsersDB.append(userDictionary)
		make_online(channelsDB, u_id)
		save_channel()

	
	userDictionary = generateUserDictionary(email, password)
	token = generateToken(userDictionary)
	

	return {'u_id':u_id, 'token':token}

def auth_logout(token):
	loggedInUsersDB = get_global_loggedInUsers()
	channelsDB = load_channel()

	email = token_to_email(token)
	if not is_loggedIn(loggedInUsersDB, email):
		return {'is_success':False}
	
	u_id = get_u_ID(loggedInUsersDB, email)
	u_id = int(u_id)
	make_offline(channelsDB, u_id)
			


	logout_user(loggedInUsersDB, email, u_id)
	return {'is_success':True}

def auth_passwordreset_request(email):
	registeredUsersDB = get_global_registeredUsers()
	for user in registeredUsersDB:
		if email == user['email']:
			reset_code = generate_reset_code()
			reset_code = str(reset_code)
			# set the reset code of the user
			user['reset_code'] = reset_code
			return reset_code
	return None


def auth_passwordreset_reset(code, password):
	registeredUsersDB = get_global_registeredUsers()

	check_valid_reset_code(code)
	check_valid_password(password)

	for user in registeredUsersDB:
		if user['reset_code'] == code:
			user['password'] = hashPassword(password)
			user['reset_code'] = None
			save_registered_users()
			return {}

	raise ValueError(description="Please try again")
