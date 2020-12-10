import pytest
import server.channel_functions as CF 
import server.token_functions as TF
import server.channel_helper_functions as CHF
from server.global_variables import reset_data
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Tony", "Hex")
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
Pub_channel = CF.channels_create(A['token'], 'channelFirst', 'True')



'''Not logged in'''
def test_reomveOwner_login():
    token = A['token']
    auth_logout(token)
    
    u_id = B['u_id']
    
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)



'''Invalid token'''
def test_remOwner_invalid_token():
    
    #token invalid created
    token = '581v2vj2vj7tvat4ta'
    
    #Create u_id that will be removed
    u_id = A['u_id']
    
    #get the channelID
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(TF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)
        


'''Invalid channelID'''
def test_invlaid_channelID_REMOWNER():
    token = A['token']
    
    #Create u_id that will be removed
    u_id = A['u_id']
    
    #get the channelID
    channelID = Pub_channel['channel_id'] + 10086
    
    with pytest.raises(CHF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)


'''You must be an owner to remove an owner'''
def test_user_REMOVE():
    #get the not owner token
    token = B['token']
    
    #Create u_id that will be removed
    u_id = A['u_id']

    #get the channelID
    channelID = Pub_channel['channel_id']
    
    
    with pytest.raises(CHF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)
    
      

'''You cant remove yourself!'''
def test_user_REMOVE_selfs():
    #get the not owner token
    token = A['token']
    
    #Create u_id that will be removed
    u_id = A['u_id']

    #get the channelID
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CHF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)
        
        
'''You cannot remove a user with higher permission'''
def test_user_REMOVE_Failed():
    token = B['token']
    
    u_id = A['u_id']

    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CHF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)


'''user removed successfully'''
def test_user_REMOVE_SUCC():
    reset_data()
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Tony", "Hex")
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
    Pub_channel = CF.channels_create(A['token'], 'channelFirst', 'True')
    CF.channel_addowner(A['token'], Pub_channel['channel_id'], B['u_id'])
    
    token = A['token']
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']
    CF.channel_addowner(token, channelID, u_id)
    
    CF.channel_removeowner(token, channelID, u_id)

'''User is not an owner'''
def test_user_already_moved():
    reset_data()
    B = auth_register("z5000000@unsw.edu.au", "wsad1990", "Tony", "Hex")
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', 'Hoya', 'Lee')
    Pub_channel = CF.channels_create(A['token'], 'channelFirst', 'True')
    CF.channel_join(B['token'], Pub_channel['channel_id'])
    
    token = A['token']
    u_id = B['u_id']
    channelID = Pub_channel['channel_id']
    
    with pytest.raises(CHF.AccessError):
        CF.channel_removeowner(token, channelID, u_id)
