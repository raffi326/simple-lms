from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.views.generic import RedirectView
from core.apiv1 import apiv1

def home(request):
    return HttpResponse("Welcome to Simple LMS 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', apiv1.urls),
]