import pytest

import server.auth_functions as AF
import server.auth_helper_functions as AHF
import server.password_functions as PF
from server.global_variables import reset_data


'''If the reset code too long'''
def test_password_rcode_invalid():
    
    code = AHF.generate_reset_code() + 'TooLong233'
    
    password = 'GoodMorningEvery1'
    
    with pytest.raises(AHF.ValueError):
        AF.auth_passwordreset_reset(code, password)



'''if the rest password is None'''
def test_password_Rcode_None():
    
    code = None
    
    password = 'GoodMorningEvery1'
    
    with pytest.raises(TypeError):
        AF.auth_passwordreset_reset(code, password)
        
        
'''If the password is not str'''     
def test_password_none():
    
    code = AHF.generate_reset_code()
    
    password = None
    
    with pytest.raises(PF.TypeError):
        AF.auth_passwordreset_reset(code, password)
        

'''If the password too short'''
def test_password_too_short():
    
    code = AHF.generate_reset_code()
    
    password = 'awc'
    
    with pytest.raises(PF.ValueError):
        AF.auth_passwordreset_reset(code, password)

'''If the password too easy'''
def test_password_dumb():
    code = AHF.generate_reset_code()
    
    password = "abcde"
    
    with pytest.raises(PF.ValueError):
        AF.auth_passwordreset_reset(code, password)
      
        
def test_password_simple1():
    code = AHF.generate_reset_code()
    
    password = "12345"
    
    with pytest.raises(PF.ValueError):
        AF.auth_passwordreset_reset(code, password)
   
        
def test_password_simple2():
    code = AHF.generate_reset_code()
    
    password = "password"
    
    with pytest.raises(PF.ValueError):
        AF.auth_passwordreset_reset(code, password)
        
def test_password_simple3():
    code = AHF.generate_reset_code()
    
    password = "iloveyou"
    
    with pytest.raises(PF.ValueError):
        AF.auth_passwordreset_reset(code, password)    

def test_password_simple4():
    code = AHF.generate_reset_code()
    
    password = "123456"
    
    with pytest.raises(PF.ValueError):
        AF.auth_passwordreset_reset(code, password)   

def test_password_not_string():
    code = AHF.generate_reset_code()
    password = 12345623456780
     
    with pytest.raises(PF.TypeError):
        AF.auth_passwordreset_reset(code, password)        
 

'''If user not in Database'''
def test_password_not_inDB():
    reset_data()
    A = AF.auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    AF.auth_passwordreset_request("z5226463@unsw.edu.au")
    
    code = AHF.generate_reset_code()
    password = 'waitaikong7k7k'
     
    with pytest.raises(AF.ValueError):
        AF.auth_passwordreset_reset(code, password)
        
################################################################################

'''Other auth functions'''
def test_auth_password_succ_requeset():
    email = 'z5000000@unsw.edu.au'
    
    AF.auth_passwordreset_request(email)  

def test_auth_password_fail_requeset():
    email = None
    
    AF.auth_passwordreset_request(email) == None

################################################################################

def test_auth_logout():
    reset_data()
    A = AF.auth_register("z5226463@unsw.edu.au", 'HoyaLee2019', "Hoya", "Lee")
    AF.auth_logout(A['token'])
   
