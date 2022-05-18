from django.http import HttpResponse


# Create your views here.


def index(request):
    return HttpResponse('<h1>La Page Des HÔTELS</h1><br><a href="/">Home</a>')
