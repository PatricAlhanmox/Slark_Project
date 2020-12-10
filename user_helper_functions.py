from werkzeug.exceptions import HTTPException
import requests
import urllib.request
from PIL import ImageFile, Image
from server.Errors import ValueError, AccessError
from server.global_variables import save_registered_users, save_channel

def get_user_profile(databaseListDict, u_id):
	u_id = int(u_id)
	for user in databaseListDict:
		if user['u_id'] == u_id:
			return user
	raise AccessError(description='User does not exist')

def update_name(userDB, channelsDB, u_id, name_first, name_last):
	u_id = int(u_id)
	# update user in users dictionary
	for user in userDB:
		if user['u_id'] == u_id:
			user['name_first'] = name_first
			user['name_last'] = name_last
			save_registered_users()
	# update user in channels dictionary
	for channel in channelsDB:
		for owner in channel['owner_members']:
			if owner['u_id'] == u_id:
				#UPDATE
				owner['name_last'] = name_last
				owner['name_first'] = name_first
		for member in channel['other_members']:
			if member['u_id'] == u_id:
				#UPDATE
				member['name_last'] = name_last
				member['name_first'] = name_first
		save_channel()

def update_profile_photo(databaseListDict,channelsDB, u_id, local_url):
	for user in databaseListDict:
		if user['u_id'] == u_id:
			user['profile_img_url'] = local_url
			save_registered_users()
			for channel in channelsDB:
				for owner in channel['owner_members']:
					if owner['u_id'] == u_id:
						#UPDATE
						owner['profile_img_url'] = local_url
						save_channel()
				for member in channel['other_members']:
					if member['u_id'] == u_id:
						#UPDATE
						member['profile_img_url'] = local_url
						save_channel()

def update_online_profile_photo(databaseListDict, u_id, local_url):
	for user in databaseListDict:
		if user['u_id'] == u_id:
			user['profile_img_url'] = local_url			
			return {}

def update_email(databaseListDict, u_id, email):
	u_id = int(u_id)
	
	for user in databaseListDict:
		if user['email'] == email:
			raise ValueError(description='this email is already taken!')

	for user in databaseListDict:
		if user['u_id'] == u_id:
			user['email'] = email
			return

def update_handle(databaseListDict, u_id, handle_str):
	u_id = int(u_id)
	for user in databaseListDict:
		if user['u_id'] == u_id:
			user['handle_str'] = handle_str
			return

def is_url_valid(url):
	r = requests.head(url)
	return r.status_code == requests.codes.ok

def get_image_sizes(url):
    # get file size *and* image size (None if not known)
    file = urllib.request.urlopen(url)
    size = file.headers.get("content-length")
    if size: 
    	size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size
    file.close()
    return size, None

def delete_user(databaseListDict, u_id, password):
	for user in databaseListDict:
		if user['u_id'] == u_id:
			if user['password'] == password:
				databaseListDict.remove(user)

def crop_image(photo, x_start, y_start, x_end, y_end):
	image = Image.open(photo)
	width, height = image.size
	if x_start == x_end or y_start == y_end:
		raise ValueError('Invalid crop size!')
	elif x_start >= width or x_start < 0 or x_end >= width or x_end < 0:
		raise ValueError('Invalid crop size!')
	elif y_start >= width or y_start < 0 or y_end >= width or y_end < 0:
		raise ValueError('Invalid crop size!')
	return image.crop((x_start,y_start,x_end, y_end))
