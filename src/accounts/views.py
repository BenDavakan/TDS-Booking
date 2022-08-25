
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from accounts.forms import ProfileForm, SignupForm, SigninForm, UserForm
from accounts.models import CustomUser, Profile


def inscription_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            form = SignupForm()
            return render(request, 'accounts/auth/signup.html', {"error": "Les mots de passse ne correspondent pas", "form": form})
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(
                request, "L'email est déja pris!! Réessayez avez un autre.")
            return redirect('inscription')
        else:
            CustomUser.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, tel=97662516,)
            return redirect('connexion')
    else:
        form = SignupForm()
        return render(request, 'accounts/auth/signup.html', {"form": form})


def connexion_view(request):
    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = SigninForm()
            return render(request, 'accounts/auth/signin.html', {"error": "Erreur de connexion, veuillez réesayer.", "form": form})
    else:
        form = SigninForm()
        return render(request, 'accounts/auth/signin.html', {"form": form})


def deconnexion(request):
    logout(request)
    return redirect('home')


def profil_view(request):
    return render(request, 'accounts/auth/profil/index.html', {'user': request.user})


def edit_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST,
                             instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)

        if user_form.is_valid():

            user_form.save()

            profile_form.save()

            return redirect('edit-profil')

    else:

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/auth/profil/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'profile': profile})
