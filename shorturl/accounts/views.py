from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View

from shortener.models import Link
from shorturl import settings

class SignUpView(View):
    """Представление для формы регистрации"""
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Замените 'login' на URL, куда вы хотите перенаправить пользователя
        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    """Представление для формы входа"""
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Перенаправление пользователя после успешного входа
            return redirect('user_links')  # Замените 'home' на URL вашей домашней страницы
        return render(request, 'login.html', {'form': form})

class UserLinksView(View):
    """Представление для вывода всех ссылок у авторизированного пользователя"""
    def get(self, request):
        user = request.user  # Получаем текущего пользователя
        links = Link.objects.filter(user=user)  # Фильтруем ссылки по пользователю

        domain_url = getattr(settings, 'DOMAIN_URL', 'http://127.0.0.1:8000/')  # Получаем DOMAIN_URL из настроек Django

        return render(request, 'user_links.html', {'links': links, 'domain_url': domain_url})