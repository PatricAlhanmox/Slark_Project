import pytest
from server.message_functions import *
import server.message_functions as MF
from server.auth_functions import *
from server.auth_helper_functions import *
import server.auth_helper_functions as AHF
from server.global_variables import *
from server.token_functions import *
from server.password_functions import * 
from server.channel_functions import *

import datetime 
from datetime import timezone
from server.message_helper_functions import *
import server.message_helper_functions as MHF
from server.Errors import ValueError, AccessError
# Data types:
# 	Variable Name:
#		email 		str
#		id 			int
#		password	str	
#		token 		str
#		message 	str
#		name 		str
#		code 		str
#	has prefix:
#		is_ 		bool
#		time_ 		datetime
#	has suffix:
#		_id 		int
#		_url 		str
#		_str		str
# 		end 		int
#		start 		int
# Outputs:
#	messages 		list of dictionaries with types{u_id, message, time_created, is_unread}
#	channels 		list of dictionaries with types {id, name}
#	members 		list of dictionaries with types {u_id, name_first, name_last}
'''
README
This file tests the message_pin function
Assume that all the functions used in this tests are complete
Assume that these function raises early exceptions when:
	message_id is not a valid message
	The authorised user is not an admin
	Message with ID message_id is already pinned
    The authorised user is not a member of the channel that the message is within
'''

def create_admin_token():
	email = "z5777777@unsw.edu.au"
	password ="validPassword"
	name_first = "test"
	name_last = "man"
	registeredUsersDB = load_user()
	loggedInUsersDB = get_global_loggedInUsers() #should login then it can create channel
	
	if is_already_registered(registeredUsersDB, email)==False:
		user = auth_register(email, password, name_first, name_last)
		validToken = user['token']
	else:
		hashpass = hashPassword(password)
		userDictionary = generateUserDictionary(email,hashpass)
		validToken = generateToken(userDictionary)

	auth_login(email, password)
	return validToken	
		
	
	 

def create_nonAdmin_token():
	email = "z5234355@unsw.edu.au"
	password = "validPassword"
	name_first = "Adrian"
	name_last = "Radoman"
	
	registeredUsersDB = load_user()
	if is_already_registered(registeredUsersDB, email)==False:
		user = auth_register(email, password, name_first, name_last)
		validToken = user['token']
		auth_login(email, password)
		return validToken
	else:
		hashpass = hashPassword(password)
		userDictionary = generateUserDictionary(email,hashpass)
		validToken = generateToken(userDictionary)
		auth_login(email, password)
		return validToken

def create_nonAdmin_u_ID():
	email = "z5234355@unsw.edu.au"
	password = "validPassword"
	name_first = "Adrian"
	name_last = "Radoman"

	registeredUsersDB = load_user()
	if is_already_registered(registeredUsersDB, email)==False:
		user = auth_register(email, password, name_first, name_last)
		validID = user['u_id']
		return validID		
	else:
		password = hashPassword(password)
		user = get_registered_user(registeredUsersDB, email, password)
		validID = user['u_id']
		return validID

def create_public_channel_id():
	channelName = "cool Channel"
	is_public = "TRUE"
	token = create_admin_token()
	channel = channels_create(token, "name", is_public)
	channel_id = channel['channel_id']
	return channel_id

def test_message_pin_invalidMessageID():
	adminToken = create_admin_token()
	channelID = create_public_channel_id()
	
	message_id = 100000

	with pytest.raises(MHF.ValueError):
		voidDict = message_pin(adminToken, message_id)


	
def test_message_pin_nonAdminPin():
	adminToken = create_admin_token()
	channelID = create_public_channel_id()
	nonAdmintoken = create_nonAdmin_token()
	nonAdminUID = create_nonAdmin_u_ID()
	channel_join(nonAdmintoken,channelID)


	message = "message"
	time_sent=int(datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
	mslist=message_send(adminToken, channelID, message, time_sent)
	message_id=mslist['message_id']-1


	with pytest.raises(AccessError):
		voidDict = message_pin(nonAdmintoken, message_id)


def test_message_pin_alreadyPinned():
	adminToken = create_admin_token()
	channelID = create_public_channel_id()

	message = "message"
	time_sent=int(datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
	mslist=message_send(adminToken, channelID, message, time_sent)
	message_id=mslist['message_id']-1 

	message_pin(adminToken, message_id)

	with pytest.raises(ValueError):
		voidDict = message_pin(adminToken, message_id)



def test_message_pin_userNotInChannel():
    adminToken = create_admin_token()
    channelID = create_public_channel_id()
    nonAdminToken = create_nonAdmin_token()
    message = "message"
    time_sent=int(datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    mslist=message_send(adminToken, channelID, message, time_sent)
    message_id=mslist['message_id']-1
        
    with pytest.raises(AccessError):
        voidDict = message_pin(nonAdminToken, message_id)
