import pytest

import server.other_functions as OF
import server.token_functions as TF
import server.channel_functions as CF
import server.channel_helper_functions as CHF
import server.message_functions as MF
from server.global_variables import reset_data
from server.auth_functions import auth_login, auth_logout, auth_register
from server.channel_functions import channels_create

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
Pub_channel = CF.channels_create(A['token'], 'Num0', 'True')
message = MF.message_send(A['token'], Pub_channel['channel_id'], "Hello", 18.11)

'''If token is invalid'''
def test_token_invalid():
    token = None
    query_str = 'hello'
    
    with pytest.raises(TypeError):
        OF.search(token, query_str)


'''Search successfully'''
def test_search_success():
    token = A['token']
    query_str = 'Hello'
    
    OF.search(token, query_str)


def test_search_otherMember_success():
    reset_data()
    
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
    Pub_channel = CF.channels_create(A['token'], 'Num0', 'True')
    CF.channel_join(B['token'], Pub_channel['channel_id'])
    
    token = B['token']
    query_str = 'Hello'
    
    OF.search(token, query_str)


def test_search_string_that_notIn():
    token = A['token']
    query_str = 'World'
    
    OF.search(token, query_str)
