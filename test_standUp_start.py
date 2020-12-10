import pytest

import server.other_functions as OF
import server.channel_helper_functions as CHF
from server.auth_functions import auth_login, auth_logout, auth_register
from server.channel_functions import channels_create
from server.global_variables import reset_data
import server.Errors as Errors

A = auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
B = auth_login("z5000000@unsw.edu.au", "wsad1990")
Pub_channel = channels_create(A['token'], 'StdChannel', 'True')


'''If user not login'''
def test_standUp_logout():
    token = A['token']
    auth_logout(A['token'])
    
    channelID = Pub_channel['channel_id']
    
    length = '15'
    
    with pytest.raises(OF.AccessError):
        OF.standup_start(token, channelID, length)

        

'''User is not the ownre'''
def test_user_notTheOwner():
    token = B['token']
    channelID = Pub_channel['channel_id'] 
    length = '15'
    
    with pytest.raises(OF.ValueError):
        OF.standup_start(token, channelID, length)
        
        
'''If user invalid'''
def test_user_INvalid():
    token = '24367543456798765'
    channelID = Pub_channel['channel_id'] 
    length = '15'
    
    with pytest.raises(Errors.AccessError):
        OF.standup_start(token, channelID, length)
        
        
'''Invalid channelID'''
def test_channel_Invalid():
    token = A['token']
    channelID = Pub_channel['channel_id'] + 10086
    length = '15'
    
    with pytest.raises(Errors.AccessError):
        OF.standup_start(token, channelID, length)



'''If a stand_up already runing'''
def test_set_already():
    token = A['token']
    channelID = Pub_channel['channel_id']
    length = '15'
    
    with pytest.raises(Errors.AccessError):
        OF.standup_start(token, channelID, length)
        

'''Stand up running success'''
def test_set_success():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = channels_create(A['token'], 'StdChannel', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id']
    length = '15'
    
    OF.standup_start(token, channelID, length)
