import pytest
import server.token_functions as TF
import server.channel_functions as CF
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout
from server.userID_functions import token_to_u_ID

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
Pub_channel = CF.channels_create(A['token'], 'Num1', 'True')
   
    
'''Invalid token'''
def test_addOwner_invalid_token():
    
    token = A['token'] + '100010'
    channelID = Pub_channel['channel_id']
    u_id = B['u_id']
    
    with pytest.raises(TF.AccessError):
        CF.channel_addowner(token, channelID, u_id)
        
       
'''Invalid channelID'''
def test_invlaid_channelID_ADOWNER():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = A['token']
    channelID = None
    u_id = B['u_id']
    
    with pytest.raises(TypeError):
        CF.channel_addowner(token, channelID, u_id)
        
         
'''Invalid UID'''
def test_invlaid_UID_ADOWNER():
    
    token = A['token']
    channelID = Pub_channel['channel_id']
    u_id = None
    
    with pytest.raises(TypeError):
        CF.channel_addowner(token, channelID, u_id)

                   
'''User not login'''
def test_user_NOTLOGIN():
    token = A['token']
    auth_logout(token)
    channelID = Pub_channel['channel_id']
    u_id = B['u_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_addowner(token, channelID, u_id)

'''User already an owner of channel'''
def test_canNot_addOwner():
    auth_login("z5226463@unsw.edu.au", 'HoyaLee2019')
    token = A['token']
    u_id = A['u_id']
    Pub_channel = CF.channels_create(A['token'], 'Test1', 'True')
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CHF.ValueError):
        CF.channel_addowner(token, channelID, u_id)
    

'''Channel addowner successed'''
def test_addOwner_succ():
    token = A['token']
    u_id = B['u_id']
    Pub_channel = CF.channels_create(A['token'], 'Test1', 'True')
    channelID = Pub_channel['channel_id']
    
    CF.channel_addowner(token, channelID, u_id)


'''User is in channel but not in the owner list'''
def test_memeber_addOwner():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = CF.channels_create(A['token'], 'Test1', 'True')
    CF.channel_join(B['token'], Pub_channel['channel_id'])
    token = A['token']
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']  
    
    CF.channel_addowner(token, channelID, u_id)
    
'You cannot promote the uer {u_id} as an owner'
def test_cant_promote():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    Pub_channel = CF.channels_create(A['token'], 'Test1', 'True')
    token = A['token']
    u_id = 1234567
    channelID = Pub_channel['channel_id'] 
    
    CF.channel_addowner(token, channelID, u_id)
