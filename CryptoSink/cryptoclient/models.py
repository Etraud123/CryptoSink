#!usr/bin/python

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django import forms


import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))



# Create your models here.

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class engine(models.Model):
	app_key =  models.CharField(max_length=200,verbose_name="APP Key")
	app_secret = models.CharField(max_length=200,verbose_name="APP Secret")
	user_name = models.CharField(max_length=100,verbose_name="Dropbox User",blank=True)
	pass_word = models.CharField(max_length=100,verbose_name="Dropbox Password", blank= True)
	email = models.CharField(max_length=100,verbose_name="Dropbox Email", blank= True)
	is_set = models.BooleanField(default=False,verbose_name='Not First Run')
	public_key = models.CharField(max_length=60, verbose_name='Public Key Path', default=PROJECT_ROOT)
	date = models.DateTimeField(auto_now_add=True,verbose_name='Date of Creation')



	def __str__(self):
		return "Dropbox Instance"

	def __unicode__(self):
		return "Dropbox Instance"

	class Meta:
		verbose_name = "Dropbox Instance"
		verbose_name_plural = "Dropbox Instances"


class userapp(models.Model):
	user = models.OneToOneField(User)
	email = models.CharField(max_length=50,verbose_name="Email",blank=True)
	space_allowed =models.CharField(max_length=200,verbose_name="Space Allowed on dropbox", blank=True)
	public_key = models.CharField(max_length=6000,verbose_name="User Public Key",blank=True)
	date = models.DateTimeField(auto_now_add=True,verbose_name='Date of Creation',blank=True)
	sym_key_size = models.IntegerField(default=16,verbose_name="Size of the Symetric Key for encription",blank=True)
	key_pair_size = models.IntegerField(default=1024,verbose_name="Size of the public/private pair",blank=True)

	
	def __unicode__(self):
		return self.user.username

class pilot(models.Model):
	user = models.ForeignKey(userapp)
	file_name = models.CharField(max_length=100,verbose_name="File name")
	timestamp = models.CharField(max_length=100,verbose_name="Time Stamp")
	path = models.CharField(max_length=16,verbose_name="Path")
	sym_key = models.CharField(max_length=500,verbose_name="Symetric Key For File")
	iv = models.CharField(max_length=200,verbose_name="IV")
	hashfile = models.CharField(max_length=600,verbose_name="Hash For File")
	hashtime = models.CharField(max_length=600,verbose_name="Hash For TimeStamp")
	size = models.IntegerField(default=0,verbose_name="Size of the file")

	def __str__(self):
		return "File %s" % self.file_name

	def __unicode__(self):
		return "File %s" % self.file_name

	class Meta:
		verbose_name = "File Instance"
		verbose_name_plural = "Files Instances"

LOGTYPE = (
    ('0','File Manipulation Log'),
    ('1','User Manipulation Log'),
    ('2','Engine Manipulation Log'),
    ('3','Other Errors'),
)


class logs(models.Model):
	user = models.ForeignKey(userapp,null=True)
	log_type = models.CharField(max_length=1,choices=LOGTYPE,default="3")
	description = models.CharField(max_length=200,verbose_name="Description of the Log")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Date of Creation")

	def __str__(self):
		return "Log %s" % self.log_type

	def __unicode__(self):
		return "Log %s" % self.log_type

	class Meta:
		verbose_name = "Log Instance"
		verbose_name_plural = "Log Instances"


