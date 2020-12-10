import pytest
import server.token_functions as TF
import server.user_functions as UF 
import server.channel_functions as CF
import server.user_helper_functions as UHF
import server.helperFunctions as HF
from server.global_variables import reset_data, load_user
from server.auth_functions import auth_login, auth_register, auth_logout

reset_data()
A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
databaseListDict = load_user()


'''Invalid token'''
def test_photo_invalidToken():
    token = None
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 0
    y_start = 0
    x_end = 200
    y_end = 200
    base = 5001
    
    with pytest.raises(TypeError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)


def test_photo_invalidBase():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 0
    y_start = 0
    x_end = 200
    y_end = 200
    base = 'abcdefg'
    
    with pytest.raises(ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)

'''Not login'''
def test_photo_notlogin():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    auth_logout(token)
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 0
    y_start = 0
    x_end = 200
    y_end = 200
    base = 5001
    
    with pytest.raises(UF.AccessError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)


'''Start dimension invalid'''
def test_start_dimension():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = -1
    y_start = -1
    x_end = 200
    y_end = 200
    base = 5001
    with pytest.raises(UF.ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)
        

'''End dimension invalid'''
def test_end_invalid():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = -1
    y_start = -1
    x_end = 200
    y_end = 200
    base = 5001
    with pytest.raises(UF.ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)


'''Start equal to end'''
def test_start_equalEnd():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 20
    y_start = 20
    x_end = 20
    y_end = 20
    base = 5001    
    with pytest.raises(UF.ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)


'''X size out of range'''
def test_X_outRange():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 500
    y_start = 20
    x_end = 500
    y_end = 20
    base = 5001
    with pytest.raises(UF.ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)    


'''Y size out of range'''
def test_Y_outRange():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 480
    y_start = 300
    x_end = 20
    y_end = 300
    base = 5001
    with pytest.raises(UF.ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)  


'''Please enter a valid image url'''
def test_valid_img_URL():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://google.com.au.jpg"
    x_start = 0
    y_start = 0
    x_end = 480
    y_end = 290
    base = 5001
    with pytest.raises(UF.ValueError):
        UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)



'''Error uploading the photo with the base'''
def test_upload_base_error():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    CF.channels_create(token, 'UploadError', "True")
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = '0'
    y_start = '0'
    x_end = '200'
    y_end = '200'
    base = None
    
    UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)
        

'''Upload successfully'''
def test_upload_successfully():
    reset_data()
    A = auth_register("z5000000@unsw.edu.au", "wsad1990", "Good", "Morning")
    token = A['token']
    img_url = "http://ichef.bbci.co.uk/onesport/cps/480/mcs/media/images/57210000/jpg/_57210683_57210682.jpg"
    x_start = 0
    y_start = 0
    x_end = 199
    y_end = 199
    base = 5001
    UF.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, base)
