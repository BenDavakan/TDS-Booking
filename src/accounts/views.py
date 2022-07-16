from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import EditProfileForm, SignupForm, SigninForm
from accounts.models import CustomUser
from hotels.models import Payement, Reservation


def inscription_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            form = SignupForm()
            return render(request, 'signup.html', {"error": "Les mots de passse ne correspondent pas", "form": form})
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
        return render(request, 'signup.html', {"form": form})


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
            return render(request, 'signin.html', {"error": "Erreur de connexion, veuillez réesayer.", "form": form})
    else:
        form = SigninForm()
        return render(request, 'signin.html', {"form": form})


def deconnexion(request):
    logout(request)
    return redirect('home')


def profil_view(request):
    return render(request, 'profil.html', {'user': request.user})


def edit_profile(request):
    return render(request, 'edit_profil.html', {})


def mes_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user.id)

    return render(request, 'accounts/reservations.html', {'reservations': reservations})


def mes_paiements(request):
    user = request.user

    paiements = Payement.objects.filter(reservation__user=user)

    return render(request, 'accounts/paiements.html', {'paiements': paiements})
