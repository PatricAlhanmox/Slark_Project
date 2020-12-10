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


'''Invalid token'''
def test_user_setHand_token():
    token = None
    handle = 'GoodMorning'
    
    with pytest.raises(TypeError):
        UF.user_profile_sethandle(token, handle)
        

'''Invalid handle'''
def test_user_setHand_handle():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    handle = None
    
    with pytest.raises(TypeError):
        UF.user_profile_sethandle(token, handle)
        

'''User not login'''     
def test_user_setHand_NotLogin():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    auth_logout(token)
    handle = 'GoodMorning'
    
    with pytest.raises(UF.AccessError):
        UF.user_profile_sethandle(token, handle) 
        

'''User handle too short'''  
def test_user_handle_short():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    handle = 'M'
    
    with pytest.raises(UF.ValueError):
        UF.user_profile_sethandle(token, handle)
        

'''User handle too long'''
def test_user_handle_long():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    handle = 'M'*23
    
    with pytest.raises(UF.ValueError):
        UF.user_profile_sethandle(token, handle) 
        

'''Existing handle string'''
def test_user_handle_Existed():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    handle = 'goodmorning'
    
    with pytest.raises(UF.ValueError):
        UF.user_profile_sethandle(token, handle)
        


'''Handle set successfully'''
def test_user_handle_success():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    handle = 'goodmorning1'
    
    UF.user_profile_sethandle(token, handle)
