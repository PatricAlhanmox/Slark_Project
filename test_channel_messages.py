import pytest

import server.token_functions as TF
import server.channel_functions as CF 
import server.channel_helper_functions as CHF
from server.global_variables import reset_data
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
Pub_channel = CF.channels_create(A['token'], 'Num0', 'True')


'''Invalid token'''
def test_invalid_token_message():
    
    #get the invalid token
    token = A['token'] + '10081'
    
    #get channelID
    channelID = Pub_channel['channel_id']
    
    #start
    start = '0'
    
    with pytest.raises(TF.AccessError):
        CF.channel_messages(token, channelID, start)
    

'''Invalid channel_id'''
def test_invalid_id_message():
    #get stoken
    token = A['token']
        
    #get invalid channelID
    channelID = None
    
    #start
    start = '0'
    
    with pytest.raises(TypeError):
        CF.channel_messages(token, channelID, start)


'''Invalid start type'''
def test_invalid_start_message():
    #get stoken
    token = A['token']
    
    #get invalid channelID
    channelID = Pub_channel['channel_id']
    
    #start
    start = None
    
    with pytest.raises(TypeError):
        CF.channel_messages(token, channelID, start)


'''Not logged in'''
def test_Not_login():
    #get token
    token = A['token']
    
    #logout
    auth_logout(token)
    
    #get channelID
    channelID = Pub_channel['channel_id']
    
    #start
    start = '0'
    
    with pytest.raises(CF.AccessError):
        CF.channel_messages(token, channelID, start)


'''channel does not exist'''
def test_channel_ID():
    #get stoken
    token = A['token']
    auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
    
    #get channelID
    channelID = '6509779080987'
    
    #start
    start = '0'
    
    with pytest.raises(CHF.ValueError):
        CF.channel_messages(token, channelID, start)


"Starting message too big"
def test_message_too_big():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
    Pub_channel = CF.channels_create(A['token'], 'Num0', 'True')
    
    #get token
    token = A['token']
    
    #get channelID
    channelID = Pub_channel['channel_id']
    
    #start
    start = '100'
    with pytest.raises(CF.ValueError):
        CF.channel_messages(token, channelID, start)


'''channel_success'''
def test_message_succ():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
    Pub_channel = CF.channels_create(A['token'], 'Num0', 'True')
    #get token
    token = A['token']
    
    #get channelID
    channelID = Pub_channel['channel_id']
    
    #start
    start = '0'
    
    assert(CF.channel_messages(token, channelID, start) == {'end': -1, 'messages': [], 'start': 0})
