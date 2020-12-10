import pytest
import server.token_functions as TF
import server.channel_functions as CF 
import server.channel_helper_functions as CHF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
databaseListDict = load_user()
Pub_channel = CF.channels_create(A['token'], 'Num2', 'True')
    
    
    
#Test following
'''not  logged in'''
def test_notLogin_invite():
    token = A['token']
    auth_logout(token)
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_invite(token,channelID, u_id)
         
   
'''Invalied channelID'''
def test_Invalid_public_channelID():    
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    u_id = B['u_id']
    channelID = Pub_channel['channel_id'] + 10086
    
    with pytest.raises(CHF.AccessError):
        CF.channel_invite(token, channelID, u_id)
   

'''Invalid user_id for public channel'''
def test_invalid_user_id():
    token = A['token']
    u_id = B['u_id'] + 1
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_invite(token, channelID, u_id)
           

'''A test for channel that not exists'''
def test_channel_invite_notExists():
    token = A['token']
    u_id = B['u_id']
    channelID = None
    
    with pytest.raises(TypeError):
        CF.channel_invite(token, channelID, u_id)

        
'''When the token not exists'''
def test_public_channel_invite_TKnot_exists():
    token = None
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']   
    
    with pytest.raises(TypeError):
        CF.channel_invite(token, channelID, u_id)
        
             
'''when the token can not be decode'''
def test_public_channel_invite_DETK_erro():
    token = 'hcuief7890995789agvhr'
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']  
    
    with pytest.raises(TF.AccessError):
        CF.channel_invite(token, channelID, u_id)


'''You must be in the channel to invite other members'''
def test_public_channel_invitor_NotIN():
    token = A['token']
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CHF.AccessError):
        CF.channel_invite(token, channelID, u_id)

'''Invite successfully'''
def test_channel_invite_success():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    Pub_channel = CF.channels_create(A['token'], 'Num2', 'True')
    channelID = Pub_channel['channel_id']
    token = A['token']
    u_id = B['u_id']
    
    CF.channel_invite(token, channelID, u_id)
