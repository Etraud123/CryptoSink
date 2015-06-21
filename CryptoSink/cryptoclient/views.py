from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from cryptoclient.models import *
from django.contrib.auth import logout
from django.db.models import *
from django.template import RequestContext
from datetime import datetime
from django.views.static import serve

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


from engine import * 

# Create your views here.

#
# Function to init the content of the page
#

def init(request):
	context={}
	context['page_title'] = 'CryptoSink Client'
	context['meta_description']='CryptoSink Client'
	context['meta_author']='Duarte Monteiro'
	context['project_name']='CryptoSink'
	context['project_description']='Storage Sharer and encryptor'
	context['is_user_authenticated'] = False
	if request.user.is_authenticated():
		print request.user.id
		tmp_user = userapp.objects.filter(user=request.user.id)
		print tmp_user
		logi = logs.objects.filter(user=tmp_user)[:10]
		print logi
		context["logs"] = logi.reverse()
		context["len_logs"] = len(logi)
		context["is_user_authenticated"] = True
		context["user_name"] = request.user.username
	return context

#
# Landing page for /
#
@login_required(login_url='/admin/')
def home(request):
	
	context = init(request)

	if request.user.is_authenticated():
		tmp_user = userapp.objects.filter(user=request.user.id)[0]
		pilot_file = pilot.objects.filter(user=tmp_user)
		tmp_ret = []
		for tmp_file in pilot_file:
			tmp_date = tmp_file.timestamp.split("-")
			mes = tmp_date[1]
			dia = tmp_date[2].split(" ")[0]
			tmp_ret.append({"file_name": tmp_file.file_name, "time":str(mes) + "/" + str(dia) ,"size": tmp_file.size})

		context["tmp_file_array"] = tmp_ret
	return render_to_response('client.html',context)

@login_required(login_url='/admin/')
def logout_user(request):
	context = init(request)
	logout(request)
	return render_to_response('client.html',context)

@login_required(login_url='/admin/')
def upload_user(request):
	context = init(request)
	return render_to_response('upload.html',context)


def handle_uploaded_file(f):
	print "HANDLE UPLOADED FILE"
	with open(PROJECT_ROOT+'/name.txt', 'wb+') as destination:
		destination.write(f)

@login_required(login_url='/admin/')
def upload_file(request):
	context = init(request)
	print "Function upload file"
	if request.method == 'POST':
		#Check if user is authenticated
		if request.user.is_authenticated():
			file = request.FILES['file']
			#handle_uploaded_file(request.FILES['file'])
			ctrl_save_file = True
			file_name_old = file.name
			print "FILE NAME OF THE UPLOADED FILE:", file_name_old
			try:
				path = default_storage.save(file_name_old, ContentFile(file.read()))
			except:
				ctrl_save_file = False

			context["ctrl_save_file"] = ctrl_save_file

			# If saved the file
			if ctrl_save_file:
				engine_handler(file_name_old,request.user)

	tmp_log = logs()
	tmp_log.log_type = 0
	tmp_user = userapp.objects.filter(user=request.user.id)[0]
	tmp_log.user = tmp_user
	tmp_log.description = "File has upload/encrypted: %s" % file_name_old
	tmp_log.save()

	context["ctrl_save_file"] = ctrl_save_file
	context["file_name"] = file_name_old
	return render_to_response('upload.html', context)

def add_to_pilot_file(user,timestamp,file_name, file_random_name, key, iv,file_hash,timestamp_hash):
	tmp_pilot_i = pilot()
	tmp_pilot_i.user = user
	tmp_pilot_i.file_name = file_name
	tmp_pilot_i.timestamp = timestamp
	tmp_pilot_i.path = file_random_name
	tmp_pilot_i.sym_key = key
	tmp_pilot_i.iv = iv
	tmp_pilot_i.hashfile = file_hash
	tmp_pilot_i.hashtime = timestamp_hash
	tmp_pilot_i.save()

def remove_tmp_file(file_name):
	os.remove(file_name)


def engine_handler(file_name_old,user):
	#Check if user has public_key
	tmp_user = userapp.objects.filter(user=user.id)[0]
	print tmp_user.public_key
	print "CHECKING IF THERE IS A PUBLIC KEY ELSE GENERATES"
	if tmp_user.public_key == "":
		
		tmp_log = logs()
		tmp_log.log_type = 1
		tmp_log.user = tmp_user
		tmp_log.description = "Key pair generated for user: %s" % tmp_user.user.username
		tmp_log.save()
		
		pilot.objects.filter(user=tmp_user).delete()
		(user_private_key, user_public_key) = key_pair_generator(tmp_user.user.username,tmp_user.key_pair_size)
		userapp.objects.filter(user=user.id).update(public_key=user_public_key)
	else:
		user_private_key = "key/" + tmp_user.user.username + '-private.pem'
		user_public_key = "key/" + tmp_user.user.username + '-public.pem'

	tmp_dropbox = engine.objects.all()[0]
	if tmp_dropbox.is_set == False:
		key_pair_generator("system", 1024)

	print "GENERATING TIMESTAMP"
	#create time stamp
	timestamp = datetime.datetime.now()
	print "ENCRYPTING FILE"
	#encrypt file

	(tmp_file_name,sym_key_private,iv) = encrypt_info("media/" + file_name_old, user_public_key)

	(hash_file_encrypted,hash_timestamp_encrypted) = encrypt_control_var(user_private_key,timestamp,"tmp/" + tmp_file_name, user_public_key)
	#(hash_file_encrypted,hash_timestamp_encrypted) = system_encrypt_var(tmp_file_name)

	if dropbox_engine(tmp_file_name):
		add_to_pilot_file(tmp_user,timestamp, file_name_old, tmp_file_name,sym_key_private,iv,hash_file_encrypted,hash_timestamp_encrypted)

		remove_tmp_file("media/" + file_name_old)
		remove_tmp_file("tmp/" + tmp_file_name)

	else:
		remove_tmp_file("media/" + file_name_old)
		remove_tmp_file("tmp/" + tmp_file_name)


	#dropbox_engine(tmp_file_name)


