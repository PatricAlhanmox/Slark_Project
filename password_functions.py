from werkzeug.exceptions import HTTPException
from server.Errors import ValueError, TypeError
import hashlib
# hash password
def hashPassword(password):
	password = hashlib.sha256(password.encode()).hexdigest()
	password = str(password)
	return password

def check_valid_password(password):
	if type(password) != str:
		raise TypeError("Password not a string")
	if len(password) < 4:
		raise ValueError(description = "Invalid password; to little characters")
	if password == "abcde":
		raise ValueError(description = "Invalid password; enter a harder password")
	if password == '12345':
		raise ValueError(description = "Invalid password; enter a harder password")
	if password == "password" or password == "iloveyou" or password == "123456":
		raise ValueError(description = "Invalid password; enter a harder password")
	
