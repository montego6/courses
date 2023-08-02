from django.shortcuts import  render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group

def registration(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			if(form.cleaned_data['is_teacher']):
				teachers_group = Group.objects.get(name='teachers') 
				teachers_group.user_set.add(request.user)
			return redirect("index")
		else: 
			print(form.errors)
	else:
		form = UserRegistrationForm()
	return render (request, "register.html", context={"form":form})