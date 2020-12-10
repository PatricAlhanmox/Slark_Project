from werkzeug.exceptions import HTTPException
from server.global_variables import load_user
from server.Errors import ValueError, TypeError

# helper function to check if the email is a valid UNSW email
def check_valid_email(email):
		
	if type(email) != str:
		raise TypeError(description="Email not a string")
	atIndex = 0
	isAt = False
	isZID = False
	# check until '@' in email
	for character in email:
		if character == '@':
			isAt = True
			break
		atIndex = atIndex + 1
	# if '@' doesnt exist
	if not isAt:
		raise ValueError(description="Error; not a valid email")
	# check if the doimain is correct
	if email[atIndex:] == "@unsw.edu.au":				# is a Z ID
		isZID = True
	else:
		raise ValueError(description="Not a valid UNSW email")

	if isZID:
		# too long zID
		if len(email[:atIndex]) != 8:
			raise ValueError(description="Not a valid ZID")
		# does not start with z
		if not (email[0] == 'z' or email[0] == 'Z'):
			raise ValueError(description="Not a valid ZID")
		# check if all following characters are numbers
		for char in email[1:atIndex]:
			if not char.isdigit():
				raise ValueError(description="Not a valid ZID")

def check_valid_name(name):
	if type(name) != str:
		raise TypeError("Name not a string")
	if len(name) > 50:
		raise ValueError(description="Name too long")
