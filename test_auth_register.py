import pytest
from server.auth_functions import*
import server.auth_functions as AF
from server.auth_helper_functions import*
from server.password_functions import*
import server.password_functions as PF
from server.helperFunctions import*
import server.helperFunctions as HF
from server.Errors import ValueError
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
This file tests the auth_register function
Assume that auth_register function is correctly implemented
Assume that this function raises early exceptions when:
	email type is invalid
	password type is invalid
	first name type is invalid
	last name type is invalid
	email is invalid
	email is already registered
	password is invalid
	first name is more than 50 chars
	last name is more than 50 chars

'''

def test_register_invalidEmailTypeInt():
	email = 42
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"

	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidEmailTypeList():
	email = ["Hoya", "Lee"]
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"
	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidEmailTypeNone():
	email = None
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"
	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidEmailTypeFloat():
	email = 4.2
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"
	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidEmailTypeBool():
	email = True
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"
	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidEmailTypeTuple():
	email = ("hoya.lee@student.unsw.edu.au", "Hello world")
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"
	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidEmailTypeDict():
	email = {'a': "hoya", 'b': "this is test"}
	password = "12345678"
	name_last = "Lee"
	name_first = "Hoya"
	with pytest.raises(HF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidPasswordTypeInt():
	email = "z5226463@unsw.edu.au"
	password = 12345678
	name_last = "Lee"
	name_first = "Hoya"
	
	with pytest.raises(PF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidPasswordTypeList():
	email = "z5226463@unsw.edu.au"
	password = [1,2,3,4,5]
	name_last = "Lee"
	name_first = "Hoya"
	
	with pytest.raises(PF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidPasswordTypeNone():

	email = "z5226463@unsw.edu.au"
	password = None
	name_last = "Lee"
	name_first = "Hoya"
	
	with pytest.raises(PF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidPasswordTypeBool():

	email = "z5226463@unsw.edu.au"
	password = False
	name_last = "Lee"
	name_first = "Hoya"
	
	with pytest.raises(PF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidPasswordTypeTuple():

	email = "z5226463@unsw.edu.au"
	password = (0,0)
	name_last = "Lee"
	name_first = "Hoya"
	
	with pytest.raises(PF.TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidFirstNameTypeInt():
	email = "z5226463@unsw.edu.au"
	password = "12345678"
	name_last = "Lee"
	name_first = 123
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidFirstNameTypeFloat():
	email = "z5226463@unsw.edu.au"
	password = "sadasdasdasd"
	name_last = "Lee"
	name_first = 2.3
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidFirstNameTypeDict():
	email = "z5226463@unsw.edu.au"
	password = "UASIUAHSUIB"
	name_last = "Lee"
	name_first = {'a' : '1'}
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidFirstNameTypeList():
	email = "z5226463@unsw.edu.au"
	password = "ASSDASAS"
	name_last = "Lee"
	name_first = [1,2,3]
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidFirstNameTypeTuple():
	email = "z5226463@unsw.edu.au"
	password = "AUISIAUDSBID"
	name_last = "Lee"
	name_first = (0,0)
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidLastNameTypeInt():
	email = "z5226463@unsw.edu.au"
	password = "12345678"
	name_first = "Lee"
	name_last = 123
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidLastNameTypeFloat():
	email = "z5226463@unsw.edu.au"
	password = "sadasdasdasd"
	name_first = "Lee"
	name_last = 2.3
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidLastNameTypeDict():
	email = "z5226463@unsw.edu.au"
	password = "UASIUAHSUIB"
	name_first = "Lee"
	name_last = {'a' : '1'}
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidLastNameTypeList():
	email = "z5226463@unsw.edu.au"
	password = "ASSDASAS"
	name_first = "Lee"
	name_last = [1,2,3]
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidLastNameTypeTuple():
	email = "z5226463@unsw.edu.au"
	password = "AUISIAUDSBID"
	name_first = "Lee"
	name_last = (0,0)
	with pytest.raises(TypeError):
		userDict = auth_register(email, password, name_first, name_last)








def test_register_notAEmail():
	email = "email.com"
	password = "P@ssw0rd"
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)
	

def test_register_regularEmail():
	email = "email@gmail.com"
	password = "P@ssw0rd"
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)
	


def test_register_tooLongZID():
	email = "z55555555@unsw.edu.com"
	password = "P@ssw0rd"
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)
	


def test_register_tooShortZID():
	email = "z555555@unsw.edu.com"
	password = "P@ssw0rd"
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)
	





def test_register_invalidPasswordNum():
	email = "z5226464@ad.unsw.edu.au"
	password = "1234"
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)

def test_register_invalidPasswordAlpha():
	email = "z5226464@ad.unsw.edu.au"
	password = "abcd"
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)


def test_register_invalidPasswordEmpty():
	email = "z5226464@ad.unsw.edu.au"
	password = ""
	name_first = "Hoya"
	name_last = "Lee"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)




def test_register_longFirstName():
	email = "z5226464@ad.unsw.edu.au"
	password = "P@ssw0rd"
	name_first = "ThisIsALongSentenceJustToTestTheFunctionAuth_RegisterAndItNeedsMoreThan50Chars"
	name_last = "Lee"

	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)
	
def test_register_longLastName():
	email = "z5226464@ad.unsw.edu.au"
	password = "P@ssw0rd"
	name_first = "Hoya"
	name_last = "ThisIsALongSentenceJustToTestTheFunctionAuth_RegisterAndItNeedsMoreThan50Chars"
	with pytest.raises(ValueError):
		userDict = auth_register(email, password, name_first, name_last)
	



'''

# helper function to check if the email is a valid UNSW email
def check_valid_email(email):
	
	if type(email) != str:
		raise TypeError(f"Email not a string")

	atIndex = 0
	isAt = false
	isZID = false
	isStudent = false

	# check until '@' in email
	for character in email:
		if character == '@':
			isAt = true
			break
		atIndex = atIndex + 1
	# if '@' doesnt exist
	if isAt = false
		raise ValueError(f"Error; not a valid email")

	# check if the doimain is correct
	if email[atIndex:] == "@unsw.edu.au":				# is a Z ID
		isZID = true
	elif email[atIndex:] == "@student.unsw.edu.au":		# is a name Email
		isStudent = true
	else:
		raise ValueError(f"Not a valid UNSW email")


	if isZID = true:
		# too long zID
		if len(email[:atIndex - 1]) != 8:
			raise ValueError(f"Not a valid ZID")
		# does not start with z
		if email[0] != 'z' or email[0] != 'Z':
			raise ValueError(f"Not a valid ZID")
		# check if all following characters are numbers
		for char in email[1:atIndex - 1]
			if char.isdigit() == false:
				raise ValueError(f"Not a valid ZID")
	# student email
	# if name is unique; format is firstNameFirstLetter.lastName@student.unsw.edu.au
	# if name is common: firstName.lastName@student.unsw.edu.au

	elif isStudent = true:
		name = email[:atIndex - 1]
		name = name.split(".")
		if len(name) != 2:
			raise ValueError(f"Not a valid name: more then two names")
		firstName = name[0]
		lastName = name[1]		






# helper function to check if the password is a 'valid' password
# minimal requriements so far
# TODO
def check_valid_password(password):
	if type(password) != str:
		raise TypeError(f"Password not a string")
	if len(password) < 4:
		raise ValueError(f"Invalid password; to little characters")






def check_name_length(name):
	if type(name) != str:
		raise TypeError("Name not a string")
	if len(name) > 50:
		raise ValueError("Name too long")


'''






