from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .forms import SignUpForm, LoginForm

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Falha na validação de segurança. Tente novamente.")
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    }
    return render(request, 'accounts/login_user.html', context)

def logout_user(request):
    logout(request)
    return redirect('login_user')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Este nome de usuário já está em uso.")
                return render(request, 'accounts/register_user.html', {
                    'form': form, 
                    'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
                })
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Este e-mail já está registrado.")
                return render(request, 'accounts/register_user.html', {
                    'form': form, 
                    'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
                })

            try:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Conta criada com sucesso! Faça o login.")
                return redirect('login_user')
            except Exception:
                messages.error(request, "Erro ao criar conta. Tente novamente.")
        else:
            messages.error(request, "Não foi possível cadastrar o usuário.")
    else:
        form = SignUpForm()
    
    context = {
        'form': form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    }
    return render(request, 'accounts/register_user.html', context)
