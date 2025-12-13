from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """
    Simple landing page for the backend root route
    """
    return render(request, 'main/home.html')


