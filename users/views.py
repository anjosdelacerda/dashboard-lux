from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro realizado com sucesso! Faça o login.')
            return redirect('admin:index') 
        else:
            pass
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})