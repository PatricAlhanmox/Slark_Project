import pytest
import server.token_functions as TF
import server.user_functions as UF 
import server.user_helper_functions as UHF
import server.helperFunctions as HF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")


'''If token type is invalid'''
def test_invalid_tokenType():
    token = None
    
    with pytest.raises(TypeError):
        UF.users_all(token)

'''If token is invalid'''
def test_invalid_token():
    token = A['token'] + '10086'
    
    with pytest.raises(TF.AccessError):
        UF.users_all(token)

'''If user not login'''
def test_user_not_login():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    auth_logout(token)
    
    with pytest.raises(UF.AccessError):
        UF.users_all(token)

'''If success'''
def test_user_sucess():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    
    UF.users_all(token)
