import pytest

import server.channel_functions as CF
import server.channel_helper_functions as CHF
import server.message_functions as MF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_logout, auth_register

reset_data()
O = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
databaseListDict = load_user()
Pub_channel = CF.channels_create(A['token'], 'DeleteChannel', 'True')


'''User logged out'''
def test_delete_logout():
    token = A['token']
    auth_logout(token)
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_delete(token, channelID)
        

'''You must be in the channel to delete a channel!'''
def test_delete_notin_channel():
    token = O['token']
    channelID = Pub_channel['channel_id']
    auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
    
    with pytest.raises(CF.AccessError):
        CF.channel_delete(token, channelID)
        
        
'''User can't define'''
def test_delete_None_channel():
    token = None
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(TypeError):
        CF.channel_delete(token, channelID)
        

'''channelID invalid'''
def test_delete_invalid_channel():
    token = A['token']
    channelID = Pub_channel['channel_id'] + 10086
    
    with pytest.raises(CF.AccessError):
        CF.channel_delete(token, channelID)


'''User not the owner'''
def test_delete_NotOwner():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    B = auth_register("z5147704@unsw.edu.au", "wsad1990", "Bad", "Night")
    Pub_channel = CF.channels_create(A['token'], 'DeleteChannel', 'True')
    token = B['token']
    channelID = Pub_channel['channel_id']
    CF.channel_join(token, channelID)
    with pytest.raises(CF.ValueError):
        CF.channel_delete(token, channelID)
        

'''channel changed successfully'''
def test_delete_success():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = CF.channels_create(A['token'], 'DeleteChannel', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id']
    
    CF.channel_delete(token, channelID)
