from django.shortcuts import  render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from mailings.tasks import send_registration_letter

def registration(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			send_registration_letter.delay(user.email, user.username)
			if(form.cleaned_data['is_teacher']):
				teachers_group = Group.objects.get(name='teachers') 
				teachers_group.user_set.add(request.user)
			return redirect("course:index")
		else: 
			print(form.errors)
	else:
		form = UserRegistrationForm()
	return render (request, "register.html", context={"form":form})