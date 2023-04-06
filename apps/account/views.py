from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import NewUserForm
from .models import Test


def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Успешная регистрация" )
			return redirect("home")
		messages.error(request, "Регистрация не завершена. Неверная информация")
	form = NewUserForm()
	return render (request=request, template_name="account/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Вы вошли под аккаунтом {username}.")
				return redirect("home")
			else:
				messages.error(request,"Неправильный логин или пароль.")
		else:
			messages.error(request,"Неправильный логин или пароль.")
	form = AuthenticationForm()
	return render(request=request, template_name="account/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "Вы успешно вышли из аккаунта.") 
	return redirect("home")


@login_required
def account(request):
	context = {}
	tests = Test.objects.filter(users__in=[request.user,])
	context['tests'] = tests
	return render(request, 'account/account.html', context)


@login_required
def test(request, pk):
	if not Test.objects.filter(pk=pk).exists():
		return Http404()
	context = {}
	test = Test.objects.get(pk=pk)
	context['test'] = test
	return render(request, 'account/test_details.html', context)


@login_required
def pass_test(request, pk):
	if not Test.objects.filter(pk=pk).exists():
		return Http404()
	test = Test.objects.get(pk=pk)
	if request.user in test.users.all():
		return Http404()


def all_tests(request):
	tests = Test.objects.all()
	return render(request, 'account/all_tests.html', {'tests': tests})