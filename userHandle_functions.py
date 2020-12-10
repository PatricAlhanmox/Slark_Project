from werkzeug.exceptions import HTTPException
from server.Errors import ValueError

'''
	Generate a userhandle according to the first name and last name
	of a user. If the user has more then 20 characters in their 
	appended name, then truncate it to 20 characters. In case of repetitive 
	usernames, append a number at the end of the character and remove the last letter 
	of the name.
'''
def generateUserHandle(databaseListDict, firstName, lastName):
	userHandle = firstName + lastName
	userHandle = userHandle.lower()
	userHandle.replace(" ", "")
	if len(userHandle) > 20:
		userHandle = userHandle[:20]

	is_found = False
	count = 0
	for key in databaseListDict:
		
		if key['handle_str'] == userHandle and not is_found:
			appendIndex = len(str(count))
			appendIndex = 0 - appendIndex
			
			userHandle = userHandle[:appendIndex] + str(count)
		
		elif key['handle_str'] == userHandle:
			count += 1
			appendIndex = len(str(count))
			appendIndex = 0 - appendIndex
			userHandle = userHandle[:appendIndex] + str(count)

	return userHandle


def check_valid_handle(databaseListDict, handle_str):
	if len(handle_str) > 21:
		raise ValueError(description='Handle too long')
	elif len(handle_str) < 2:
		raise ValueError(description='Handle too short')
	else: 
		for user in databaseListDict:
			if user['handle_str'] == handle_str:
				raise ValueError(description='Existing handle string')

def get_user_handle(databaseListDict, u_id):
	for user in databaseListDict:
		if user['u_id'] == u_id:
			return user['handle_str']
	raise ValueError("User does not exist")
