from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserOurRegistrations, ProfileImage, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import News


def register(request):
    if request.method == "POST":
        form = UserOurRegistrations(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} был(а) успешно зарегистрирован! Вы можете войти в личный кабинет')
            return redirect('auth')
    else:
        form = UserOurRegistrations()
    return render(request, 'users/registration.html', {'form':form})

@login_required
def profile(request):
    context = {
        'posts': News.objects.filter(author=request.user)
    }

    return render(request, 'users/profile.html', context)

@login_required
def change(request):
    if request.method == "POST":
        img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
        update_user = UserUpdateForm(request.POST, instance=request.user)

        if img_profile.is_valid() and update_user.is_valid():
            img_profile.save()
            update_user.save()
            messages.success(request, 'Ваш аккаунт успешно обновлен!')
            return redirect('profile')
    else:
        img_profile = ProfileImage(instance=request.user.profile)
        update_user = UserUpdateForm(instance=request.user)

    data = {
        'img_profile': img_profile,
        'update_user': update_user,
    }

    return render(request, 'users/profile_change.html', data)
