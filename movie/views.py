from django.shortcuts import get_object_or_404,render,redirect,reverse
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm,RatingForm
from . import urls
from .models import movies
import pandas as pd
from . import forms
from item_item import calculateitem
from user_user import calculateuser
from matrix_factorization import calculate

def list(request):
	
		return render(request, 'home.html')
def recommend(request):
	recommended=pd.Series()
	recommended=calculateitem(request.user.id)
	m=[]
	n=[]
	o=[]
	for i in range (0,min(15,len(recommended.index))):															
		m.append(get_object_or_404(movies,id=recommended.index[i]))
	recommended=calculateuser(request.user.id)
	for i in range (0,min(15,len(recommended.index))):															
		n.append(get_object_or_404(movies,id=recommended.index[i]))
	recommended=calculate(request.user.id)
	for i in range (0,len(recommended.index)):
		o.append(get_object_or_404(movies,id=recommended.iloc[i]['id']))
	return render(request, 'recommend.html',{'moviesitem' : m,'moviesuser' : n,'moviesfac' : o}) 

def session(request):
		movies_all = movies.objects.all().order_by('id')
		for movie in movies_all:
			movie.movie_id=movie.id
		return render(request, 'session.html', {'movies' : movies_all})
def explore(request, id=None):
	movie=get_object_or_404(movies,id=id)
	form = forms.RatingForm(request.POST or None)
	if request.POST:
		if form.is_valid():
			rating=form.save(commit=False)
			rating.account=request.user
			rating.movie_id=movie.id
			rating.save()
			return redirect('movie:session')

	else:
		return render(request, 'explore.html',{'form':form, 'movie' : movie}) 
def reg_user(request):
	state= ""
	template = 'register.html'
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/login')
		else:
			state = "Incorrect Credentials!"
	else:
		form = RegistrationForm()
	variables = {'form':form, 'state':state}
	return render(request,'register.html', variables)

def login_user(request):
	template = 'login.html'
	state="Please fill in your credentials"
	log = False
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "Logged in!"
				log = True
				user_id=user.id
				return HttpResponseRedirect('/session')
			else:
				state = "Not registered user"
		else:
			state = "Incorrect username or password!"
	variables=	{
		'state': state,
		'log': log
		}	

	
	return render(request,template, variables)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/') 