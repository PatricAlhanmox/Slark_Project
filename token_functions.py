from werkzeug.exceptions import HTTPException
from server.Errors import AccessError
import jwt 
import hashlib

def tokenHashAlgo():
	return 'HS256'

def secretKey():
	string = 'this is a very imporant secret please do not attempt to decode'
	secret = hashlib.sha256(string.encode()).hexdigest()
	return secret

def generateToken(userDictionary):
	token = jwt.encode(userDictionary, secretKey(), algorithm = tokenHashAlgo())
	token = str(token)
	token = token[2:-1]

	return token

def generateUserDictionary(email,password):
	return {'email':email, 'password':password}

def decodeToken(token):
	secret = secretKey()
	token = str.encode(token)
	try:
		userDictionary = jwt.decode(token, secret, algorithm = ('HS256'))
	except:
		raise AccessError(description = 'Invalid token')
		
	return userDictionary