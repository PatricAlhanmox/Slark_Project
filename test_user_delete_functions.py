import pytest
import server.token_functions as TF
import server.channel_functions as CF
import server.user_functions as UF 
import server.userID_functions as UIF
import server.user_helper_functions as UHF
import server.Errors as Errors
from server.global_variables import reset_data, load_user,DEFAULTPHOTO
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")


def test_user_delete_invalidToken():
    token = None
    password = 'HoyaLee2019'
    
    with pytest.raises(TypeError):
        UF.user_profile_delete(token, password)


def test_user_delete_invalidPassword():
    token = A['token']
    password = None
    
    with pytest.raises(AttributeError):
        UF.user_profile_delete(token, password)
        

def test_user_delete_notLogin():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = A['token']
    auth_logout(token)
    password = 'HoyaLee2019'
    
    with pytest.raises(UF.AccessError):
        UF.user_profile_delete(token, password)
        
        
def test_user_delete_success():
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = B['token']
    password = "wsad1990"

    UF.user_profile_delete(token, password)
    
       
