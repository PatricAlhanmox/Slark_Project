import pytest

import server.token_functions as TF
import server.channel_functions as CF 
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
databaseListDict = load_user()
Pub_channel = CF.channels_create(A['token'], 'Num3', 'True')
Prv_channel = CF.channels_create(A['token'], 'Num5', 'False')



'''User not logged in'''
def test_Join_not_login():
    token = A['token']
    auth_logout(token)
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_join(token, channelID)
       
 
'''Invalid Token'''
def test_invalid_NADToken():
    token = A['token'] + '14301580495'
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(TF.AccessError):
        CF.channel_join(token, channelID)


'''channelId is invlaid'''
def test_channel_id_invalid():
    token = A['token']
    channelID = Pub_channel['channel_id']+ 14301580495
    
    with pytest.raises(CF.AccessError):
        CF.channel_join(token, channelID)


'''channelId refered private channel'''
def test_channel_joined_failed():
    token = A['token']
    channelID = Prv_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_join(token, channelID)


'''Joined succeefully'''
def test_channel_Succjoined():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = CF.channels_create(A['token'], 'Num3', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id']
    
    CF.channel_join(token, channelID)
    
