from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

def login_user(request):
    print(f"Método da requisição: {request.method}")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Loggin form success, logging...")
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print(f"Login form error: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login_user.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login_user')

def register_user(request):
    if request.method == 'POST':
        nome = request.POST.get('username')
        email = request.POST.get('email')
        s1 = request.POST.get('password1')
        s2 = request.POST.get('password2')

        if s1 != s2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'accounts/register_user.html')

        if User.objects.filter(username=nome).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return render(request, 'accounts/register_user.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return render(request, 'accounts/register_user.html')

        try:
            user = User.objects.create_user(username=nome, email=email, password=s1)
            user.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login_user')
        except Exception as e:
            messages.error(request, "Erro ao criar conta. Tente novamente.")
            
    return render(request, 'accounts/register_user.html')
