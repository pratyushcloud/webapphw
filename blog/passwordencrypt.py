import hashlib
import random
import string

USERNAME_HASH_SEPARATOR = "|"
SALT_LENGTH = 5

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(SALT_LENGTH))

def make_cookie(userid, hashpw):
	return '%s%s%s' %(userid, USERNAME_HASH_SEPARATOR, hashpw)
	
# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(username, pw):
    salt = make_salt()
    h = make_pw_hash1(username, pw, salt)
    return (h, salt)

    
def make_pw_hash1(username, pw, salt):
    h = hashlib.sha256(username + pw + salt).hexdigest()
    return h

def decode_cookie(cookie_val):
    if cookie_val:
    	 idx = cookie_val.index(USERNAME_HASH_SEPARATOR)
       	 return (cookie_val[:idx], cookie_val[idx+1:])

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s|HASH
# and returns s if hash_str(s) == HASH, otherwise None 

'''
def check_secure_val(h):
    ###Your code here
    if h:
        idx1 = h.index(USERNAME_HASH_SEPARATOR)
        idx2 = h[idx1:].index(SALT_SEPARATOR)
        if idx1 > 0 and idx2 > 0:
            username = h[0:idx1]
            passwordhash = h[idx1:idx2]
            salt= h[-SALT_LENGTH:]
            if make_pw_hash(username, passwordhash, salt) ==  :
                return value'''

#h = make_cookie('spez', 'hunter2')
hh = make_pw_hash('rrr', 'rrr')
#print "%s %s" %(hh[0], hh[1])
#print "make_cookie('spez', 'hunter2') = %s" %h
#print decode_cookie("dadad|ddsada")

#isvalid = check_secure_val('spez|ebb2346c30ae92e539273e0732f99c065f0364dc5200210d4f625445f6ddbb1b|lUxOq')
#print "check_secure_val('spez|ebb2346c30ae92e539273e0732f99c065f0364dc5200210d4f625445f6ddbb1b|lUxOq') = %s" %str(isvalid)

#print "check_secure_val('5|e4da3b7fbbce2345d7772b0674a318d5') = %s" %(check_secure_val("5|e4da3b7fbbce2345d7772b0674a318d5"))
#print "check_secure_val('spez|e9c8af3e8a4affb4f23f2b953b8ab634701d68dc8dc1e82633147d84d7de85ba,QlPyd') = %s" %(check_secure_val("spez|e9c8af3e8a4affb4f23f2b953b8ab634701d68dc8dc1e82633147d84d7de85ba,QlPyd"))
