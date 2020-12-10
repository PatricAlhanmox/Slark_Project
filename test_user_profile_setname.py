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


'''Invalid User token'''
def test_user_name_tokenInvalid():
    token = None
    name_first = 'Hello'
    name_last = 'World'
    
    with pytest.raises(TypeError):
        UF.user_setname(token, name_first, name_last)
    
    
'''You must be logged in to change your name!'''
def test_user_name_Notlogin():
    token = A['token']
    auth_logout(token)
    name_first = 'Hello'
    name_last = 'World'
    
    with pytest.raises(UF.AccessError):
        UF.user_setname(token, name_first, name_last)
        
'''name_first too long'''
def test_user_firstname_tooLong():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    name_first = 'A'*51
    name_last = 'World'
    
    with pytest.raises(HF.ValueError):
        UF.user_setname(token, name_first, name_last)

'''name_last too long'''
def test_user_lastname_tooLong():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    name_first = 'Hellows'
    name_last = 'W'*51
    
    with pytest.raises(HF.ValueError):
        UF.user_setname(token, name_first, name_last)

'''name_first not string'''
def test_user_fName():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    name_first = 12345
    name_last = 'World'
    
    with pytest.raises(HF.TypeError):
        UF.user_setname(token, name_first, name_last)
        

'''name_first not string'''
def test_user_lName():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    name_first = 'Hello'
    name_last = 123445
    
    with pytest.raises(HF.TypeError):
        UF.user_setname(token, name_first, name_last)
        

'''user profile success'''
def test_user_profile_success():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    name_first = 'Hello'
    name_last = 'World'
    
    UF.user_setname(token, name_first, name_last)
