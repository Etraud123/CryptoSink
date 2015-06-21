import os
import datetime
import M2Crypto
import hashlib
import base64
import random
import string
import struct
from Crypto.Cipher import AES
from Crypto import Random
import binascii
import json

SYM_KEY_SIZE = 16 # 16;32;64
BLOCKSIZE = 65536 # for creating hashes

#
# Hash Creator
#
def create_hash(info,is_file):
	hasher=hashlib.sha1()
	if is_file == True:
		with open(info,'rb') as afile:
			buf=afile.read(BLOCKSIZE)
			while len(buf) >0:
				hasher.update(buf)
				buf=afile.read(BLOCKSIZE)
		return hasher.hexdigest()
	else:
		hasher.update(info)
		return hasher.hexdigest()

#
# Generate Random String
#
def gen_rand_string(N):
	return unicode(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N)),'utf8')
	
#
# Encrypt Files using AES
#
def encrypt_file(key, in_filename, out_filename,iv):
    cipher=M2Crypto.EVP.Cipher('aes_256_cfb',key,iv, op=1)
    with open(in_filename, 'rb') as infile:
        with open("tmp/" + out_filename, 'wb') as outfile:
          #outfile.write(b)
          while True:
            buf = infile.read(1024)
            if not buf:
                break
            outfile.write(cipher.update(buf))

          outfile.write( cipher.final() )  
          outfile.close()
        infile.close()

#
# Decrypt Files using AES
#
def decrypt_file(key, in_filename, out_filename,iv):
    cipher = M2Crypto.EVP.Cipher("aes_256_cfb",key , iv, op = 0)
    with open(in_filename, 'rb') as infile: 
        with open(out_filename, 'wb') as outfile:
          while True:
            buf = infile.read(1024)
            if not buf:
                break
            try:
                outfile.write(cipher.update(buf))
            except:
                print "here"
          outfile.write( cipher.final() )  
          outfile.close()
        infile.close()

#
# Function For Key Generation Pair
#
def key_pair_generator(user_name,size_key):
	print "Generating a 1024 bit private/public key pair for %s..." % user_name

	User = M2Crypto.RSA.gen_key (size_key, 65537)

	private_key = "key/" + user_name + '-private.pem'
	public_key = "key/" + user_name + '-public.pem'

	User.save_key (private_key, None)
	User.save_pub_key (public_key)

	return (private_key, public_key)

#
# Function to encrypt Message/file
#

def encrypt_info(file_name_to_encrypt,public_key_name):

	#Load user RSA Public Key For encryption
	UserRSA = M2Crypto.RSA.load_pub_key (public_key_name)

	sym_key = gen_rand_string(SYM_KEY_SIZE)

	temporary_file_name = gen_rand_string(8)
	iv = gen_rand_string(8)

	encrypt_file(sym_key,file_name_to_encrypt,temporary_file_name,iv)

	sym_key_private = UserRSA.public_encrypt(sym_key,M2Crypto.RSA.pkcs1_oaep_padding).encode('base64')

	return (temporary_file_name,sym_key_private,iv)

#
# Adding header to cypher file
#
def adding_header(file_name, hash_file_encrypted, hash_timestamp_encrypted):
	header = hash_file_encrypted + "#" + hash_timestamp_encrypted
	with open(file_name, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(header + '\n' + content)


#
# Check if the file is the owner
#
def is_allowed_to_decrypt(public_key_name,hash_file,hash_timestamp, timestamp, file_to_check):

	tmp_hash_timestamp = create_hash(str(timestamp), False)
	tmp_hash_file = create_hash(file_to_check,True)

	VerifyRSA = M2Crypto.RSA.load_pub_key("key/system-public.pem")

	MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')
	MsgDigest.update (tmp_hash_file)
	file_ctrl = VerifyRSA.verify_rsassa_pss (MsgDigest.digest (), base64.b64decode(hash_file))

	MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')
	MsgDigest.update (tmp_hash_timestamp)
	time_ctrl = VerifyRSA.verify_rsassa_pss (MsgDigest.digest (), base64.b64decode(hash_timestamp))

	if time_ctrl == 1 and file_ctrl == 1:
		return True
	else:
		return False



#
# Function to decrypt the file
#
def decrypt_info(dict_info, private_key_name,public_key_name):

	ReadRSA = M2Crypto.RSA.load_key(private_key_name)

	temporary_file_name = "tmp/" + dict_info["path"]

	if is_allowed_to_decrypt(public_key_name,dict_info["hash_file"], dict_info["hash_timestamp"],dict_info["time"],temporary_file_name):

		key_plain = ReadRSA.private_decrypt(base64.b64decode(dict_info["key"]), M2Crypto.RSA.pkcs1_oaep_padding)

		
		final_file_name = "media/" + dict_info["file_name"]
		iv = dict_info["iv"]

		decrypt_file(key_plain,temporary_file_name,final_file_name, iv);

		return True
	else:

		print "User Not allowed"
		return False


#
# Function to delete temporary files
#
def delete_tmp_file(folder_tmp, file_name):
	os.remove(folder_tmp + file_name)

#
# Function to encrypto control access to file
#
def encrypt_control_var(user_private_key,timestamp, input_file, pub):

	tmp_hash_timestamp = create_hash(str(timestamp), False)
	tmp_hash_file = create_hash(input_file,True)

	UserRSA = M2Crypto.RSA.load_key("key/system-private.pem")

	MsgDigest = M2Crypto.EVP.MessageDigest ('sha1')

	MsgDigest.update (tmp_hash_file)
	Signature = UserRSA.sign_rsassa_pss (MsgDigest.digest ())
	hash_file_encrypted =  Signature.encode ('base64')

	MsgDigest_2 = M2Crypto.EVP.MessageDigest ('sha1')
	MsgDigest_2.update (tmp_hash_timestamp)
	Signature = UserRSA.sign_rsassa_pss (MsgDigest_2.digest ())
	hash_timestamp_encrypted =  Signature.encode ('base64')

	return (hash_file_encrypted,hash_timestamp_encrypted)

#
# MAIN!!
#
'''
def start_engine(user,timestamp,input_file):
	timestamp = datetime.datetime.now()
	author = "Duarte"
	input_file = "D3.pdf"

	#--------- Key generator ---------#
	(user_private_key, user_public_key) = key_pair_generator(author,1024)
	#--------- END ---------#

	#--------- Encryption of a input.txt file ---------#
	print "\n SYS: Encrypting the File: %s" % input_file
	(tmp_file_name,sym_key_private,iv) = encrypt_info(input_file, user_public_key)

	print "\n SYS: Encrypting control vars...."
	(hash_file_encrypted,hash_timestamp_encrypted) = encrypt_control_var(user_private_key,timestamp,"tmp/" + tmp_file_name, user_public_key)

	print "\n SYS: Adding File to Pilot: %s | For User: %s" % (input_file,author)
	add_to_pilot_file(author,timestamp, input_file, tmp_file_name,sym_key_private,iv,hash_file_encrypted,hash_timestamp_encrypted)
	#--------- END ---------#

	#--------- Decryption of input.txt file ---------#
	print "\n SYS: Decrypting File: %s"  % input_file
	if decrypt_info(input_file,user_private_key,user_public_key):

		print "\n SYS: Deleting temp files"
		delete_tmp_file("tmp/", tmp_file_name)
	#--------- END ---------#
'''