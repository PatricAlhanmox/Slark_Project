import pytest

import server.other_functions as OF
import server.token_functions as TF
import server.channel_helper_functions as CHF
from server.global_variables import reset_data
from server.auth_functions import auth_login, auth_logout, auth_register
from server.channel_functions import channels_create


reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
Pub_channel = channels_create(A['token'], 'STDChannel', 'True')


'''If token is invalid'''
def test_set_standUp_invalid_token():
    token = None
    channel_id = Pub_channel['channel_id']
    
    with pytest.raises(TypeError):
        OF.standup_active(token, channel_id)

'''If channel_id is invalid'''
def test_set_standUp_invalid_channel_id():
    token = A['token']
    channel_id = None 
    
    with pytest.raises(TypeError):
        OF.standup_active(token, channel_id)


'''User not login'''
def test_set_standUp_not_login():
    token = A['token']
    auth_logout(token)
    channel_id = Pub_channel['channel_id'] 
    
    with pytest.raises(OF.AccessError):
        OF.standup_active(token, channel_id)

'''channel standup not running'''
def test_set_channel_notRunning():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = channels_create(A['token'], 'STDChannel', 'True')
    OF.standup_start(A['token'], Pub_channel['channel_id'], '15')
    
    token = A['token']
    channel_id = Pub_channel['channel_id']
    OF.standup_active(token, channel_id)
    

'''standup successfully'''
def test_set_channel_success():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = channels_create(A['token'], 'STDChannel', 'True')
    
    token = A['token']
    channel_id = Pub_channel['channel_id']
    OF.standup_active(token, channel_id)