#
# BEGIN DROPBOX CONECTION
#
import dropbox 
token = "cin_Ql8TPTMAAAAAAAAGkK_P5Ermvm9i-X6IB6r0FNQf8w9jnq-7z4nLFySsDFuM"

def dropbox_handler():

	tmp_dropbox = engine.objects.all()[0]
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(tmp_dropbox.app_key, tmp_dropbox.app_secret)
	client = dropbox.client.DropboxClient(token)
	print 'linked account: ', client.account_info()
	if tmp_dropbox.is_set == False:
		client.file_create_folder("sync")
		engine.objects.filter(pk=tmp_dropbox.id).update(is_set=True)

	return client 


def dropbox_engine(file_name):
	
	drop_handler = dropbox_handler()	

	try:	
		folder_metadata = drop_handler.metadata('/sync')
		print "metadata:", folder_metadata
	except:
		print "Error! Checking if folder exists"
		return None

	try:
		f = open("tmp/" + file_name, 'rb')
		response = drop_handler.put_file("sync/" + file_name, f)
		print 'uploaded: ', response
		folder_metadata = drop_handler.metadata('/sync')
		print "metadata:", folder_metadata
	except Exception as e:
		print e
		return None
	return True

#
# Delete files from the system
#
def delete_file_from_server(file_name_input,user,d_handler):
	tmp_user = userapp.objects.filter(user=user.id)[0]
	tmp_pilot_i = pilot.objects.filter(file_name=file_name_input)[0]
	if tmp_pilot_i.user == tmp_user:
		tmp_pilot_i.delete()
		d_handler.file_delete("sync/" + tmp_pilot_i.path)
	else:
		return None
	return True


#
# Function to get info about a project 
#
def get_file_info(file_name_input, author):
	tmp_i = pilot.objects.filter(file_name=file_name_input,user=author)[0]
	ret = {}
	ret["hash_file"] = tmp_i.hashfile
	ret["hash_timestamp"] = tmp_i.hashtime
	ret["file_name"] = tmp_i.file_name
	ret["iv"] = tmp_i.iv
	ret["key"] = tmp_i.sym_key
	ret["time"] = tmp_i.timestamp
	ret["path"] = tmp_i.path
	return ret 


#
# Download File View
#
@login_required(login_url='/admin/')
def download_file(request):
	context = init(request)
	tmp_user = userapp.objects.filter(user=request.user.id)[0]
	if request.method == 'POST':
		print request.POST
		d_handler = dropbox_handler()
		if request.POST.has_key("Delete"):
			print "ENTREI EM DELETEFUNCTION"
			tmp_log = logs()
			tmp_log.log_type = 0
			tmp_log.user = tmp_user
			tmp_log.description = "File Deleted: %s" % str(request.POST["file_name"])
			tmp_log.save()
			if delete_file_from_server(request.POST["file_name"],request.user,d_handler):
				return HttpResponseRedirect('/#0')
		else:
			print "ENTREI EM DOWNLOAD FUNCTION"

			file_name_post = request.POST["file_name"]
			tmp_i = pilot.objects.filter(file_name=file_name_post)[0]

			print "RETRIVING FILES FROM DROPBOX"
			f, metadata = d_handler.get_file_and_metadata("sync/"+ tmp_i.path)
			out = open("tmp/" + tmp_i.path, 'wb')
			out.write(f.read())
			out.close()
			print metadata
			print "LOCALIZACAO DO FICHEIRO: tmp/%s" % tmp_i.path

			print "COMECAR A DECIFRAR"
			tmp_user = userapp.objects.filter(user=request.user.id)[0]
			print tmp_user.public_key
			print "CHECKING IF THERE IS A PUBLIC KEY ELSE GENERATES"
			if tmp_user.public_key != "":
				user_private_key = "key/" + tmp_user.user.username + '-private.pem'
				user_public_key = "key/" + tmp_user.user.username + '-public.pem'
			else:
				return HttpResponseRedirect('/#0')

			print "BUSCAR INFORMACAO DO FICHEIRO NA BASE DE DADOS %s" % file_name_post
			dict_info = get_file_info(str(file_name_post),tmp_user)
			if decrypt_info(dict_info ,user_private_key, user_public_key):
				remove_tmp_file("tmp/" + tmp_i.path)
				path_to_file =PROJECT_ROOT + "/media/" + tmp_i.file_name
				tmp_log = logs()
				tmp_log.log_type = 0
				tmp_log.user = tmp_user
				tmp_log.description = "File DOWNLOADED: %s" % str(request.POST["file_name"])
				tmp_log.save()
				return serve(request, os.path.basename(path_to_file), os.path.dirname(path_to_file))
			else:
				return HttpResponseRedirect('/#0')

