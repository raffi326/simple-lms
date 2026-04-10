from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Simple LMS 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]