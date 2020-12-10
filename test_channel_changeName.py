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
Pub_channel = CF.channels_create(O['token'], 'NameChanging', 'True')


'''User logged out'''
def test_changeName_logout():
    token = O['token']
    auth_logout(token)
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_name_change(token, channelID, 'name')
      
        
'''User not part of channel'''
def test_changeName_notin_channel():
    token = A['token']
    channelID = Pub_channel['channel_id']
    auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
    
    with pytest.raises(CF.AccessError):
        CF.channel_name_change(token, channelID, 'name')
        
      
'''User can't define'''
def test_changeName_None_channel():
    token = None
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(TypeError):
        CF.channel_name_change(token, channelID, 'name')
        
'''channelID invalid'''
def test_changeName_invalid_channel():
    token = O['token']
    channelID = Pub_channel['channel_id'] + 10086
    
    with pytest.raises(CF.AccessError):
        CF.channel_name_change(token, channelID, 'name')
        
        
'''channel changed successfully'''
def test_change_success():
    reset_data()
    O = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = O['token']
    Pub_channel = CF.channels_create(O['token'], 'NameChanging', 'True')
    channelID = Pub_channel['channel_id']
    
    CF.channel_name_change(token, channelID, 'Name1')
