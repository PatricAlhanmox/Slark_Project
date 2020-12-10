import pytest
import server.token_functions as TF
import server.channel_functions as CF
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_logout, auth_register

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
Pub_channel = CF.channels_create(A['token'], 'NextChannel', 'True')

#test follows

'''Invalid Token'''
def test_validationOFtoken():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = CF.channels_create(A['token'], 'NextChannel', 'True')
    token = A['token'] + '45645'
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(TF.AccessError):
        CF.channel_details(token, channelID)
    
    
'''Invalid ChannelID'''
def test_invalid_channelID():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = CF.channels_create(A['token'], 'NextChannel', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id'] + 45645
    
    with pytest.raises(CHF.ValueError):
        CF.channel_details(token, channelID)
    
    
'''user not logged in'''
def test_not_loggedIn():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = CF.channels_create(A['token'], 'NextChannel', 'True')
    token = A['token']
    auth_logout(token)
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_details(token, channelID)


'''Details successed'''
def test_details_highPermission_succ():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = CF.channels_create(A['token'], 'NextChannel', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id']
    
    CF.channel_details(token, channelID)
    

