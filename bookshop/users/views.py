
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Profile
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from shop.models import  Book 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Проверки
        if password1 != password2:
            messages.error(request, "Пароли не совпадают")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует")
        elif not username or not email or not password1:
            messages.error(request, "Пожалуйста, заполните все поля")
        else:
            # Создаем пользователя
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Регистрация успешна! Войдите в систему.")
            return redirect('login')

    return render(request, 'users/register.html')




login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')  # чтобы избежать повторной отправки формы
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)





class ProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    context_object_name = 'profile_author'
    template_name = 'users/profile_author.html'
    slug_url_kwarg='slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        # Получаем все книги этого автора
        books = Book.objects.filter(author=profile)

        # Пагинация: по 6 книг на страницу
        paginator = Paginator(books, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj  # для шаблона
        return context

    
class ProfileViewAbout(DetailView):
    model = Profile
    template_name = 'users/author_about.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'slug'


@login_required
def delete_avatar(request):
    profile = request.user.profile
    if profile.avatar:
        profile.avatar.delete(save=False)  # удаляем файл из storage
        profile.avatar = None               # очищаем поле
        profile.save()
    return redirect('profile')
