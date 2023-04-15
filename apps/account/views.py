from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User

from .forms import NewUserForm
from .models import Test, TestQuestion, TestQuestionOption, TestResult


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
def test_result(request, test_pk):
	if not (Test.objects.filter(pk=test_pk).exists() and TestResult.objects.filter(test__pk=test_pk, user=request.user).exists()):
		raise Http404()
	test_result = TestResult.objects.filter(test__pk=test_pk, user=request.user).first()
	return render(request, 'account/test_result.html', {'result': test_result})


@login_required
def test_history(request):
	test_results = TestResult.objects.filter(user=request.user)
	return render(request, 'account/test_history.html', {'results': test_results})


@login_required
def pass_test(request, pk):
	if not Test.objects.filter(pk=pk).exists():
		raise Http404()
	context = dict()

	test = Test.objects.get(pk=pk)
	if not ((request.user in test.users.all()) and (not test.is_expired())):
		raise Http404()
	
	if TestResult.objects.filter(user=request.user, test=test).exists():
		test_result = TestResult.objects.filter(user=request.user, test=test).first()
		return redirect('test_result', test_pk=test.pk)

	if request.method == 'POST':
		answers = dict(request.POST)
		del answers['csrfmiddlewaretoken']
		test_result = TestResult.objects.create(user=request.user, test=test)
		choosed_options = list()
		for key, value in answers.items():
			choosed_option = TestQuestionOption.objects.filter(pk=value[0]).first()
			choosed_options.append(choosed_option)
			right_answers = TestQuestionOption.objects.filter(question__pk=key, is_answer=True)
			if choosed_option in right_answers:
				test_result.choosed_options.add(choosed_option)
				test_result.result += 1
		test_result.save()
		return redirect('test_result', test_pk=test.pk)
	
	context['test'] = test
	return render(request, 'account/pass_test.html', context)


def all_tests(request):
	tests = Test.objects.all()
	return render(request, 'account/all_tests.html', {'tests': tests})