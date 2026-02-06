from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Cliente

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'cliente'):
                    return redirect('home')
                elif hasattr(user, 'venditore'):
                    return redirect('dashboard_vendite')
                else:
                    return redirect("home")
            else: 
                form.add_error(None, "Username o password non validi")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form":form} )

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            try:
                user=User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                Cliente.objects.create(
                    utente=user,
                    telefono=form.cleaned_data['telefono'],
                    indirizzo=form.cleaned_data['indirizzo'],
                    newsletter=form.cleaned_data['newsletter']
                )
            except Exception as e:
                form.add_error(None, "Errore durante la registrazione")
            login(request, user)
            return redirect('home')
    else:
        form=RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})