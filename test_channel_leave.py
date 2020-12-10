import pytest
import server.token_functions as TF
import server.channel_functions as CF 
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
Pub_channel = CF.channels_create(A['token'], 'Num4', 'True')
databaseListDict = load_user()
    
    
'''Invalid Token'''
def test_invalid_token():
    token = A['token'] + '10086'
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(TF.AccessError):
        CF.channel_join(token, channelID)

'''Invalid channel_id'''
def test_channelisID_invalid():
    token = A['token']
    channelID = Pub_channel['channel_id']+10086
    
    with pytest.raises(CF.AccessError):
        CF.channel_join(token, channelID)
        
        
'''Channel_id is NULL'''
def test_channelisID_NULL():
    token = A['token']
    channelID = None
    
    with pytest.raises(CF.AccessError):
        CF.channel_join(token, channelID)
        
        
'''User not logged in'''
def test_leave_notLogin():
    token = A['token']
    auth_logout(token)
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_join(token, channelID)
        

'''leaved successfully'''
def test_succ_left():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = CF.channels_create(A['token'], 'Num4', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id']
    
    CF.channel_leave(token, channelID)
