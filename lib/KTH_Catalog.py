import subprocess, base64
import requests

def lookup_user(kth_id):
	"""
	Lookup a user by KTH-ID. First, an attempt to connect to KTH directory using LDAP protocol is made.
	If the first attempt fails, a second attempt is made using KTH Profiles API.

	Params:
		`kth_id`: User's KTH-ID (username)

	Returns:
		`user_info`: User information containing the email, first name and last name if available.
	"""

	# Try ldap protocol to get user details
	user_dict = lookup_user_with_ldap(kth_id)

	# If ldap does not succeed, try  api
	if user_dict is None:
		user_dict = lookup_user_with_api(kth_id)
	
	return user_dict

def lookup_user_with_ldap(kth_id):
	try:
		raw = subprocess.check_output(["ssh", "armada@cloud.armada.nu", "ldapsearch -x -h ldap.kth.se -s sub -b 'ou=Addressbook,dc=kth,dc=se' 'ugKthid=" + kth_id + "'"], timeout = 3).decode("utf-8").split("\n")
	except:
		print('failed to connect to LDAP')
		return None
	
	user_info = dict(email=None, first_name=None, last_name=None)

	for line in raw:
		if line.startswith("mail: "):
			user_info['email'] = line[6:].strip()
			
		if line.startswith("givenName: "):
			user_info['first_name'] = line[11:].strip()
			
		if line.startswith("givenName:: "):
			user_info['first_name'] = base64.b64decode(line[12:].strip())
			
		if line.startswith("sn: "):
			user_info['last_name'] = line[4:].strip()
			
		if line.startswith("sn:: "):
			user_info['last_name'] = base64.b64decode(line[5:].strip())

	return user_info

def lookup_user_with_api(kth_id):
	# KTH Profiles API - Swagger: https://api.kth.se/api/profile/swagger/?url=/api/profile/swagger.json#/v1.1/getPublicProfile_v11
	base_uri = "https://api.kth.se/api/profile/1.1/"

	uri = base_uri + kth_id
	response = requests.get(uri)
	
	if response.status_code // 100 != 2 or len(response.content) == 0:
		print('failed to connect to KTH Profiles API')
		return None

	try: 
		json = response.json()
	except:
		return None

	return dict(email=json.get('email'), first_name=json.get('givenName'), last_name=json.get('familyName'))
