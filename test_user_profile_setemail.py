import pytest
import server.token_functions as TF
import server.user_functions as UF 
import server.user_helper_functions as UHF
import server.helperFunctions as HF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
databaseListDict = load_user()


'''Invalid user email'''
def test_user_email_invalidEmail():
    reset_data()
    emailChange = ''
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    
    with pytest.raises(HF.ValueError):
        UF.user_profile_setemail(token, emailChange)


'''Invalid user token'''
def test_user_email_invalidToken():
    emailChange = 'z5172634@unsw.edu.au'
    token = ''
    
    with pytest.raises(UF.AccessError):
        UF.user_profile_setemail(token, emailChange)
        
      
'''You must be logged in to view a profile!'''
def test_user_email_NotLogin():
    token = A['token']
    auth_logout(token)
    emailChange = 'z5172634@unsw.edu.au'
    
    with pytest.raises(UF.AccessError):
        UF.user_profile_setemail(token, emailChange)


'''Not a valid UNSW email'''
def test_user_email_Invalid():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    emailChange = 'acxqqg@gmail.com'
    
    with pytest.raises(HF.ValueError):
        UF.user_profile_setemail(token, emailChange)


'''Email not sting'''
def test_user_email_notString():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    emailChange = 43992200
    
    with pytest.raises(HF.TypeError):
        UF.user_profile_setemail(token, emailChange)
        
        
'''@ is not exist'''
def test_user_invalidFormat():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    emailChange = 'acxqqggmail.com'
    
    with pytest.raises(HF.ValueError):
        UF.user_profile_setemail(token, emailChange)    
    
    
'''this email is already taken!'''
def test_user_email_alreadyTaken():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    emailChange = 'z5000000@unsw.edu.au'
    
    with pytest.raises(UF.ValueError):
        UF.user_profile_setemail(token, emailChange)


'''user email successed'''
def test_user_email_success():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    emailChange = 'z5149573@unsw.edu.au'
    
    UF.user_profile_setemail(token, emailChange)
