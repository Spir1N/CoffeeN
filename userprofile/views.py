from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm

@login_required
def profile_view(request):
    profile = request.user.profile  # получаем связанную модель
    return render(request, 'userprofile/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            profile.sync_to_user()  # обновляем данные пользователя
            return redirect('userprofile:profile')
    else:
        profile.sync_from_user()  # заполняем поля из User
        form = ProfileForm(instance=profile)

    return render(request, 'userprofile/edit_profile.html', {'form': form})