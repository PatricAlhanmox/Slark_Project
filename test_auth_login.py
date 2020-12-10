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
This file tests the function auth_login. 
Assume that auth_login is correctly implemented
Assume that the function raises early exceptions when:
	email type is invalid
	password type is invalid
	email is not valid
	zID is not valid
	email does not belong to a user
	password is not correct
'''




def test_login_invalidEmailTypeInt():

	email = 42
	password = "12345678"
	

	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailTypeList():
	email = ["Hoya", "Lee"]
	password = "12345678"
	
	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailTypeNone():

	email = None
	password = "12345678"
		
	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailTypeFloat():

	email = 4.2
	password = "12345678"
	
	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailTypeBool():

	email = True
	password = "12345678"
	
	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailTypeTuple():
	email = ("hoya.lee@student.unsw.edu.au", "Hello world")
	password = "12345678"

	
	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailTypeDict():

	email = {'a': "hoya", 'b': "this is test"}
	password = "12345678"

	
	with pytest.raises(HF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordTypeInt():
	email = "z5226463@unsw.edu.au"
	password = 12345678

	with pytest.raises(PF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordTypeList():
	email = "z5226463@unsw.edu.au"
	password = [1,2,3,4,5]
	
	with pytest.raises(PF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordTypeNone():
	email = "z5226463@unsw.edu.au"
	password = None
	
	with pytest.raises(PF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordTypeBool():
	email = "z5226463@unsw.edu.au"
	password = False
		
	with pytest.raises(PF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordTypeTuple():
	email = "z5226463@unsw.edu.au"
	password = (0,0)
		
	with pytest.raises(PF.TypeError):
		userDict = auth_login(email, password)

def test_login_invalidEmailGmail():

	email = "regularGMail@gmail.com"	
	password = "12345678"
	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidNotEmail():

	email = "regularMail.com"
	password = "12345678"
	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidEmailEmptyStr():

	email = ""
	password = "12345678"
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidEmailOnlyHost():

	email = "@unsw.edu.au"	
	password = "12345678"
	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidZIDLong():
	email = "z55555555@unsw.edu.au"
	password = "12345678"
	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidZIDShort():

	email = "z555555@unsw.edu.au"
	password = "12345678"

	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidPassword():
	email = "z5226463@unsw.edu.au"
	password = "1234"
	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordEmptyStr():
	email = "z5226463@unsw.edu.au"
	password = " "
	
	
	with pytest.raises(PF.ValueError):
		userDict = auth_login(email, password)

def test_login_invalidPasswordFourAlpha():

	email = "z5226463@unsw.edu.au"
	password = "abcd"
	
	with pytest.raises(ValueError):
		userDict = auth_login(email, password)
		


'''
def test_login_function():
	email = "z5226463.unsw.edu.au"
	password = "abcdefg"
	try:
		check_valid_email(email)
		check_valid_password(password)
	except TypeError:
		print("Password not a string")
	except ValueError:
		print("Not a valid password")
	dictionary = auth_login(email,password)
	assert dictionary["u_id"] == "dummyId"
	assert dictionary["token"] == "dummyToken"

	email = "z5226463@unsw.edu.au"
	password = "abcdefg"
	try:
		check_valid_email(email)
		check_valid_password(password)
	except TypeError:
		print("Password not a string")
	except ValueError:
		print("Not a valid password")
	dictionary = auth_login(email,password)
	assert dictionary["u_id"] == "dummyId"
	assert dictionary["token"] == "dummyToken"

	email = "hoya.lee0@gmail.com"
	password = "abcdefg"
	try:
		check_valid_email(email)
		check_valid_password(password)
	except TypeError:
		print("Password not a string")
	except ValueError:
		print("Not a valid password")
	dictionary = auth_login(email,password)
	assert dictionary["u_id"] == "dummyId"
	assert dictionary["token"] == "dummyToken"

	email = 32
	password = "abcdefg"
	try:
		check_valid_email(email)
		check_valid_password(password)
	except TypeError:
		print("Password not a string")
	except ValueError:
		print("Not a valid password")
	dictionary = auth_login(email,password)
	assert dictionary["u_id"] == "dummyId"
	assert dictionary["token"] == "dummyToken"






# helper function to check if the email is a valid UNSW email
def check_valid_email(email):
	
	if type(email) != str:
		raise TypeError("Email not a string")


	atIndex = 0
	isAt = False
	isZID = False
	isStudent = False

	# check until '@' in email
	for character in email:
		if character == '@':
			isAt = True
			break
		atIndex = atIndex + 1
	# if '@' doesnt exist
	if isAt == False:
		raise ValueError("Error; not a valid email")

	# check if the doimain is correct
	if email[atIndex:] == "@unsw.edu.au":				# is a Z ID
		isZID = True
	elif email[atIndex:] == "@student.unsw.edu.au":		# is a name Email
		isStudent = True
	else:
		raise ValueError("Not a valid UNSW email")


	if isZID == True:
		# too long zID
		if len(email[:atIndex - 1]) != 8:
			raise ValueError("Not a valid ZID")
		# does not start with z
		if email[0] != 'z' or email[0] != 'Z':
			raise ValueError("Not a valid ZID")
		# check if all following characters are numbers
		for char in email[1:atIndex - 1]:
			if char.isdigit() == false:
				raise ValueError("Not a valid ZID")
	# student email
	# if name is unique; format is firstNameFirstLetter.lastName@student.unsw.edu.au
	# if name is common: firstName.lastName@student.unsw.edu.au

	elif isStudent == True:
		name = email[:atIndex - 1]
		name = name.split(".")
		if len(name) != 2:
			raise ValueError("Not a valid name: more then two names")
		firstName = name[0]
		lastName = name[1]		

# helper function to check if the password is a 'valid' password
# minimal requriements so far
# TODO
def check_valid_password(password):
	if type(password) != str:
		raise TypeError("Password not a string")
	if len(password) < 4:
		raise ValueError("Invalid password; to little characters")


'''