import subprocess, base64

def lookup_user(kth_id):
	try:
		raw = subprocess.check_output(["ssh", "armada@cloud.armada.nu", "ldapsearch -x -h ldap.kth.se -s sub -b 'ou=Addressbook,dc=kth,dc=se' 'ugKthid=" + kth_id + "'"], timeout = 3).decode("utf-8").split("\n")
	
	except:
		print('failed to connect to LDAP')
		return None
	
	email = None
	first_name = None
	last_name = None
	
	for line in raw:
		if line.startswith("mail: "):
			email = line[6:].strip()
			
		if line.startswith("givenName: "):
			first_name = line[11:].strip()
			
		if line.startswith("givenName:: "):
			first_name = base64.b64decode(line[12:].strip())
			
		if line.startswith("sn: "):
			last_name = line[4:].strip()
			
		if line.startswith("sn:: "):
			last_name = base64.b64decode(line[5:].strip())
	
	return dict(email = email, first_name = first_name, last_name = last_name)
