from werkzeug.exceptions import HTTPException
import uuid
from server.token_functions import decodeToken

# Generate u_id according to user handle
# There wont be any repetitions since user handles are unique
def generateU_ID(userHandle):
	bitSize = 64
	userID = uuid.uuid5(uuid.NAMESPACE_DNS, userHandle).int>>bitSize
	userID = str(userID)
	userID = userID[:10]
	userID = int(userID)
	return userID
# Get u_id with user email
def get_u_ID(databaseListDict, email):
	for user in databaseListDict:
		if user['email'] == email:
			return user['u_id']
# Convert token to u_id
def token_to_u_ID(databaseListDict, token):
	userDictonary = decodeToken(token)
	email = userDictonary['email']
	for user in databaseListDict:
		if user['email'] == email:
			return user['u_id']
