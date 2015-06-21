import urllib, hashlib
import os
from django.db.models.fields.files import FileField

#Clean File Fields
def clean_files(sender, **kwargs):
    for field in sender._meta._fields():
        if isinstance(field, FileField):
            inst = kwargs['instance']
            f = getattr(inst, field.name)
            m = inst.__class__._default_manager
            if os.path.exists(f.path) \
                    and not m.filter(**{'%s__exact' % field.name: getattr(inst, field.name)})\
                    .exclude(pk=inst._get_pk_val()):
                        os.remove(f.path) 

#Validations 
def verify_email(data):
	if(len(data)==0):
		return False
	data=data.lower()
	allowed = "1234567890abcdefghijklmnopqrstuvxzyw_.@"
	for c in data:
		if(not c in allowed):
			return False
	return True

def verify_number(data):
	if(len(data)<7):
		return False
	data=data.lower()
	allowed = "1234567890"
	for c in data:
		if(not c in allowed):
			return False
	return True

def verify_password(data,dataux):
	if(len(data)==0):
		return False
	if(data==dataux):
		if(len(data)>6):
			return True
	return False

def verify_name(data,dataux):
	if(len(data)==0 or len(data)>=30):
		return False
	if(len(dataux)==0 or len(dataux)>=30):
		return False
	allowed = "abcdefghijklmnopqrstuvxzyw"
	for c in data.lower():
		if(not c in allowed):
			return False
	for c in dataux.lower():
		if(not c in allowed):
			return False
	return True

def getGravatar(email,size):
	# Set your variables here
	#default = "http://www.example.com/default.jpg"
	default="https://www.gravatar.com/avatar/3bc36c7cdb9d3ef3a3e48802c693ea38?s="+str(size)
 
	# construct the url
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
	return gravatar_url
