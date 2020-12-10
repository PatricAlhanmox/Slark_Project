import pytest
import server.token_functions as TF
import server.channel_functions as CF 
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout
from server.userHandle_functions import generateUserHandle
from server.token_functions import generateToken, generateUserDictionary

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
databaseListDict = load_user()
    
#Test follows:
'''If the user are not logged in'''
def test_Not_login_NoAd():
    token = A['token']
    auth_logout(token)
    with pytest.raises(CF.AccessError):
        CF.channels_list(token)


'''If the token are invalid'''
def test_invalid_AD_token():
    token = A['token'] + '10010'
    auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
    with pytest.raises(TF.AccessError):
        CF.channels_list(token)
        


'''If the token is None'''
def test_token_None():
    token = None
    with pytest.raises(TypeError):
        CF.channels_list(token)
        


'''If the token can not be decode'''
def test_DEtoken():
    reset_data()
    token = 'NM$LW$ND6324'
    with pytest.raises(TF.AccessError):
        CF.channels_list(token)


'''list of Admain_User_token successed'''    
def test_admain_list():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = A['token']
    CF.channels_list(token) 
    
def test_noAdmain_join_list():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = CF.channels_create(A['token'], 'Num2', 'True')
    channelID = Pub_channel['channel_id']
    token1 = B['token']
    CF.channel_join(token1, channelID)
    
    CF.channels_list(token1)
