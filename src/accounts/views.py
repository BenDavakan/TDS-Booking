from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from kkiapay import Kkiapay


from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from accounts.forms import EditProfileForm, ManagerEditChambre, SignupForm, SigninForm
from accounts.models import CustomUser, HotelManager, Profile
from hotels.models import Chambre, Payement, Reservation


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
    user = request.user
    profil = Profile.objects.get(user=user.id)
    profil.gender = "Masculin"
    profil.save()

    print(profil.gender)

    return render(request, 'edit_profil.html', {'profil': profil})


def mes_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user.id)

    return render(request, 'accounts/mes_reservations.html', {'reservations': reservations})


def detail_reservation(request, token):

    reservation = get_object_or_404(Reservation, token=token)

    return render(request, 'accounts/detail_reservation.html', {'reservation': reservation})


def annul_reservation(request, token):

    reservation = Reservation.objects.get(token=token)
    reservation.status = "AN"
    reservation.save()

    return HttpResponseRedirect(reverse('reservation', args=[token]))


def mes_paiements(request):
    user = request.user

    paiements = Payement.objects.filter(reservation__user=user)

    return render(request, 'accounts/mes_paiements.html', {'paiements': paiements})


def detail_paiement(request, token):
    paiement = get_object_or_404(Payement, token=token)

    k = Kkiapay('286874f0fedb11eca56ad905c440058f',
                'tpk_28689c01fedb11eca56ad905c440058f', 'tsk_28689c02fedb11eca56ad905c440058f', sandbox=True)
    transaction = k.verify_transaction(paiement.transaction_id)
    return render(request, 'accounts/detail_paiement.html', {'paiement': paiement, 'transaction': transaction, })


def dashboard_admin(request):
    return render(request, 'accounts/admin/dashboard_admin.html')


def manager_chambres(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    chambres = Chambre.objects.filter(hotel=manager.hotel)

    return render(request, 'hotels/manager/chambres/index.html', {'chambres': chambres})


def manager_chambre(request, number):
    chambre = get_object_or_404(Chambre, number=number)
    form = ManagerEditChambre()

    return render(request, 'hotels/manager/chambres/chambre.html', {"form": form, 'chambre': chambre})
