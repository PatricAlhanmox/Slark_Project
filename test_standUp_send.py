import pytest

import server.other_functions as OF
import server.token_functions as TF
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_logout, auth_register
from server.channel_functions import channels_create

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
Pub_channel = channels_create(A['token'], 'STDChannel', 'True')
databaseListDict = load_user()


'''If user not login'''
def test_standUp_logout():
    token = A['token']
    auth_logout(A['token'])
    
    channelID = Pub_channel['channel_id']
    
    length = '15'
    
    with pytest.raises(OF.AccessError):
        OF.standup_start(token, channelID, length)
        
        
'''If user is NULL'''
def test_user_NULL():
    auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
    
    token = None
    channelID = Pub_channel['channel_id'] 
    length = '15'
    
    with pytest.raises(TypeError):
        OF.standup_start(token, channelID, length)
        

'''User unauthorised to call standup'''
def test_user_notTheOwner():
    reset_data()
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = channels_create(A['token'], 'STDChannel', 'True')
    token = B['token']
    channelID = Pub_channel['channel_id'] 
    length = '15'
    
    with pytest.raises(OF.AccessError):
        OF.standup_start(token, channelID, length)
        
        
'''If user invalid'''
def test_user_INvalid():
    token = '24367543456798765'
    channelID = Pub_channel['channel_id'] 
    length = '15'
    
    with pytest.raises(TF.AccessError):
        OF.standup_start(token, channelID, length)
        
'''Invalid channelID'''
def test_channel_Invalid():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = channels_create(A['token'], 'STDChannel', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id'] + 10086
    length = '15'
    
    with pytest.raises(CHF.ValueError):
        OF.standup_start(token, channelID, length)


'''Set successfully'''
def test_set_successful():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = channels_create(A['token'], 'STDChannel', 'True')
    token = A['token']
    channelID = Pub_channel['channel_id']
    length = '15'
    
    OF.standup_start(token, channelID, length)

'''Another standup is currently running'''
def test_set_already():
    token = A['token']
    channelID = Pub_channel['channel_id']
    length = '15'
    
    with pytest.raises(OF.ValueError):
        OF.standup_start(token, channelID, length)
        
