from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def home(request):
	return HttpResponse("<h1>hello</h1>")


def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Your account has been created! You are now able to login!")
			return redirect('users-login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form, 'title': 'Register'})
