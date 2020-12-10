import pytest
import server.token_functions as TF
import server.other_functions as OF
import server.channel_helper_functions as CHF
from server.auth_functions import auth_login, auth_logout, auth_register
from server.global_variables import reset_data, load_user
from server.channel_functions import channels_create
from server.userID_functions import token_to_u_ID

reset_data()
O = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
databaseListDict = load_user()


'''Invalid UID'''
def test_invalid_token():
    token = O['token']
    u_id = None
    permission_id = 1
    
    with pytest.raises(TypeError):
        OF.admin_permission_change(token, u_id, permission_id)

'''Invalid token'''
def test_invalid_UID():
    token = O['token']
    u_id = token_to_u_ID(databaseListDict, token)
    permission_id = 1
    token = None
    
    with pytest.raises(TypeError):
        OF.admin_permission_change(token, u_id, permission_id)


"Permission None"
def test_invalid_PID():
    token = O['token']
    u_id = token_to_u_ID(databaseListDict, token)
    permission_id = None
    
    with pytest.raises(TypeError):
        OF.admin_permission_change(token, u_id, permission_id)
        

'Permission invalid'
def test_wrong_PID():
    token = O['token']
    u_id = token_to_u_ID(databaseListDict, token)
    permission_id = 8
    
    with pytest.raises(OF.ValueError):
        OF.admin_permission_change(token, u_id, permission_id)
        

"permission_id too high"
def test_tooHigh_PID():
    token = A['token']
    u_id = token_to_u_ID(databaseListDict, token)
    permission_id = 1
    
    with pytest.raises(OF.ValueError):
        OF.admin_permission_change(token, u_id, permission_id)

"Invalid permission change; lower permission"
def test_tooHigh_PID2():
    token = A['token']
    u_id = token_to_u_ID(databaseListDict, token)
    permission_id = 4
    
    with pytest.raises(OF.ValueError):
        OF.admin_permission_change(token, u_id, permission_id)


'successed changed'
def test_succ_admain():
    reset_data()
    O = auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    token = O['token']
    u_id = O['u_id']
    
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    i_token = A['token']
    
    permission_id = 2
    
    OF.admin_permission_change(token, u_id, permission_id)
