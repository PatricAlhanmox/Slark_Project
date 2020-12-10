import pytest
import server.token_functions as TF
import server.user_functions as UF 
import server.user_helper_functions as UHF
import server.Errors as Errors
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
databaseListDict = load_user()

'''Invalid user ID'''
def test_user_invalidID():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    u_id = None
    token = A['token']
    
    with pytest.raises(TypeError):
        UF.user_profile(token, u_id)


'''Invalid user token'''
def test_user_invalidToken():
    u_id = A['u_id']
    token = None
    
    with pytest.raises(TypeError):
        UF.user_profile(token, u_id)
        
        
'''You must be logged in to view a profile!'''
def test_user_NotLogin():
    token = A['token']
    auth_logout(token)
    u_id = A['u_id']
    
    with pytest.raises(UF.AccessError):
        UF.user_profile(token, u_id)


'''user with u_id is not a valid user'''
def test_user_Invalid():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = A['token']
    u_id = A['u_id'] + 10010
    
    with pytest.raises(UF.AccessError):
        UF.user_profile(token, u_id)


'''user profile successed'''
def test_user_success():
    reset_data()
    A = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = A['token']
    u_id = A['u_id']
    
    UF.user_profile(token, u_id)
