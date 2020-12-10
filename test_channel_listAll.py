import pytest
import server.token_functions as TF

import server.channel_functions as CF 
import server.channel_helper_functions as CHF 
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
databaseListDict = load_user()


'''If the user are not logged in'''
def test_ALL_Not_login_NoAd():
    token = A['token']
    auth_logout(token)
    with pytest.raises(CF.AccessError):
        CF.channels_listall(token)
        

'''If the token is None'''
def test_ALL_token_None():
    reset_data()
    token = None
    with pytest.raises(TypeError):
        CF.channels_listall(token)
        

'''If the token is Integer'''
def test_ALL_token_Int():
    reset_data()
    token = 2345678865432
    with pytest.raises(TypeError):
        CF.channels_listall(token)


'''If the token can not be decode'''
def test_ALL_DEtoken():
    reset_data()
    token = 'NM$LW$ND6324'
    with pytest.raises(TF.AccessError):
        CF.channels_listall(token)


'''list of User_token successed''' 
def test_ALL_admain_list():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = A['token']
    CF.channels_listall(token)
