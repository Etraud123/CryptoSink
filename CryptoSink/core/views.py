#!/usr/bin/env python
# encoding: utf-8

# Project: MadLabs 
# Version: Core (0.1)
# Author: Renato Rodrigues - renato.rodrigues@bip.pt
# Blip, 2014

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from core.utils import *
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as _login

#Main Method - Set Global Vars 
def init():
	context={}
	context['meta_description']='MadLabs going mad...'
	context['meta_author']='Renato Rodrigues'
	context['project_name']='MadLabs'
	context['project_description']='Mad...'
	return context


def home(request):
	context=init()
	context["title"]='MadLabs - Home'
	return render_to_response('index.html',context)
	
def core(request):
	context=init()
	context["title"]='MadLabs - Core 🐵'
	return render_to_response('core.html',context)


#Login Page
def login(request):
	context=init()
	context["title"]='MadLabs - Login'

	context.update(csrf(request))
	if(request.method=="POST"):
		if('username' in request.POST and 'passwd' in request.POST):
			user = authenticate(username=request.POST['username'], password=request.POST['passwd'])
			if user is not None:
				if user.is_active:
					_login(request,user)
					return redirect('/core/')
				else:
					context["login_error"]={"level":"warning","title":"Activation!","message":" Please follow activation instructions."}
			else:
				context["login_error"]={"level":"danger","title":"Error:","message":" Username or password invalid."}
	if request.user.is_authenticated():
		return core(request)
	else:
		return render_to_response('login.html',context)


#Register Page
def register(request):
	context=init()
	context["title"]='MadLabs - Register New Account'
	
	context.update(csrf(request))
	if(request.method=="POST"):
		#Check for Missing Information
		if(not request.POST.has_key('username')):
			context["register_error"]={"level":"danger","title":"Error:","message":" Missing Email Information."}
		elif(not request.POST.has_key('passwd') or not request.POST.has_key('passwdaux')):
			context["register_error"]={"level":"danger","title":"Error:","message":" Password is Missing."}
		elif(not request.POST.has_key('fname')):
			context["register_error"]={"level":"danger","title":"Error:","message":" First Name is Missing."}
		elif(not request.POST.has_key('lname')):
			context["register_error"]={"level":"danger","title":"Error:","message":" Last Name is Missing."}

		username = request.POST['username']
		mail = request.POST['username'].lower()
		passwd = request.POST['passwd']
		fname = request.POST['fname']
		lname  = request.POST['lname']
		
		#Validate Fields
		valid=True
		if(not verify_email(mail)):
			context["register_error"]={"level":"danger","title":"Error:","message":" Invalid Email Address."}
			valid=False
		elif(not verify_password(passwd,request.POST['passwdaux'])):
			context["register_error"]={"level":"danger","title":"Error:","message":" Passwords Don't Match."}
			valid=False
		elif(not verify_name(fname,lname)):
			context["register_error"]={"level":"danger","title":"Error:","message":" Invalid Name."}
			valid=False
		
		#Check if User Exists
		u = User.objects.filter(username=mail)
		if(len(u)==0 and valid):
			try:
				#Create User
				user = User.objects.create_user(username=username, email=mail, password=passwd)
				user.active = True
				user.first_name = fname
				user.last_name = lname
				user.save()
				#Add User to Free Group
				group = Group.objects.get(name='Free') 
				group.user_set.add(user)
				group.save()
				context["register_error"]={"level":"success","title":"Success:","message":"User Registered Successful. Redirecting..."}
				context["redirect_login"]=True
			except Exception, e:
				print e
		elif(valid):
			context["register_error"]={"level":"danger","title":"Error:","message":"User Not Available."}
	if request.user.is_authenticated():
		return core(request)
	else:
		return render_to_response('register.html', context)
	


