from werkzeug.exceptions import HTTPException
import pickle
import os
from server.Errors import ValueError, AccessError
#########################
registeredUsersDB = []	#
loggedInUsersDB = []	#
channelsDB = []			#
message_id = 0			#
messageQueue = []		#
#########################

'''In order to clean the duplicate and unnecessary data and only remain each test's data'''
def reset_data():
    global registeredUsersDB
    global loggedInUsersDB
    global channelsDB
    registeredUsersDB = []
    save_registered_users()
    loggedInUsersDB = []			
    channelsDB = []	
    save_channel()					
    message_id = 0						
    messageQueue = []

def get_global_message_id():
	global message_id
	return message_id
	
def get_global_loggedInUsers():
	global loggedInUsersDB
	return loggedInUsersDB

def get_global_registeredUsers():
	global registeredUsersDB
	return registeredUsersDB

def get_global_existingChannels():
	global channelsDB
	return channelsDB
	
def get_global_messageQueue():
	global messageQueue
	return messageQueue

def load_user():
	global registeredUsersDB
	registeredUsersDB = load_registered_users()
	return registeredUsersDB
def load_channel():
	global channelsDB
	channelsDB = load_channels()
	return channelsDB


def save_message_id():
	global message_id
	print('saving message_id...')
	with open('message_id.p', 'wb') as FILE:
 	   pickle.dump(message_id, FILE)


def save_registered_users():
	global registeredUsersDB
	print('saving registered users...')
	with open('registered_users.p', 'wb') as FILE:
 	   pickle.dump(registeredUsersDB, FILE)

def save_channel():
	global channelsDB
	print('saving channels...')	
	with open('channels.p', 'wb') as FILE:
 	   pickle.dump(channelsDB, FILE)

def load_registered_users():
	global registeredUsersDB
	if os.path.exists('registered_users.p'):
		try:
			registeredUsersDB = pickle.load(open("registered_users.p", "rb")) # alternative way
			return registeredUsersDB
		except:
			raise ValueError(description='Please refresh the page')
	else:
		return []
def load_message_id():
	global message_id
	if os.path.exists('message_id.p'):
		try:
			message_id = pickle.load(open("message_id.p", "rb")) # alternative way
			return message_id
		except:
			raise ValueError(description='Please refresh the page')
	else: 
		return 0

def load_channels():
	global channelsDB
	if os.path.exists('channels.p'):
		try:
			channelsDB = pickle.load(open("channels.p", "rb")) # alternative way
			return channelsDB
		except:
			raise ValueError(description='Please refresh the page')
	else:
		return []

def DEFAULTPHOTO():
	return 'http://www.edu-fair.net/uploads/2012/07/blanck-pic.jpg'

def PAGINATION():
	return 50

def MEMBER():
	return 3
def ADMIN():
	return 2
def OWNER():
	return 1
